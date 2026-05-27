# Contributing to PEtFiSh Market

Thank you for sharing your skill with the community!

## Prerequisites

- A working skill in your own GitHub repository
- The skill must pass `run_gate.py` locally (lint ≥ 80, security risk ≤ 0.5, no CRITICAL)
- Apache-2.0 or compatible license

## Submission Steps

### 1. Prepare Your Skill

Ensure your skill repo contains a valid skill at a known path:

```
your-repo/
  .opencode/skills/your-skill-name/
    SKILL.md          # Required
    scripts/           # Optional
    references/        # Optional
    evals/             # Optional
```

Run the quality gate locally:

```bash
uv run .opencode/skills/quality-gate/scripts/run_gate.py --path .opencode/skills/your-skill-name/
```

### 2. Tag a Release

Create a git tag for the version you want to submit:

```bash
git tag v1.0.0
git push origin v1.0.0
```

### 3. Create the Metadata File

Fork this repo and add a file at `skills/community--<your-skill-name>.json`:

```json
{
  "name": "your-skill-name",
  "namespace": "community",
  "display_name": "Your Skill Name",
  "description": "Brief description of what the skill does",
  "version": "1.0.0",
  "author": "your-github-username",
  "repo": "your-github-username/your-repo",
  "ref": "v1.0.0",
  "path": ".opencode/skills/your-skill-name",
  "license": "Apache-2.0",
  "platforms": ["opencode"],
  "dependencies": []
}
```

**Field reference:**

| Field | Required | Description |
|-------|----------|-------------|
| `name` | Yes | Skill name, kebab-case, must match directory name |
| `namespace` | Yes | Must be `community` |
| `display_name` | Yes | Human-readable name |
| `description` | Yes | One-line description (max 200 chars) |
| `version` | Yes | Semantic version (X.Y.Z) |
| `author` | Yes | Your GitHub username |
| `repo` | Yes | `owner/repo` format |
| `ref` | Yes | Git tag or commit SHA |
| `path` | Yes | Path to skill directory within the repo |
| `license` | Yes | SPDX identifier (Apache-2.0, MIT, etc.) |
| `platforms` | Yes | Array of: `opencode`, `claude`, `codex`, `cursor`, `copilot`, `windsurf`, `antigravity`, `universal` |
| `dependencies` | No | Array of other community skill names this depends on |

### 4. Open a PR

Open a pull request. The CI will automatically:

1. Validate your JSON schema
2. Clone your repo at the specified `ref`
3. Verify the skill path exists and contains `SKILL.md`
4. Run the full quality gate (lint + security audit)
5. Post results as a PR comment
6. Label the PR: `gate:pass`, `gate:conditional`, or `gate:fail`

### 5. Review

A maintainer will review your PR. Even if CI passes, human review is required before merge.

## Updating a Skill

To update an existing skill:

1. Push a new tag to your repo
2. Update the `version` and `ref` fields in your `skills/community--<name>.json`
3. Open a PR — CI re-validates against the new version

## Submitting a Pack (Official or Community)

PEtFiSh Market supports a **dual submission model**:

- **`skills/`** — single-skill entries (one JSON per skill, existing model)
- **`registry/`** — pack-level entries (one JSON per pack, containing multiple skills)

### Pack Model Overview

| Type | Directory | Namespace | Who maintains |
|------|-----------|-----------|---------------|
| Official pack | `registry/official/<pack-name>.json` | `official` | petfish team |
| Community pack | `registry/community/<pack-name>.json` | `community` | PR contributors |

### Submitting a Community Pack

1. **Prepare your pack** in your own GitHub repository, tagged at a stable release
2. **Fork this repo** and add a file at `registry/community/<pack-name>.json`
3. **Use the pack registry JSON schema:**

```json
{
  "namespace": "community",
  "name": "your-pack-name",
  "alias": ["short-alias"],
  "description": "Brief description of what the pack contains (bilingual preferred)",
  "repo": "your-github-username/your-repo",
  "ref": "vX.Y.Z",
  "path": "path/to/pack/within/repo",
  "skill_count": 3,
  "license": "Apache-2.0",
  "author": "your-github-username",
  "platforms": ["opencode"],
  "gate_result": {}
}
```

**Field reference:**

| Field | Required | Description |
|-------|----------|-------------|
| `namespace` | Yes | `official` or `community` |
| `name` | Yes | Pack directory name, kebab-case |
| `alias` | Yes | Short install aliases (array) |
| `description` | Yes | One-line description (bilingual preferred) |
| `repo` | Yes | `owner/repo` format |
| `ref` | Yes | Git tag or commit SHA |
| `path` | Yes | Path to pack directory within the repo |
| `skill_count` | Yes | Number of skills in the pack |
| `license` | Yes | SPDX identifier (Apache-2.0, MIT, etc.) |
| `author` | Yes | GitHub username of pack author |
| `platforms` | Yes | Array of: `opencode`, `claude`, `codex`, `cursor`, `copilot`, `windsurf`, `antigravity`, `universal` |
| `gate_result` | Auto | **Leave as `{}`** — CI auto-populates this field |

4. **File naming rule:** `registry/<namespace>/<pack-name>.json`
   - Example: `registry/community/my-data-tools.json`

5. **Open a PR** — CI will automatically:
   1. Validate your JSON schema
   2. Clone your pack repo at the specified `ref`
   3. Verify the path exists in the cloned repo
   4. Run the full quality gate (lint + security audit) on each skill
   5. Auto-populate `gate_result` on pass
   6. Post results as a PR comment and apply `gate:pass/conditional/fail` label

> **Note:** `gate_result` is auto-populated by CI — do not fill it manually in your submission.

### Official Packs

Official packs (in `registry/official/`) are maintained by the petfish team and published with namespace `official`. Community contributors cannot directly add to `registry/official/` — open an issue instead to propose an official pack.

### How Packs Appear in index.json

Pack entries from `registry/official/` and `registry/community/` are included as-is in `index.json` under the `packs[]` array, alongside the existing `skills[]` array.

## Naming Rules

- Skill names must be kebab-case: `my-cool-skill`, not `MyCoolSkill`
- Names must be unique within the `community` namespace
- Don't use names that could be confused with built-in PEtFiSh packs
- Avoid generic names like `utils`, `helper`, `tools`

## Quality Standards

Your skill should:

- Have a clear, specific purpose (not a grab-bag of unrelated features)
- Include meaningful trigger phrases in the SKILL.md description
- Not require secrets or credentials to function
- Not execute arbitrary code from the internet
- Not access the filesystem outside the project directory

## Questions?

Open an issue in this repo or in [petfish.ai](https://github.com/kylecui/petfish.ai/issues).
