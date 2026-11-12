# Review changes before running an adapter

The CLI now attaches a deterministic SHA-256 fingerprint to every parsed manifest,
including blocked plans. JSON key order and whitespace do not affect the hash.
Numeric spellings such as `1` and `1.0` can differ. This is a project-specific
canonical representation, not an implementation of RFC 8785.

```sh
python -m avatar_plan examples/synthetic_plan.json > audit.json
python -m avatar_plan examples/synthetic_plan.json --compare examples/synthetic_plan.json
```

The second command has no changes. To exercise review, copy the synthetic example
locally, change `media.audio` to `media/revised.wav`, then compare it to the original.
`comparison.changed_paths` will include `/media/audio` and `review_required` will
be true. Changing consent to false still blocks the plan; a hash never overrides
validation. A previous manifest is checked independently and its status is shown.

## Semantics and limitations

- Paths use JSON Pointer escaping. Arrays are compared by position, not role.
- Comparisons omit values, but field names can themselves be sensitive. Reports
  are local artifacts, **not automatically safe to publish**.
- The report contains no timestamp, randomness or network result, so identical
  inputs give identical reports under the same tool version.
- Hashes identify content; they do not prove authorship, consent or integrity of
  referenced files. This tool does not open those files or sign anything.
- Duplicate JSON keys and nonstandard NaN/Infinity constants are rejected rather
  than silently overriding declarations.
- Exit 0 means structurally valid declarations, not unchanged configuration.
  Consumers must separately inspect `review_required`.

For real review, retain the tool commit, manifest and report in a private evidence
store. Consent documents, media and private manifests must not be committed here.
