# PEtFiSh Market

Community marketplace for [PEtFiSh](https://github.com/kylecui/petfish.ai) skills and packs.

Submit skills or packs via PR → automated quality gate → discoverable and installable by the community.
（通过 PR 提交 skill 或 pack → 自动质量门禁 → 社区可发现、可安装）

## How It Works

1. **Submit** — Open a PR adding a metadata JSON file in `skills/` (single skill) or `registry/` (pack)
2. **Validate** — CI clones your repo at the specified `ref`, runs lint + security audit + quality gate
3. **Review** — Maintainers review the PR (human approval required)
4. **Publish** — On merge, your skill or pack appears in `index.json` and becomes discoverable via `/petfish search`

## Dual Submission Model

PEtFiSh Market supports two submission types:

| Type | Directory | Use when |
|------|-----------|----------|
| **Single skill** | `skills/community--<name>.json` | Submitting one standalone skill |
| **Pack** | `registry/community/<pack-name>.json` | Submitting a collection of related skills |

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

## Install a Community Pack

```bash
# PowerShell
.\install.ps1 -Pack "community/my-data-tools" -Target . -Detect

# Bash
./install.sh --pack community/my-data-tools --target . --detect
```

Or via the agent:
```
/petfish install community/my-data-tools
```

## Submit a Skill or Pack

See [CONTRIBUTING.md](CONTRIBUTING.md) for the full submission guide.

### Quick Start: Single Skill

1. Create a skill in your own repo (use `/petfish create <name>` to scaffold)
2. Run `/petfish gate <path>` locally to ensure it passes the quality gate
3. Fork this repo
4. Add `skills/community--<your-skill-name>.json` with your skill metadata
5. Open a PR — CI validates automatically
6. Wait for review and merge

### Quick Start: Pack

1. Organize your skills as a pack in your own repo
2. Run `/petfish gate <pack-path>` locally
3. Fork this repo
4. Add `registry/community/<your-pack-name>.json` with pack metadata
5. Open a PR — CI validates automatically
6. Wait for review and merge

## Registry Structure

```
registry/
  official/    # Official packs maintained by the petfish team
  community/   # Community-submitted packs (via PR)
```

Official packs (`registry/official/`) are published by the petfish team with namespace `official`. Community packs (`registry/community/`) are submitted by contributors via PR with namespace `community`.

## Quality Requirements

All submissions (skills and packs) must pass the PEtFiSh quality gate:

- **Lint score** ≥ 80/100
- **Security risk** ≤ 0.5
- **No CRITICAL** security findings

## Index

The machine-readable index is at [`index.json`](index.json). It is auto-generated from:

- `skills/*.json` → appears in the `skills[]` array
- `registry/official/*.json` + `registry/community/*.json` → appears in the `packs[]` array

The index schema (v2):
```json
{
  "version": 2,
  "generated_at": "ISO-8601",
  "skill_count": N,
  "pack_count": M,
  "skills": [...],
  "packs": [...]
}
```

The index is regenerated automatically on every merge to `main` that touches `skills/*.json` or `registry/**/*.json`.

## License

Apache-2.0 — see [LICENSE](LICENSE).

Submitted skills and packs must use Apache-2.0 or a compatible license.
