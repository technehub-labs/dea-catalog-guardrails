# Contributions — gated intake (Guardrail)

This catalog ingests candidate records through a queue with two gates:

1. **Queue gate** — `scripts/check_contributions.py` runs in CI on every PR
   touching `contributions/queue/`. It validates the submission shape: no
   hand-invented `id` (ids are content-derived at admission), queue status
   vocabulary, identity fields, entity fields against
   `schemas/entity.schema.json` (required set + enums), evidence contract
   (>= 1 source of a known kind with a non-empty reference + rationale).
2. **Admission** — a maintainer runs
   `python scripts/admit_entity.py contributions/queue/<shard>/<slug>.yaml`
   on the PR branch: it mints the content-derived id
   `<prefix>-<slug>-<hash6>` (collision-checked), scaffolds the entity
   subtree `entities/v1-alpha/<shard>/<slug>-<hash>/candidates/` with the
   record (`version: 0.1.0`, `lifecycle_status: proposed`) and the per-record
   README, and flips the queue entry to `status: admitted`.

## Process

1. Copy `intake-template.yaml` to `contributions/queue/<shard>/<slug>.yaml`
   (shard = first character of the slug; `0-9` fallback).
2. Fill in the fields. Evidence must cite a verifiable published source
   (`repository-path`, `system-of-record`, or `published-document`).
3. Open a PR. The queue gate runs in CI.
4. A maintainer admits via `scripts/admit_entity.py`, then the batch
   admission CR regenerates `CATALOG.yaml` (the `candidates` counter grows)
   and records the change.
5. Canonical admission is a separate, evidence-gated step (FOUNDATIONS D-4/D-5):
   candidates sit at `lifecycle_status: proposed` / version 0.1.0 in
   `candidates/` subtrees; `approval_status: proposed`; relationships are
   deferred with an explicit README note until canonical admission asserts
   them against canonical targets.

No bot moves entries between statuses; the tools only act when a maintainer
runs them, and every admission lands through PR review (no direct pushes to
`main`).
