#!/usr/bin/env python3
"""Rebuild index.json v2 from skills/*.json and registry/**/*.json files."""

import json
import glob
import os
from datetime import datetime, timezone

# --- Scan single-skill entries from skills/*.json ---
skills = []
for path in sorted(glob.glob("skills/*.json")):
    if os.path.basename(path) in (".gitkeep",):
        continue
    try:
        with open(path) as f:
            entry = json.load(f)
        skills.append(entry)
    except Exception as e:
        print(f"Warning: skipping {path}: {e}")

# Sort skills by name
skills.sort(key=lambda x: x.get("name", ""))

# --- Scan pack entries from registry/official/*.json and registry/community/*.json ---
packs = []
for namespace in ("official", "community"):
    pattern = f"registry/{namespace}/*.json"
    for path in sorted(glob.glob(pattern)):
        if os.path.basename(path) in (".gitkeep",):
            continue
        try:
            with open(path) as f:
                entry = json.load(f)
            # Ensure namespace is set correctly
            entry["namespace"] = namespace
            packs.append(entry)
        except Exception as e:
            print(f"Warning: skipping {path}: {e}")

# Sort packs by namespace then name
packs.sort(key=lambda x: (x.get("namespace", ""), x.get("name", "")))

# --- Build v2 index ---
index = {
    "version": 2,
    "generated_at": datetime.now(timezone.utc).isoformat(),
    "skill_count": len(skills),
    "pack_count": len(packs),
    "skills": skills,
    "packs": packs,
}

with open("index.json", "w") as f:
    json.dump(index, f, indent=2)
    f.write("\n")

print(f"index.json v2 rebuilt: {len(skills)} skill(s), {len(packs)} pack(s)")
