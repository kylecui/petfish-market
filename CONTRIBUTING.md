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
