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
  "rendered_hash": "<issued sha256-v1 digest>",
  "warnings": ["A finding remains unresolved"]
}
```

`status` is one of `draft`, `presented`, `published`, or `failed`.
`rendered_hash` must equal the issued snapshot digest before `issue-review` is
called. `warnings` remain visible presentation notes, never a semantic verdict.
The invoking workflow alone decides whether a host has actually presented the
view, and the `approve-handoff` skill alone transcribes an explicit current
human message through the helper.

## Host boundaries

- Codex v1 has the presentational Site template at
  `adapters/codex-site/template/`; it never mutates review state.
- Claude, OpenCode, and Qwen Code documentation below is a roadmap only. No
  production host adapter, semantic parser, or remote integration ships in v1.
- OpenCode and Qwen Code are planned to share one local static renderer, but
  they retain separate extension metadata and host preview instructions.
