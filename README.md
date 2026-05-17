# PEtFiSh Market

Community skill marketplace for [PEtFiSh](https://github.com/kylecui/petfish.ai).

Submit skills via PR → automated quality gate → discoverable and installable by the community.

## How It Works

1. **Submit** — Open a PR adding a `skills/<namespace>--<name>.json` metadata file
2. **Validate** — CI clones your skill repo, runs lint + security audit + quality gate
3. **Review** — Maintainers review the PR (human approval required)
4. **Publish** — On merge, your skill appears in `index.json` and becomes discoverable via `/petfish search`

## Install a Community Skill

```bash
# PowerShell
.\install.ps1 -Pack "community/pdf-processor" -Target . -Detect

# Bash
./install.sh --pack community/pdf-processor --target . --detect
```

Or via the agent:
```
/petfish install community/pdf-processor
```

## Submit a Skill

See [CONTRIBUTING.md](CONTRIBUTING.md) for the full submission guide.

### Quick Start

1. Create a skill in your own repo (use `/petfish create <name>` to scaffold)
2. Run `/petfish gate <path>` locally to ensure it passes the quality gate
3. Fork this repo
4. Add `skills/community--<your-skill-name>.json` with your skill metadata
5. Open a PR — CI validates automatically
6. Wait for review and merge

## Quality Requirements

All submissions must pass the PEtFiSh quality gate:

- **Lint score** ≥ 80/100
- **Security risk** ≤ 0.5
- **No CRITICAL** security findings

## Index

The machine-readable skill index is at [`index.json`](index.json). It is auto-generated from individual `skills/*.json` entries on every merge to `main`.

## License

Apache-2.0 — see [LICENSE](LICENSE).

Submitted skills must use Apache-2.0 or a compatible license.
