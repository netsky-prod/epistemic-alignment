# Installation

## Install from the public GitHub marketplace

Add the canonical repository as a Codex marketplace:

```sh
codex plugin marketplace add netsky-prod/epistemic-alignment
```

Start Codex, run `/plugins`, choose **Epistemic Alignment**, and install
**Alignment**. Start a new task after installation so the eight
`alignment:*` skills are discovered.

Use the remaining sections only when developing or validating a local checkout.

## Requirements

- Codex desktop with the `codex` CLI available.
- Python 3.9 or newer. The alignment helper uses only the standard library.
- PyYAML 6.0.2 in a separate virtual environment for the plugin-creator
  validator only; it is not a plugin runtime dependency.
- Superpowers installed for the post-approval implementation handoff.
- Node 22.13 or newer and pnpm 11.19 when building the Codex review Site.

Create the reusable validator environment before installing or validating the
plugin. Pinning PyYAML makes the documented validator command reproducible and
keeps the plugin's dependency-free helper environment unchanged.

```sh
validator_venv="$HOME/.cache/epistemic-alignment/plugin-validator-pyyaml-6.0.2"
python3 -m venv "$validator_venv"
"$validator_venv/bin/python" -m pip install --disable-pip-version-check "PyYAML==6.0.2"
```

## Local development installation

Run these commands from a clean checkout. The plugin-creator helper creates the
personal marketplace entry; do not edit `~/.agents/plugins/marketplace.json` or
Codex configuration by hand.

```sh
PLUGIN_CREATOR="$HOME/.codex/skills/.system/plugin-creator"
validator_python="$HOME/.cache/epistemic-alignment/plugin-validator-pyyaml-6.0.2/bin/python"
mkdir -p "$HOME/plugins"
python3 "$PLUGIN_CREATOR/scripts/create_basic_plugin.py" alignment \
  --path "$HOME/plugins" --with-marketplace
cp -R ./. "$HOME/plugins/alignment/"
"$validator_python" "$PLUGIN_CREATOR/scripts/validate_plugin.py" "$HOME/plugins/alignment"
MARKETPLACE_NAME=$(python3 "$PLUGIN_CREATOR/scripts/read_marketplace_name.py")
codex plugin add "alignment@$MARKETPLACE_NAME"
```

The default personal marketplace is discovered automatically. Do not run
`codex plugin marketplace add` for this default path. Start a new Codex task
after installation so the eight `alignment:*` skills are discovered.

For a repo/team marketplace at a non-default path, create the marketplace with
the plugin-creator helper, add its root once with
`codex plugin marketplace add <marketplace-root>`, read its name with
`read_marketplace_name.py --marketplace-path <marketplace.json>`, and install
from that name.

## Development reinstall

Update the installed source copy, then use the cachebuster helper. It preserves
the base version and replaces the single `+codex.<token>` suffix.

```sh
PLUGIN_CREATOR="$HOME/.codex/skills/.system/plugin-creator"
validator_python="$HOME/.cache/epistemic-alignment/plugin-validator-pyyaml-6.0.2/bin/python"
cp -R ./. "$HOME/plugins/alignment/"
python3 "$PLUGIN_CREATOR/scripts/update_plugin_cachebuster.py" \
  "$HOME/plugins/alignment"
"$validator_python" "$PLUGIN_CREATOR/scripts/validate_plugin.py" "$HOME/plugins/alignment"
MARKETPLACE_NAME=$(python3 "$PLUGIN_CREATOR/scripts/read_marketplace_name.py")
codex plugin add "alignment@$MARKETPLACE_NAME"
```

Do not append cachebusters manually and do not increment the public version
only to refresh Codex. Start a new task after each reinstall.

## Removal

Read the personal marketplace name, then uninstall the active plugin:

```sh
PLUGIN_CREATOR="$HOME/.codex/skills/.system/plugin-creator"
MARKETPLACE_NAME=$(python3 "$PLUGIN_CREATOR/scripts/read_marketplace_name.py")
codex plugin remove "alignment@$MARKETPLACE_NAME"
```

This removes the Codex installation without deleting project dossiers or the
local source. Keep the marketplace source until any other installed versions
that depend on it have been removed. Never delete a project `alignment/`
directory as part of plugin removal.
