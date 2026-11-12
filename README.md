# Avatar Preflight Lab

**An experimental, offline preflight validator for talking-avatar workflows.**

This repository contains working configuration validation and planning code. It
**does not generate speech, animate a face, or provide a replacement for HeyGen**.
It is an early engineering prototype, not a production service or an established
open-source community. Developed with AI assistance; no deployment, users or
research results are claimed.

## Why build this?

A voice + lip-sync pipeline is more than connecting model names. It needs explicit
consent, licensed components, reproducible revisions, compatible hardware and a
human quality check. This tool makes these *declarations* explicit before an
experimental run. It cannot determine whether a statement is truthful or legally
sufficient.

## Try it in a minute

Python 3.10+; no third-party runtime dependencies, GPU, account or model required.

```sh
python -m avatar_plan examples/synthetic_plan.json
python -m unittest discover -s tests -v
```

The example contains **invented paths and component metadata**, no personal media,
no weights, no actual consent record and no measured GPU requirement. It validates
because the declarations are structurally acceptable, not because real inference
is possible. Its result is `declarations_valid`, deliberately not `ready`.

Exit codes: `0` declarations valid; `1` blocked by checks; `2` unreadable/invalid JSON.

## Implemented

- Strict expected fields and finite numeric checks.
- Explicit consent review and synthetic-media disclosure flags.
- Relative media-path format checks (not a filesystem sandbox).
- Offline-only declared configuration.
- Separate commercial-permission and dependency-license review declarations.
- Pinned component revision requirement (not cryptographic verification).
- Declared GPU memory comparison and a 30-second prototype clip limit.
- Dependency check: generated audio needs a voice component; recorded audio does not.
- Machine-readable blocked reasons and a human review plan.
- Unit/CLI tests and a GitHub Actions test workflow.
- Deterministic manifest fingerprints and value-free change review with `--compare`.
- Strict duplicate-key rejection to avoid ambiguous JSON declarations.

## Change review and contribution

See [audit walkthrough](docs/AUDIT.md) for reproducible reports and comparison
semantics, and [contributing](CONTRIBUTING.md) for architecture and starter tasks.

## Not implemented

No model adapter, inference, downloader, network client, media validation,
biometric identity verification, actual license verification, video player or
publishing integration. No inference benchmark has been performed. The CLI does
not inspect the files named by the manifest. It only reads the supplied JSON.

## Architecture

```text
manifest.json → schema + declaration checks → blocked reasons OR review plan
                                                   ↓ future work only
reviewed media → voice adapter (optional) → lip-sync adapter → human QA → export
```

The executable deliberately stops before the lower pipeline. Adding an adapter
requires a separate implementation, dependency/license review and hardware test.

## Research directions

See [model candidates](docs/MODELS.md), [safety and privacy](docs/SAFETY.md),
[manifest reference](docs/MANIFEST.md) and [roadmap](docs/ROADMAP.md).

## License

This repository's original code is MIT licensed. No upstream model code or weights
are included. Their licenses do not become MIT by being mentioned here.
