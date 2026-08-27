# Qwen Code local-renderer roadmap — future work

No Qwen Code adapter code is shipped in v1. Qwen Code will share the future
local static renderer with OpenCode while keeping its host metadata and launch
guidance distinct.

## Planned extension metadata

```yaml
name: epistemic-alignment-qwen-code
adapter: qwen-code-local-static
contract_version: "1.0"
entrypoint: render-alignment-review
capabilities:
  local_static_preview: true
  mutates_approval_state: false
```

The future Qwen Code extension supplies the renderer-contract input, opens or
reports the local draft URL using Qwen Code's supported extension mechanism,
and returns standard adapter output. The host installation details are future
work pending validation of that extension mechanism.

## Capability check and fallback

The future extension first requires `host_capabilities.local_static_preview ==
true`. There is no permitted fallback within the Qwen Code local-static path.
If the predicate is false, it returns the standard `failed` result (null
location/rendered hash plus a warning) and does not call `issue-review`.

## Planned preview

After the shared future renderer writes `<project>/alignment-review/static/`:

```sh
cd <project>/alignment-review/static
python3 -m http.server 4174
```

This is a local draft preview. It cannot publish, transcribe consent, or change
the thin gate.
