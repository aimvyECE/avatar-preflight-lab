# Change-aware review invalidation

A valid JSON plan is not a lasting approval. Replacing audio after someone has
reviewed a clip can make that review stale even if every boolean is still `true`.
The `--compare` report now follows a conservative dependency graph and explains
which reviews need repeating without printing changed values.

```sh
python -m avatar_plan examples/changed_audio_plan.json --compare examples/synthetic_plan.json
```

The synthetic example changes the declared audio path. The report invalidates
consent, voice, lip-sync, human QA and disclosure reviews. Licensing and runtime
are labelled *unaffected*, never approved. Only paths and review categories are
included in the comparison. The ordinary declaration checks still run.

## Policy

- Subject changes → consent → voice/lip-sync → human QA → disclosure.
- Audio changes → consent and voice; visual reference changes → consent/lip-sync.
- Runtime or duration changes → runtime → voice/lip-sync → human QA → disclosure.
- Component changes → license, runtime and voice checks, then downstream reviews.
- Disclosure-only changes invalidate only disclosure review.
- Unknown or whole-document changes invalidate every review (fail closed).

This is a deliberately over-conservative heuristic, not a model execution DAG or
security boundary. For example, a recorded-audio workflow still gets a voice
review category. It does not store actual approvals, inspect media, authenticate
reviewers, verify consent, or block a downstream tool from running. A future
integration must bind reviewer attestations to immutable artifact hashes and
revocation state. No novelty, measured time saving or legal sufficiency is claimed.
