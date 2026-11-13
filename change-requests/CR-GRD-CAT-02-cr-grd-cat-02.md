# CR-GRD-CAT-02: Entity Ingestion Groundwork (candidate intake queue + gates)

**Status**: Landed (this PR)
**Layer**: Catalog tooling (intake workflow)
**Owner**: Emmanuel A. Otchere
**Date**: 2026-11-13
**Admission authority**: tooling only (no records are admitted by this CR)
**Trigger**: Catalog population programme (2026-11 owner directive): advance 10 foundational skeleton catalogs with evidence-backed candidate corpora (>=1,000 each) through a gated intake workflow. Guardrails is first: NIST SP 800-53 Rev.5 + published control catalogs are the candidate seed sources named per FOUNDATIONS §7.
**Carrier**: Single PR on feature branch `feat/cr-grd-cat-02`. PR review, not direct push.
**Lands against**: `main`
**Depends on**: the catalogue foundation CR (kit bring-up); dea-metaframework v2.8.0 (released 2026-11-10 — the pin bump satisfies the CR-CATALOG-STRUCT-13 land-then-pin ordering).

## 1. Objective

Stand up the gated intake workflow for the Guardrail candidate corpus (catalog population programme): a contribution queue with a blocking gate and an admission tool that lands records in the CANDIDATE state (`candidates/` subtrees, `lifecycle_status: proposed`, version 0.1.0), leaving canonical admission to the FOUNDATIONS evidence gate (D-4/D-5).

## 2. Changes

1. `scripts/check_contributions.py` — the queue gate (blocking): validates every `contributions/queue/<shard>/<slug>.yaml` submission — no top-level `id` (ids are content-derived at admission), status vocabulary, identity fields, entity required-fields + enum membership derived from `schemas/entity.schema.json`, evidence contract (≥1 source of a known kind with a non-empty reference + ≥20-char rationale). Self-deriving: carries no per-repo constants.
2. `scripts/admit_entity.py` — the admission tool: validates via the queue gate, mints the content-derived id `<prefix>-<slug>-<hash6>` (sha256 mod 31^6 over the intake content; collision-checked), scaffolds `entities/v1-alpha/<shard>/<slug>-<hash>/candidates/` with the record (`version: 0.1.0`, `lifecycle_status: proposed`, governance `approval_status: proposed`, one-step provenance ladder `candidate`, relationships deferred) + the per-record README (RECORD-STANDARD sections), and flips the queue entry to `status: admitted`.
3. `contributions/intake-template.yaml` + `contributions/README.md` — the intake contract and the process (the CR-SVC-004 process, generalized to candidate-state semantics).
4. `.github/workflows/validate-catalogue.yml` — new blocking step: "Run contribution queue gate" (queue gate added to the gate order).
5. **Toolchain modernization (rider)**: metaframework pin `v2.6.0` → `v2.8.0` across the workflows and `dependencies.yaml`; `scripts/regenerate_catalog.py` and `scripts/check_catalog_index.py` re-vendored from dea-metaframework v2.8.0 (the shard-aware toolchain — candidate subtrees sharded under `entities/v1-alpha/<letter>/` at admission; the canonical v2.8.0 `regenerate_catalog.py` receives the documented shard-walk patch (`is_shard_dir` + depth-2 `list_subtrees`, the CR-SVC-016 / CR-MET-024 recipe) so candidate subtrees sharded under `entities/v1-alpha/<letter>/` enumerate; Vendored-copy-is-authoritative (CST-013/014) unchanged — repo-local patch recorded here).
6. CHANGELOG `[Unreleased]` entry and this CR + index row.

## 3. What this CR does NOT do

- No records: the queue ships empty (`check_contributions.py` conforms on an empty queue; `entities/v1-alpha/` untouched).
- No gate-semantics changes: the six existing gates keep their behavior; the queue gate is additive.
- No canonical admissions: even after corpus CRs land, records stay candidate-state until their evidence-gated canonical CRs.

## 4. Verification

1. `check_contributions.py` → CONFORMANT (empty queue).
2. All six existing gates + the new queue gate green locally; `regenerate_catalog.py --check` exit 0 (re-vendored, shard-aware).
3. `admit_entity.py --dry-run` on a sample intake yields a schema-legal record id and no writes.
4. CI green on the PR (workflow diff is the pin bump + the new step).

## 5. Acceptance criteria

1. The queue gate is wired as a blocking CI step and conforms on the empty queue.
2. `admit_entity.py --dry-run` round-trips a sample submission without error.
3. Pins resolve: every advertised metaframework release-tag pin in the workflows exists on origin (v2.8.0, released 2026-11-10).
4. `register_version`/register row untouched; no records admitted.
