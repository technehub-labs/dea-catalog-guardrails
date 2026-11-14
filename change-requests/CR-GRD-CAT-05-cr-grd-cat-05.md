# CR-GRD-CAT-05: Guardrail Candidate Admission Batch 02 (PE-3.6 — Facility Penetration Testing … SR-9 — Tamper Resistance and Detection)

**Status**: Landed (this PR)
**Layer**: Catalog content (candidate corpus admission)
**Owner**: Emmanuel A. Otchere
**Date**: 2026-11-13
**Admission authority**: candidate corpus only (canonical admission remains the evidence-gated step; FOUNDATIONS D-5)
**Trigger**: catalog population programme (2026-11 directive). This CR is one batch of the approved programme, executed through the gated intake workflow (queue gate → admission tool → catalog gates). Prepared by the authoring agent under eaojnr's direction; authorship of record per the Authorship Cardinal Rule (CR-BP-118).
**Carrier**: Single PR on feature branch `feat/cr-grd-cat-05`. PR review, not direct push.
**Lands against**: `main`
**Depends on**: the ingestion groundwork CR (intake machinery), the candidate corpus CR (queue population).

## 1. What this CR admits

596 new `Guardrail` CANDIDATE records, admitted from `contributions/queue/` by `scripts/admit_entity.py`:

| Type | Admitted |
|---|---|
| Guardrail | 596 |

Each admission: id assigned by the content-derived hash (collision-checked against all record ids), entity subtree `entities/v1-alpha/<shard>/<slug>-<hash>/candidates/` (sharded per entity-storage-layout §4) carrying the record (`version: 0.1.0`, `lifecycle_status: proposed`) + per-record README (RECORD-STANDARD sections), queue entry flipped to `status: admitted` with `assigned_id`. Evidence sources are cited per record (`published-document` references from the corpus bank manifest); governance `approval_status: proposed` and a one-step provenance ladder (`candidate`) — honest pre-admission semantics. Relationships are deferred with an explicit README note (no canonical target ids are asserted at candidate state).

## 2. What changes

- `596` entity subtrees under `entities/v1-alpha/<shard>/` (PE-3.6 — Facility Penetration Testing … SR-9 — Tamper Resistance and Detection)
- `596` queue files moved to `status: admitted` with `assigned_id` + date
- `CATALOG.yaml` regenerated (candidates count +596; canonical count unchanged)
- This CR file, CHANGELOG entry, and index row

## 3. Verification

- `check_contributions.py`: CONFORMANT (queue valid post-admission)
- `check_record_posture.py` / `check_schema.py` / `check_record_documentation.py`: CONFORMANT over the full tree (candidates included)
- `regenerate_catalog.py --check`: CATALOG.yaml current
- CI green on the landing PR

## 4. NOT-List

- NOT canonical admission: records stay candidate-state (`lifecycle_status: proposed`, version 0.1.0, in `candidates/`); the canonical counter is unchanged.
- NOT a change to gates, schemas, or the intake tooling (groundwork CR artifacts untouched).
- NOT a relationship assertion (explicitly deferred in each record README).
- NOT a release/tag action.

## 5. Acceptance criteria

1. `CATALOG.yaml` `counts.candidates` increases by exactly 596; `counts.canonical` unchanged.
2. All 596 queue files carry `status: admitted` and a recorded `assigned_id`.
3. All repo gates green on the landing PR.
