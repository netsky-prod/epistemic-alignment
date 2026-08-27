# Renderer adapter contract (v1)

This is a renderer-only contract. It carries an already authored dossier and
its human semantic review to a host presentation. It does not parse dossier
semantics, decide whether findings are acceptable, transcribe a human decision,
or write approval state.

## Input

The invoking skill supplies this JSON-compatible object after it has read the
canonical documents:

```json
{
  "contract_version": "1.0",
  "dossier_path": "<project>/alignment",
  "snapshot_paths": ["charter.md", "review.md"],
  "snapshot": {"algorithm": "sha256-v1", "digest": "<64 hex>"},
  "semantic_review_path": "<project>/alignment/review.md",
  "host_capabilities": {
    "artifact": false,
    "local_static_preview": false,
    "sites": false
  }
}
```

`snapshot_paths` and `snapshot` are supplied by the thin helper. The adapter
may render source text and the human-authored review, but must leave them
unchanged. A host capability is descriptive; it grants neither publishing nor
approval permission.

## Output

The adapter returns one JSON-compatible result:

```json
{
  "adapter": "codex-sites",
  "version": "1.0",
  "location": "site://draft-or-host-reference",
  "status": "draft",
  "rendered_hash": "<input snapshot sha256-v1 digest>",
  "warnings": ["A finding remains unresolved"]
}
```

`status` is one of `draft`, `presented`, `published`, or `failed`.
`warnings` remain visible presentation notes, never a semantic verdict.

## Capability predicates and fallbacks

The invoking skill evaluates a capability predicate before asking a renderer
to create a presentation:

| Adapter path | Required predicate | Permitted fallback |
| --- | --- | --- |
| Codex Site | `host_capabilities.sites == true` | A local draft only if the caller explicitly selects a local-static adapter and `local_static_preview == true`. |
| Claude Artifact | `host_capabilities.artifact == true` | None in v1. |
| OpenCode/Qwen local static | `host_capabilities.local_static_preview == true` | None in v1. |

When the required capability is false and no permitted fallback is selected,
the adapter result is a failure record. It must contain a warning and must not
start review issuance:

```json
{
  "adapter": "requested-adapter",
  "version": "1.0",
  "location": null,
  "status": "failed",
  "rendered_hash": null,
  "warnings": ["Required host capability is unavailable; no permitted fallback was selected."]
}
```

This failure result performs no rendering, no state mutation, and no issue-review call.
A capability grants neither publishing nor approval permission.

## Snapshot binding and issuance

Before `issue-review`, compute a fresh current snapshot, render only its listed
paths, and require the adapter's `rendered_hash` to equal that input snapshot
digest. There is no pre-existing issued digest requirement: issuance is what
records the first issued digest. Immediately after `issue-review`, recheck that
the current, issued, and rendered hashes are equal; if they diverge, do not
record a human decision and return to review. The invoking workflow alone
decides whether a host has actually presented the view, and the
`approve-handoff` skill alone transcribes an explicit current human message
through the helper.

## Host boundaries

- Codex v1 has the presentational Site template at
  `adapters/codex-site/template/`; it never mutates review state.
- Claude, OpenCode, and Qwen Code documentation below is a roadmap only. No
  production host adapter, semantic parser, or remote integration ships in v1.
- OpenCode and Qwen Code are planned to share one local static renderer, but
  they retain separate extension metadata and host preview instructions.
