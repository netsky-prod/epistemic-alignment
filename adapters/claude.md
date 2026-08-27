# Claude Artifact adapter roadmap — future work

No Claude adapter code is shipped in v1. This roadmap is concrete enough to
implement later without changing the canonical dossier or thin gate.

1. Add an Artifact entry point that accepts exactly the v1 renderer-contract
   input and reads only the declared snapshot paths plus `review.md`.
2. Render the seven dossier views with source references, uncertainty labels,
   findings, and the supplied snapshot hash.
3. Return the contract output with `adapter: "claude-artifact"`, an Artifact
   reference in `location`, a truthful status, the supplied rendered hash, and
   visible warnings.
4. Keep the Artifact display-only: no approval control, no direct
   `review-state.json` mutation, and no finding-resolution claim.
5. Test draft and presented states using static fixtures before any host
   installation or publishing workflow is proposed.

## Capability check and fallback

Before invoking the future Artifact entry point, require
`host_capabilities.artifact == true`. There is no permitted fallback for the
Claude Artifact path in v1. If it is unavailable, return the contract's
`failed` result with null location/rendered hash and a warning; do not call
`issue-review`.

The host conversation remains the place for an explicit human decision; the
existing helper remains the only gate writer.
