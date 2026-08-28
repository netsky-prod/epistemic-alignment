# Installed resources

The target project and installed plugin are different roots. Never assume the target project contains this plugin's `scripts/`, `references/`, `adapters/`, or `skills/`.

Resolve the absolute path of the active `SKILL.md`. Its directory is `<plugin-root>/skills/<skill-name>/`, so the plugin root is two directories above that skill directory. Keep these values separate:

```text
ALIGNMENT_PLUGIN_ROOT=<absolute installed plugin root>
ALIGNMENT_HELPER=<ALIGNMENT_PLUGIN_ROOT>/scripts/alignment  # exact-snapshot mode only
PROJECT_ROOT=<absolute target project root>
```

When the process contract selects exact-snapshot binding, verify the helper exists and run `"$ALIGNMENT_HELPER" --version` before its first use. Invoke every helper command through this resolved absolute path and quote both paths, for example:

```sh
"$ALIGNMENT_HELPER" snapshot "$PROJECT_ROOT" --json
```

Conversational binding does not invoke snapshot/decision/check/handoff helper commands. It may still use the initializer if desired, or copy the human-readable templates directly without overwriting existing files.

Resolve shared references and presentation templates from `ALIGNMENT_PLUGIN_ROOT`. Write generated dossier and Site files only under `PROJECT_ROOT`. If the host does not expose the loaded skill path, locate the plugin through the host's installed-plugin inventory; never guess a cache path or copy bundled tooling into the target repository.
