#!/usr/bin/env python3
# VENDORED — catalog candidate-intake queue gate (catalog population programme).
# Generalized from dea-catalog-business-services CR-SVC-004 check_contributions.py.
# Self-deriving: every entity-specific rule comes from schemas/entity.schema.json.
"""Contribution queue gate (catalog population programme).

Validates every ``contributions/queue/*.yaml`` intake submission:

- explicit ``status`` from the queue vocabulary (draft / queued / admitted / rejected)
- NO top-level ``id`` — record ids are assigned at admission by
  ``scripts/admit_entity.py`` (content-derived hash, id-system convention);
  hand-invented hashes are exactly what this gate exists to catch
- required identity fields (name, description) and every entity-specific
  required field + enum membership, derived from ``schemas/entity.schema.json``
  (id, type, version, lifecycle_status are admission-assigned and not
  expected in a submission)
- evidence: >= 1 source of a known kind with a non-empty reference, and a
  rationale of at least 20 characters (RECORD-STANDARD machine-checkable subset)
- multi-entity schemas (``anyOf`` over per-type branches) are dispatched by
  the submission's ``type`` field

Exit codes: 0 = queue conforms (an empty queue conforms); 1 = findings.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parents[1]
SCHEMA_PATH = REPO / "schemas" / "entity.schema.json"
QUEUE = REPO / "contributions" / "queue"

QUEUE_STATUSES = {"draft", "queued", "admitted", "rejected"}
SLUG_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
KNOWN_SOURCE_KINDS = {"repository-path", "system-of-record", "published-document"}
ADMISSION_ASSIGNED = {"id", "type", "version", "lifecycle_status"}

_SCHEMA_CACHE: dict | None = None


def load_schema() -> dict:
    global _SCHEMA_CACHE
    if _SCHEMA_CACHE is None:
        _SCHEMA_CACHE = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    return _SCHEMA_CACHE


def _type_branches(schema: dict) -> dict[str, dict]:
    """Map each record type value -> the schema branch that governs it."""
    props = schema.get("properties", {})
    tspec = props.get("type", {})
    if "anyOf" in schema:
        branches = {}
        for br in schema["anyOf"]:
            val = br.get("properties", {}).get("type", {}).get("const")
            if val:
                branches[val] = br
        if branches:
            return branches
    if tspec.get("const"):
        return {tspec["const"]: schema}
    if tspec.get("enum"):
        return {v: schema for v in tspec["enum"]}
    return {None: schema}


def _entity_rules(branch: dict) -> tuple[list[str], dict[str, set]]:
    """(required entity fields, enum fields -> allowed values) minus admission-assigned."""
    required = [f for f in branch.get("required", []) if f not in ADMISSION_ASSIGNED]
    enums: dict[str, set] = {}
    for fname, fprops in branch.get("properties", {}).items():
        if fname in ADMISSION_ASSIGNED:
            continue
        if isinstance(fprops, dict) and fprops.get("enum"):
            enums[fname] = set(fprops["enum"])
    return required, enums


def validate_queue_file(path: Path, schema: dict) -> list[str]:
    """Return a list of findings for one queue file (empty = valid)."""
    findings: list[str] = []
    rel = path.relative_to(REPO) if path.is_relative_to(REPO) else path
    try:
        entry = yaml.safe_load(path.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:
        return [f"{rel}: not valid YAML ({exc})"]
    if not isinstance(entry, dict):
        return [f"{rel}: top level must be a mapping"]

    if "id" in entry:
        findings.append(
            f"{rel}: submissions must not carry an 'id' — ids are assigned at "
            f"admission (content-derived hash)"
        )
    status = entry.get("status")
    if status not in QUEUE_STATUSES:
        findings.append(f"{rel}: 'status' must be one of {sorted(QUEUE_STATUSES)} (got {status!r})")
    name = entry.get("name")
    if not isinstance(name, str) or not name.strip():
        findings.append(f"{rel}: 'name' is required (non-empty string)")
    desc = entry.get("description")
    if not isinstance(desc, str) or len(desc.strip()) < 40:
        findings.append(f"{rel}: 'description' is required (>= 40 chars; it seeds the entity README)")
    slug = entry.get("slug")
    if slug is not None and (not isinstance(slug, str) or not SLUG_RE.match(slug) or len(slug) > 48):
        findings.append(f"{rel}: optional 'slug' must be lowercase kebab-case, <= 48 chars")

    branches = _type_branches(schema)
    type_values = [k for k in branches if k is not None]
    multi = len(type_values) > 1
    if multi:
        rtype = entry.get("type")
        if rtype not in branches:
            findings.append(f"{rel}: 'type' must be one of {sorted(type_values)} (got {rtype!r})")
            return findings
        branch = branches[rtype]
    else:
        branch = branches[type_values[0]] if type_values else branches[None]

    required, enums = _entity_rules(branch)
    for f in required:
        v = entry.get(f)
        if v is None or (isinstance(v, str) and not v.strip()) or (
            isinstance(v, list) and not v
        ):
            findings.append(f"{rel}: entity field {f!r} is required (per schemas/entity.schema.json)")
    for f, allowed in enums.items():
        if f in entry and entry[f] is not None and entry[f] not in allowed:
            findings.append(
                f"{rel}: entity field {f!r} = {entry[f]!r} not in schema enum {sorted(allowed)}"
            )

    evidence = entry.get("evidence")
    if not isinstance(evidence, dict):
        findings.append(f"{rel}: 'evidence' is required ({'{sources, rationale}'})")
    else:
        sources = evidence.get("sources") or []
        if not isinstance(sources, list) or not sources:
            findings.append(f"{rel}: evidence.sources must be a non-empty list")
        for s in sources:
            if not isinstance(s, dict) or s.get("kind") not in KNOWN_SOURCE_KINDS:
                findings.append(
                    f"{rel}: evidence source kind {s.get('kind')!r} is not known "
                    f"({sorted(KNOWN_SOURCE_KINDS)})"
                )
            elif not isinstance(s.get("reference"), str) or not s["reference"].strip():
                findings.append(f"{rel}: evidence source reference must be a non-empty string")
        if not isinstance(evidence.get("rationale"), str) or len(evidence["rationale"].strip()) < 20:
            findings.append(f"{rel}: evidence.rationale is too thin (>= 20 chars)")

    tags = entry.get("tags", []) or []
    if not isinstance(tags, list) or any(not isinstance(t, str) or not SLUG_RE.match(t) for t in tags):
        findings.append(f"{rel}: 'tags' must be kebab-case tokens")
    return findings


def queue_files() -> list[Path]:
    if not QUEUE.is_dir():
        return []
    return sorted(QUEUE.glob("*.yaml")) + sorted(QUEUE.glob("*/*.yaml"))


def main() -> int:
    schema = load_schema()
    findings: list[str] = []
    files = queue_files()
    for path in files:
        findings.extend(validate_queue_file(path, schema))
    for f in findings:
        print(f"ERROR: {f}")
    print(
        f"Contribution queue (catalog population programme): "
        f"{'CONFORMANT' if not findings else f'{len(findings)} finding(s)'} "
        f"({len(files)} queue file(s))"
    )
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())
