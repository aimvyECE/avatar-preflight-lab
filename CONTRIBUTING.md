# Contributing

Start with Python 3.10+ and `python -m unittest discover -s tests -v`. No model,
GPU, account or network access is required. Run the synthetic CLI example from the
README before changing behavior.

## Architecture

- `core.py`: declaration validation and human review plan.
- `audit.py`: deterministic manifest fingerprints and value-free change paths.
- `__main__.py`: strict JSON loading, CLI interface and exit codes.

A useful pull request includes the failure case, a small fix, regression tests,
and updated documentation for any behavior change. Keep input/output examples
synthetic. Do not add real consent forms, personal recordings or credentials.

Good first contributions: malformed-input regression tests, clearer field-level
errors, or documentation examples for recorded-audio plans. Discuss schema changes
before implementation. A generation adapter is a separate research task requiring
license review and actual hardware benchmarks, not just a model name in JSON.

Do not claim that validation guarantees consent, safety, legal compliance or GPU
compatibility. Review upstream licenses independently. Disclose material AI
assistance and explain how you checked the result. Contributions are welcome; no
response-time or support commitment is promised by this prototype.
