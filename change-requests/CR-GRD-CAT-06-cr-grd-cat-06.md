# CR-GRD-CAT-06: Canonical Admission Wave (1196 Guardrail records)

**Status**: Landed (this PR)
**Layer**: Catalog content (canonical admission)
**Owner**: Emmanuel A. Otchere
**Date**: 2026-11-15
**Admission authority**: yes (evidence-gated canonical admission — every promoted record carries verifiable published-document sources recorded at candidate admission, per FOUNDATIONS D-4/D-5)
**Trigger**: Catalog population programme, promotion wave (2026-11 owner directive: advance the skeleton catalogs to full population, promoting the admitted candidate corpora through the evidence gates with the abstraction's provenance linked to its evidence).
**Carrier**: Single PR on feature branch `feat/cr-grd-cat-06`. PR review, not direct push.
**Lands against**: `main`
**Depends on**: the candidate corpus + batch admission CRs of this catalogue's programme series.

## 1. What this CR admits

**1196 Guardrail records promoted from the candidate slot to the CANONICAL slot** (`candidates/` -> subtree root), completing the provenance ladder per record:

- `lifecycle_status: active`; `metadata.status: active`
- `governance.approval_status: approved` + `review_date`
- `provenance.ladder_passage` completed: candidate (preserved from admission) -> corroborated -> reviewed -> canonical (each stage dated, actor of record per the Authorship Cardinal Rule)
- evidence sources untouched — every record keeps the `published-document` citation recorded at admission (the abstraction's link to its evidence)
- record ids untouched (assignment-once, rename-stable); the intake queue machinery stays live for future submissions

## 2. What changes

- `1196` record files move from `candidates/` to the canonical subtree root; READMEs move alongside
- `CATALOG.yaml` regenerated: `canonical: 1196`, `candidates: 0`
- This CR file, CHANGELOG entry, and index row

## 3. Verification

- All gates green: posture / queue / schema / documentation / index `--strict` / `regen --check`
- Every promoted record carries >=1 published-document evidence source (admission-time citations preserved verbatim)

## 4. NOT-List

- No new records; no id changes; no relationship assertions beyond the deferred notes (per-record relationship binding remains follow-up work).
- No gate-semantics changes.
- No release/tag action.
