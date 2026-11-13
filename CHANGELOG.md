# Changelog

## [Unreleased]

### CR-GRD-CAT-04: Guardrail Candidate Admission Batch 01

Admitted 500 new `Guardrail` CANDIDATE records through the gated intake workflow (queue gate → admission tool → catalog gates); ids content-derived and collision-checked; records land in `candidates/` subtrees at `lifecycle_status: proposed` / version 0.1.0; candidates count +500, canonical unchanged; queue entries flipped to `admitted`.

### CR-GRD-CAT-03: Guardrail Candidate Corpus (NIST SP 800-53 Rev.5)

1,196 Guardrail candidate submissions landed in the contribution queue (sharded, gate-CONFORMANT) from the NIST SP 800-53 Rev.5 OSCAL catalog — 324 controls + 872 enhancements, each carrying its published statement/guidance prose, a published-document evidence citation, and a source_ref control identifier. Provenance recorded in ingestion/manifest.yaml (bank sha256, source URL). enforcement/domain mappings are provisional (documented, subject to canonical-admission review). No catalog entities change in this CR; admission follows in CR-GRD-CAT-04/05.

### CR-GRD-CAT-02: Entity Ingestion Groundwork (candidate intake queue + gates)

Gated intake workflow stood up: contribution queue + blocking queue gate (`scripts/check_contributions.py`, self-deriving from the projected schema) + admission tool (`scripts/admit_entity.py`: content-derived ids, collision-checked, candidates/ subtrees at `lifecycle_status: proposed` / v0.1.0) + intake template and process docs. CI: queue gate added as a blocking step; metaframework pin v2.6.0 → v2.8.0 with the shard-aware toolchain re-vendored from the v2.8.0 release (cmp'd). No records admitted by this CR.

### CR-GRD-CAT-02: Entity Ingestion Groundwork (candidate intake queue + gates)

Gated intake workflow stood up: contribution queue + blocking queue gate (`scripts/check_contributions.py`, self-deriving from the projected schema) + admission tool (`scripts/admit_entity.py`: content-derived ids, collision-checked, candidates/ subtrees at `lifecycle_status: proposed` / v0.1.0) + intake template and process docs. CI: queue gate added as a blocking step; metaframework pin v2.6.0 → v2.8.0 with the shard-aware toolchain re-vendored from the v2.8.0 release (cmp'd). No records admitted by this CR.

### CR-GRD-CAT-02: Entity Ingestion Groundwork (candidate intake queue + gates)

Gated intake workflow stood up: contribution queue + blocking queue gate (`scripts/check_contributions.py`, self-deriving from the projected schema) + admission tool (`scripts/admit_entity.py`: content-derived ids, collision-checked, candidates/ subtrees at `lifecycle_status: proposed` / v0.1.0) + intake template and process docs. CI: queue gate added as a blocking step; metaframework pin v2.6.0 → v2.8.0 with the shard-aware toolchain re-vendored from the v2.8.0 release (cmp'd). No records admitted by this CR.

### CR-GRD-CAT-02: Entity Ingestion Groundwork (candidate intake queue + gates)

Gated intake workflow stood up: contribution queue + blocking queue gate (`scripts/check_contributions.py`, self-deriving from the projected schema) + admission tool (`scripts/admit_entity.py`: content-derived ids, collision-checked, candidates/ subtrees at `lifecycle_status: proposed` / v0.1.0) + intake template and process docs. CI: queue gate added as a blocking step; metaframework pin v2.6.0 → v2.8.0 with the shard-aware toolchain re-vendored from the v2.8.0 release (cmp'd). No records admitted by this CR.

### `CR-GRD-CAT-01` — catalogue foundation (kit bring-up)

Standard kit generated from the metamodel (org-wide catalog advancement
programme): hybrid pointer pinned to OpenDEAM v0.8.0;
`dependencies.yaml`; schema projection (copied-and-narrowed) with the
catalogue-instance layer; vendored relationship-instance contract; fixtures;
gates 1-6 wired into `validate-catalogue.yml` plus allocation and authorship
workflows; FOUNDATIONS (D-1..D-6) and record documentation standard. No
records admitted (population gated on CR-GRD-CAT-02).
