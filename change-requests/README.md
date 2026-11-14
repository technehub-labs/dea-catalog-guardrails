# Change Requests: dea-catalog-guardrails

This index tracks every change request that lands on this repository.

| CR | Title | Status | Notes |
|----|-------|--------|-------|
| [CR-GRD-CAT-01](CR-GRD-CAT-01-catalogue-foundation.md) | Catalogue foundation (kit bring-up) | Landed (this PR) | Standard kit: pointer, dependencies, schema projection, gates 1-6, workflows, FOUNDATIONS, record standard. No records admitted. |
| CR-GRD-CAT-02 | Initial population | Planned | Evidence-gated seed population per FOUNDATIONS §7. |

## Numbering

Series tag `CR-GRD-CAT-NN`, sequential. Cross-repo CRs that touch this
repository are recorded here with their home-repo identifier.
| [CR-GRD-CAT-02](CR-GRD-CAT-02-cr-grd-cat-02.md) | Entity Ingestion Groundwork (candidate intake queue + gates) | **Proposed (this PR)** | Gated intake: queue + blocking queue gate + admission tool (candidate-state subtrees, content-derived ids); pin v2.6.0→v2.8.0 + shard-aware toolchain re-vendor. No records. |
| [CR-GRD-CAT-02](CR-GRD-CAT-02-cr-grd-cat-02.md) | Entity Ingestion Groundwork (candidate intake queue + gates) | **Proposed (this PR)** | Gated intake: queue + blocking queue gate + admission tool (candidate-state subtrees, content-derived ids); pin v2.6.0→v2.8.0 + shard-aware toolchain re-vendor. No records. |
| [CR-GRD-CAT-02](CR-GRD-CAT-02-cr-grd-cat-02.md) | Entity Ingestion Groundwork (candidate intake queue + gates) | **Proposed (this PR)** | Gated intake: queue + blocking queue gate + admission tool (candidate-state subtrees, content-derived ids); pin v2.6.0→v2.8.0 + shard-aware toolchain re-vendor. No records. |
| [CR-GRD-CAT-02](CR-GRD-CAT-02-cr-grd-cat-02.md) | Entity Ingestion Groundwork (candidate intake queue + gates) | **Proposed (this PR)** | Gated intake: queue + blocking queue gate + admission tool (candidate-state subtrees, content-derived ids); pin v2.6.0→v2.8.0 + shard-aware toolchain re-vendor. No records. |
| [CR-GRD-CAT-03](CR-GRD-CAT-03-cr-grd-cat-03.md) | Guardrail Candidate Corpus (NIST SP 800-53 Rev.5) | **Landed (this PR)** | 1,196 queue submissions from the NIST SP 800-53 Rev.5 OSCAL catalog (controls + enhancements; published prose + evidence citations + source_refs; manifest with sha256). Queue gate CONFORMANT; no entities change. |
| [CR-GRD-CAT-04](CR-GRD-CAT-04-cr-grd-cat-04.md) | Guardrail Candidate Admission Batch 01 (PE-3.6 — Facility Penetration Testing … SI-20 — Tainting) | **Landed (this PR)** | Admitted 500 `Guardrail` CANDIDATE records via the gated intake workflow (queue gate → admission tool → catalog gates); candidates +500, canonical unchanged; records at `lifecycle_status: proposed` in `candidates/` subtrees. |
| [CR-GRD-CAT-05](CR-GRD-CAT-05-cr-grd-cat-05.md) | Guardrail Candidate Admission Batch 02 (PE-3.6 — Facility Penetration Testing … SR-9 — Tamper Resistance and Detection) | **Landed (this PR)** | Admitted 596 `Guardrail` CANDIDATE records via the gated intake workflow (queue gate → admission tool → catalog gates); candidates +596, canonical unchanged; records at `lifecycle_status: proposed` in `candidates/` subtrees. |
