# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
"""PEtFiSh Market CLI — Contributor workflow tool.

Usage:
    uv run market.py validate <path>     # Validate a skill/pack locally
    uv run market.py list                # List all market skills/packs
    uv run market.py init <name>         # Scaffold a skill metadata JSON
    uv run market.py check <path>        # Pre-submission readiness check
    uv run market.py index               # Regenerate index.json from registry

This CLI lives in the petfish-market repo and provides a smooth contributor
experience for submitting skills and packs.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


MARKET_ROOT = Path(__file__).resolve().parent
SKILLS_DIR = MARKET_ROOT / "skills"
REGISTRY_DIR = MARKET_ROOT / "registry"
INDEX_PATH = MARKET_ROOT / "index.json"


# ---------------------------------------------------------------------------
# validate — run quality checks on a local skill/pack
# ---------------------------------------------------------------------------

def cmd_validate(args: argparse.Namespace) -> int:
    """Validate a skill or pack directory for market submission readiness."""
    path = Path(args.path).resolve()
    if not path.is_dir():
        print(f"Error: {path} is not a directory", file=sys.stderr)
        return 1

    skill_md = path / "SKILL.md"
    manifest = path / "pack-manifest.json"

    issues: list[str] = []
    warnings: list[str] = []

    # Check SKILL.md exists
    if not skill_md.is_file():
        issues.append("Missing SKILL.md — every skill must have one")
    else:
        content = skill_md.read_text(encoding="utf-8")
        # Check frontmatter
        fm_match = re.match(r"^---\s*\n(.*?)\n---", content, re.DOTALL)
        if not fm_match:
            issues.append("SKILL.md missing YAML frontmatter (--- ... ---)")
        else:
            fm = fm_match.group(1)
            if "name:" not in fm:
                issues.append("SKILL.md frontmatter missing 'name' field")
            if "description:" not in fm:
                issues.append("SKILL.md frontmatter missing 'description' field")
            # Check description length
            desc_match = re.search(r"description:\s*[\"']?(.*?)[\"']?\s*$", fm, re.MULTILINE)
            if desc_match:
                desc = desc_match.group(1)
                if len(desc) > 500:
                    warnings.append(f"Description is {len(desc)} chars (recommended <500)")
                if len(desc) < 20:
                    warnings.append("Description is very short (<20 chars) — may not trigger reliably")

    # Check pack-manifest.json if it's a pack
    if manifest.is_file():
        try:
            data = json.loads(manifest.read_text(encoding="utf-8"))
            if "name" not in data:
                issues.append("pack-manifest.json missing 'name'")
            if "version" not in data:
                warnings.append("pack-manifest.json missing 'version' — add for per-skill versioning")
            skills_list = data.get("skills", [])
            if not skills_list:
                warnings.append("pack-manifest.json has no skills listed")
        except json.JSONDecodeError as e:
            issues.append(f"pack-manifest.json is invalid JSON: {e}")

    # Check for dangerous content
    for dangerous in path.rglob("*"):
        if dangerous.name in [".env", "credentials.json", "id_rsa", "id_ed25519"]:
            issues.append(f"Dangerous file found: {dangerous.name}")
        if dangerous.suffix in [".pem", ".key"]:
            issues.append(f"Private key file found: {dangerous.name}")

    # Report
    if issues:
        print(f"\n  ✗ {len(issues)} issue(s) found:\n")
        for issue in issues:
            print(f"    ✗ {issue}")
    else:
        print("\n  ✓ All checks passed!")

    if warnings:
        print(f"\n  ⚠ {len(warnings)} warning(s):\n")
        for w in warnings:
            print(f"    ⚠ {w}")

    return 1 if issues else 0


# ---------------------------------------------------------------------------
# list — show all market skills/packs
# ---------------------------------------------------------------------------

def cmd_list(args: argparse.Namespace) -> int:
    """List all skills and packs in the market."""
    if not INDEX_PATH.is_file():
        print("Error: index.json not found. Run 'market.py index' first.", file=sys.stderr)
        return 1

    data = json.loads(INDEX_PATH.read_text(encoding="utf-8"))

    skills = data.get("skills", [])
    packs = data.get("packs", [])

    print(f"\n  PEtFiSh Market — {len(skills)} skills, {len(packs)} packs\n")

    if skills:
        print("  Skills:")
        for s in skills:
            print(f"    {s['name']:30s} {s.get('description', '')[:60]}")

    if packs:
        print("\n  Packs:")
        for p in packs:
            aliases = ", ".join(p.get("alias", []))
            print(f"    {p['name']:40s} [{aliases}]")

    return 0


# ---------------------------------------------------------------------------
# init — scaffold a skill metadata JSON
# ---------------------------------------------------------------------------

def cmd_init(args: argparse.Namespace) -> int:
    """Scaffold a skill metadata JSON for market submission."""
    name = args.name
    output = SKILLS_DIR / f"community--{name}.json"

    if output.exists() and not args.force:
        print(f"Error: {output} already exists. Use --force to overwrite.", file=sys.stderr)
        return 1

    template = {
        "name": name,
        "namespace": "community",
        "version": "0.1.0",
        "description": "TODO: Describe what this skill does (max 500 chars)",
        "repo": "YOUR_GITHUB_USERNAME/YOUR_REPO",
        "ref": "main",
        "path": ".opencode/skills/" + name,
        "license": "Apache-2.0",
        "author": "YOUR_NAME",
        "tags": ["TODO: add", "relevant", "tags"],
    }

    SKILLS_DIR.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(template, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"  Created: {output}")
    print(f"  Edit the TODO fields, then submit a PR to petfish-market.")
    return 0


# ---------------------------------------------------------------------------
# check — pre-submission readiness check
# ---------------------------------------------------------------------------

def cmd_check(args: argparse.Namespace) -> int:
    """Pre-submission check: validate + show submission steps."""
    path = Path(args.path).resolve()

    print("\n  PEtFiSh Market — Pre-submission Check\n")

    rc = cmd_validate(argparse.Namespace(path=str(path)))

    if rc == 0:
        print("\n  Submission steps:")
        print("  1. Fork https://github.com/kylecui/petfish-market")
        print("  2. Add your skill metadata to skills/ or pack metadata to registry/community/")
        print("  3. Open a PR — CI will validate automatically")
        print("  4. Wait for maintainer review")
        print(f"\n  Or use: uv run market.py init {path.name} --force")

    return rc


# ---------------------------------------------------------------------------
# index — regenerate index.json
# ---------------------------------------------------------------------------

def cmd_index(args: argparse.Namespace) -> int:
    """Regenerate index.json from skills/ and registry/ directories."""
    skills = []
    packs = []

    # Collect skills
    if SKILLS_DIR.is_dir():
        for f in sorted(SKILLS_DIR.glob("*.json")):
            try:
                skills.append(json.loads(f.read_text(encoding="utf-8")))
            except json.JSONDecodeError:
                print(f"  Warning: invalid JSON in {f.name}", file=sys.stderr)

    # Collect packs from registry
    for subdir in ["official", "community"]:
        reg_subdir = REGISTRY_DIR / subdir
        if reg_subdir.is_dir():
            for f in sorted(reg_subdir.glob("*.json")):
                try:
                    pack = json.loads(f.read_text(encoding="utf-8"))
                    pack.setdefault("namespace", subdir)
                    packs.append(pack)
                except json.JSONDecodeError:
                    print(f"  Warning: invalid JSON in {f.name}", file=sys.stderr)

    index = {
        "version": 2,
        "generated_at": __import__("datetime").datetime.now(
            __import__("datetime").timezone.utc
        ).isoformat(),
        "skill_count": len(skills),
        "pack_count": len(packs),
        "skills": skills,
        "packs": packs,
    }

    INDEX_PATH.write_text(
        json.dumps(index, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    print(f"  Generated {INDEX_PATH.name}: {len(skills)} skills, {len(packs)} packs")
    return 0


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> int:
    parser = argparse.ArgumentParser(
        description="PEtFiSh Market CLI — contributor workflow tool"
    )
    sub = parser.add_subparsers(dest="command", required=True)

    # validate
    p_validate = sub.add_parser("validate", help="Validate a skill/pack directory")
    p_validate.add_argument("path", help="Path to skill or pack directory")

    # list
    sub.add_parser("list", help="List all market skills and packs")

    # init
    p_init = sub.add_parser("init", help="Scaffold a skill metadata JSON")
    p_init.add_argument("name", help="Skill name")
    p_init.add_argument("--force", action="store_true", help="Overwrite existing")

    # check
    p_check = sub.add_parser("check", help="Pre-submission readiness check")
    p_check.add_argument("path", help="Path to skill or pack directory")

    # index
    sub.add_parser("index", help="Regenerate index.json from registry")

    args = parser.parse_args()

    commands = {
        "validate": cmd_validate,
        "list": cmd_list,
        "init": cmd_init,
        "check": cmd_check,
        "index": cmd_index,
    }

    return commands[args.command](args)


if __name__ == "__main__":
    sys.exit(main() or 0)
