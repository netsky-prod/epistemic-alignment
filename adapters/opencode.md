# OpenCode local-renderer roadmap — future work

No OpenCode adapter code is shipped in v1. It will use the future shared local
static renderer described by `adapters/adapter-contract.md`, not a semantic
parser or a second approval implementation.

## Planned extension metadata

```yaml
name: epistemic-alignment-opencode
adapter: opencode-local-static
contract_version: "1.0"
entrypoint: render-alignment-review
capabilities:
  local_static_preview: true
  mutates_approval_state: false
```

The extension will map OpenCode's command/skill registration to the renderer
input and return the standard adapter output. Installation packaging, command
syntax, and host API calls remain future work until OpenCode's extension API is
validated.

## Capability check and fallback

The future extension first requires `host_capabilities.local_static_preview ==
true`. There is no permitted fallback within the OpenCode local-static path.
If the predicate is false, it returns the standard `failed` result (null
location/rendered hash plus a warning) and does not mutate decision state.

## Planned preview

After a future renderer writes `<project>/alignment-review/static/`, preview
only the generated output:

```sh
cd <project>/alignment-review/static
python3 -m http.server 4173
```

The local URL is a draft reference, not proof of presentation or approval.
