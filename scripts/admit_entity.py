#!/usr/bin/env python3
# VENDORED — catalog candidate-admission tool (catalog population programme).
# Generalized from dea-catalog-business-services CR-SVC-004 admit_entity.py.
# Self-deriving: id prefix, entity type, and required/enum rules come from
# schemas/entity.schema.json.
"""Entity admission tool (catalog candidate corpus).

Turns a queued intake submission (``contributions/queue/<shard>/<slug>.yaml``)
into a CANDIDATE-STATE entity subtree:

- validates the submission via the queue gate (``check_contributions``)
- derives the slug (explicit or from ``name``)
- assigns the record id ``<prefix>-<slug>-<hash6>`` where ``<prefix>`` comes
  from the projected schema's id pattern and ``<hash6>`` is the content-derived
  suffix: first 4 bytes of the SHA-256 of the canonical YAML serialization of
  the intake content mapping (everything except queue metadata), big-endian,
  6 base-31 digits over the visually-unambiguous alphabet. Assigned once;
  never recomputed (rename-stability contract).
- checks the id against every existing record id (collision aborts)
- scaffolds ``entities/v1-alpha/<shard>/<slug>-<hash>/candidates/`` — the
  record YAML (``version: 0.1.0``, ``lifecycle_status: proposed``) and the
  per-record README (RECORD-STANDARD sections). The candidates/ placement is
  what makes the vendored regenerator count the subtree as candidate state;
  a canonical root file is NOT created.
- adds the catalogue-instance governance layer with ``approval_status:
  proposed`` and a one-step provenance ladder (candidate) — honest
  pre-admission semantics per the FOUNDATIONS evidence ladder (D-4/D-5)
- marks the queue entry ``status: admitted`` with the assigned id and date

The admission PR then regenerates ``CATALOG.yaml`` (the candidates counter
grows), adds the CHANGELOG entry, and records the batch admission CR/index
row per house rules.

Usage:
  python scripts/admit_entity.py contributions/queue/<shard>/<slug>.yaml [--dry-run]
"""

from __future__ import annotations

import hashlib
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
from check_contributions import (  # noqa: E402
    REPO,
    _type_branches,
    load_schema,
    validate_queue_file,
)

ENTITIES = REPO / "entities" / "v1-alpha"
ALPHABET = "abcdefghjkmnpqrstuvwxyz23456789"  # 31 visually-unambiguous symbols
QUEUE_META = {"status", "slug", "submitted_by", "submitted", "source_bank", "source_ref",
              "assigned_id", "admitted"}
OWNER = "Emmanuel A. Otchere"


def content_hash(payload: dict) -> str:
    text = yaml.safe_dump(payload, sort_keys=True, allow_unicode=True, default_flow_style=False)
    digest = hashlib.sha256(text.encode("utf-8")).digest()
    val = int.from_bytes(digest[:4], "big")
    digits = []
    for _ in range(6):
        digits.append(ALPHABET[val % 31])
        val //= 31
    return "".join(reversed(digits))


