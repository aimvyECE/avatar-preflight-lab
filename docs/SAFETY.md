# Safety and privacy boundaries

- Use only your own identity or documented, specific consent from the person shown
  and heard. A boolean field cannot create or prove consent.
- Do not use this research to impersonate someone deceptively, bypass identity
  checks, harass, defraud or create unauthorized intimate material.
- Disclose synthetic media appropriately to the audience and publishing platform.
- Keep consent documents and source recordings outside the repository; example
  directories are ignored by Git, but `.gitignore` is not a confidentiality guarantee.
- Do not commit secrets, raw biometric media, customer documents or identifiable
  recordings. Review every change before publication.
- `network_allowed: false` is a declaration. This package makes no network calls,
  but cannot stop unrelated software from accessing the network.
- Relative path checks are not a security sandbox. A future runner must handle
  symlinks, real paths, output permissions and process/network isolation separately.
- A license review checkbox is not legal advice or verification. Approval to use a
  model does not automatically authorize a face, voice, soundtrack or dataset.
- Real exports require human checks: identity fidelity, pronunciation, lip timing,
  face artifacts, misleading context and disclosure.

This is a personal engineering prototype. It has not undergone independent
security review or production validation.
