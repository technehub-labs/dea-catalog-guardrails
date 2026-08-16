# dea-catalog-guardrails

> DEA catalog for **Guardrail** — OpenDEAM v0.4.0 (ADR-0004; renamed from `dea-catalog-standards`).

## Guardrail (`GRD`)

- **Entity id:** `dea:entity-guardrail`
- **Allocation:** L2 · L2-rules-guidance
- **Status:** planned

An enforceable constraint on technology or solution choices. Carries an
enforcement maturity level (`advisory | automated-warn | automated-block |
platform-enforced`) — policy-as-code / platform-guardrail practice rather than
a static compliance document. Renamed from **Standard** in v0.4.0 (ADR-0004 D4).

## Relationships (from the OpenDEAM model)

- **TNT → GRD** — informs (dependency, 0..N:0..N)
- **GRD → CTL** — implements (realization, 0..N:1)
- **GRD → TEC** — governs (governance, 0..N:0..N)
- **GRD → SC** — governs (governance, 0..N:0..N)

## Allocation contract

This repo's `metamodel-pointer.yaml` is validated in CI against the pinned
OpenDEAM root model (`v0.4.0`) via the reusable
`validate-against-model.yml` workflow. Drift fails CI.

Content (entity instances) lands when the entity promotes from
`planned` to `scaffold` per the model lifecycle.

## License

Apache 2.0 — see [LICENSE](./LICENSE) and [NOTICE](./NOTICE).