def slug_from_name(name: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", name.strip().lower()).strip("-")
    slug = re.sub(r"-+", "-", slug)[:48].strip("-")
    if not slug:
        raise SystemExit("ERROR: cannot derive a slug from the given name")
    return slug


def id_prefix(schema: dict, rtype: str | None) -> str:
    """From the branch's id pattern ('^dea:guardrail-[a-z0-9-]+$' -> 'dea:guardrail')."""
    branches = _type_branches(schema)
    branch = branches.get(rtype, branches.get(None))
    pattern = branch.get("properties", {}).get("id", {}).get("pattern", "")
    m = re.match(r"\^?([^\\[]+?)-\[", pattern)
    if not m:
        raise SystemExit(f"ERROR: cannot derive an id prefix from schema pattern {pattern!r}")
    return m.group(1)


def existing_ids() -> set[str]:
    ids = set()
    for p in sorted(ENTITIES.rglob("*.yaml")):
        if p.name == "CATALOG.yaml":
            continue
        try:
            rec = yaml.safe_load(p.read_text(encoding="utf-8")) or {}
        except yaml.YAMLError:
            continue
        if isinstance(rec, dict) and isinstance(rec.get("id"), str):
            ids.add(rec["id"])
    return ids


def record_readme(record_id: str, record: dict) -> str:
    name = record.get("name", record_id)
    desc = str(record.get("description", "")).strip()
    sources = (record.get("evidence") or {}).get("sources") or []
    src_lines = "\n".join(
        f"- kind: `{s.get('kind')}` — reference: {s.get('reference')}" for s in sources
    )
    today = record.get("metadata", {}).get("created_at", "")
    return (
        f"# {name}\n\n"
        f"> {desc}\n\n"
        f"## Identity\n\n"
        f"- **Record id**: `{record_id}`\n"
        f"- **Type**: {record.get('type')}\n"
        f"- **Version**: {record.get('version')}\n"
        f"- **Lifecycle**: proposed (candidate corpus; admitted via the gated intake\n"
        f"  workflow; canonical admission is a separate evidence-gated step)\n\n"
        f"## Evidence\n\n"
        f"{str((record.get('evidence') or {}).get('rationale', '')).strip()}\n\n"
        f"{src_lines}\n\n"
        f"## Classification-or-relationships\n\n"
        f"Deferred: relationship assertions are not made at candidate admission;\n"
        f"bindings land at canonical admission with per-assertion evidence.\n\n"
        f"## Provenance\n\n"
        f"Ladder passage: candidate ({today}, {OWNER}).\n\n"
        f"## Governance\n\n"
        f"Functional owner: {OWNER}. Steward: {OWNER}. Approval: proposed\n"
        f"(candidate corpus; the approval decision belongs to canonical admission).\n"
    )


def build_record(entry: dict, slug: str, record_id: str, today: str, rtype: str | None) -> dict:
    content = {k: v for k, v in entry.items() if k not in QUEUE_META}
    if rtype is None:
        rtype = load_schema().get("properties", {}).get("type", {}).get("const")
    record: dict = {
        "id": record_id,
        "type": rtype if rtype else content.pop("type", None),
        "name": content.pop("name"),
        "description": content.pop("description"),
        "version": "0.1.0",
        "lifecycle_status": "proposed",
    }
    # entity-specific fields next, then the catalogue-instance layer
    for k, v in content.items():
        if k not in {"evidence", "tags"}:
            record[k] = v
    record["evidence"] = content.get("evidence")
    record["provenance"] = {
        "ladder_passage": [{"stage": "candidate", "date": today, "actor": OWNER}]
    }
    record["governance"] = {
        "functional_owner": OWNER,
        "steward": OWNER,
        "approval_status": "proposed",
        "source_and_evidence": "Candidate corpus admission; evidence sources cited per record.",
    }
    record["metadata"] = {
        "created_at": today,
        "updated_at": today,
        "created_by": OWNER,
        "status": "proposed",
    }
    if content.get("tags"):
        record["tags"] = content["tags"]
    return record


def main() -> int:
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    dry_run = "--dry-run" in sys.argv
    if len(args) != 1:
        print(__doc__)
        return 2
    queue_path = Path(args[0]).resolve()
    if not queue_path.is_file():
        print(f"ERROR: queue file not found: {queue_path}")
        return 2

    schema = load_schema()
    findings = validate_queue_file(queue_path, schema)
    if findings:
        for f in findings:
            print(f"ERROR: {f}")
        return 1

    entry = yaml.safe_load(queue_path.read_text(encoding="utf-8"))
    slug = entry.get("slug") or slug_from_name(entry["name"])
    branches = _type_branches(schema)
    type_values = [k for k in branches if k is not None]
    rtype = entry.get("type") if len(type_values) > 1 else (type_values[0] if type_values else None)
    content = {k: v for k, v in entry.items() if k not in QUEUE_META}
    suffix = content_hash(content)
    prefix = id_prefix(schema, rtype)
    record_id = f"{prefix}-{slug}-{suffix}"

    collisions = existing_ids()
    if record_id in collisions:
        print(f"ERROR: derived id {record_id} collides with an existing record — "
              f"disambiguate the name/slug")
        return 1

    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    record = build_record(entry, slug, record_id, today, rtype)

    first = slug[:1]
    shard = first if first.isalpha() and first.islower() else "0-9"
    entity_dir = ENTITIES / shard / f"{slug}-{suffix}"
    candidates_dir = entity_dir / "candidates"
    record_path = candidates_dir / (record_id.replace(":", "-").lower() + ".yaml")

    print(f"submission : {queue_path.name}")
    print(f"slug       : {slug}")
    print(f"assigned id: {record_id}")
    print(f"entity dir : entities/v1-alpha/{shard}/{slug}-{suffix}/candidates/")
    if dry_run:
        print("dry run: no files written")
        return 0

    candidates_dir.mkdir(parents=True, exist_ok=False)
    record_path.write_text(
        yaml.safe_dump(record, sort_keys=False, allow_unicode=True, default_flow_style=False),
        encoding="utf-8",
    )
    (candidates_dir / "README.md").write_text(record_readme(record_id, record), encoding="utf-8")

    entry["status"] = "admitted"
    entry["assigned_id"] = record_id
    entry["admitted"] = today
    queue_path.write_text(
        yaml.safe_dump(entry, sort_keys=False, allow_unicode=True, default_flow_style=False),
        encoding="utf-8",
    )

    print(
        "\nAdmitted (candidate state). The admission PR must also:\n"
        "  1. regenerate CATALOG.yaml (candidates counter grows)\n"
        "  2. add the CHANGELOG.md [Unreleased] entry and the batch CR + index row\n"
        "  3. commit queue entries (status: admitted) with the entity subtrees"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
