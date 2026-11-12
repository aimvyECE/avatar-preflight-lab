# Manifest version 1

All fields in the sample are required; extra fields are rejected to catch typos.

- `schema_version`: integer `1`.
- `purpose`: `personal` or `commercial`.
- `subject.consent_record`: relative path pointing to intended consent documentation.
- `subject.consent_reviewed`: explicit boolean `true`.
- `subject.synthetic_disclosure`: explicit boolean `true`.
- `media.reference_video`, `media.audio`: relative POSIX-style file paths, not URLs.
- `media.duration_seconds`: positive finite number, maximum 30 for this prototype.
- `media.audio_origin`: `recorded` or `generated`.
- `runtime.network_allowed`: boolean `false`.
- `runtime.gpu_memory_gib`: positive finite declared available GPU memory.
- `components`: exactly one `lipsync`; add exactly one `voice` for generated audio.
- Component `name`, `revision`: nonempty strings. Moving `main/latest/master` revisions rejected.
- Component `model_path`: relative path, not downloaded or opened.
- Component `license_reviewed`: boolean `true`, covering code, weights and dependencies.
- Component `commercial_use_allowed`: boolean; must be true for commercial plans.
- Component `tested_gpu_memory_gib`: declared memory associated with the selected configuration;
  must not exceed declared available memory. No automatic benchmarking is performed.

These checks are necessary conventions for this prototype, not sufficient
conditions for legal, safe or successful generation. The sample's values are
illustrative and do not describe a real model benchmark.
