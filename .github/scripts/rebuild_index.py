#!/usr/bin/env python3
"""Rebuild index.json from skills/*.json files."""

import json
import glob
import os
from datetime import datetime, timezone

skills = []
for path in sorted(glob.glob("skills/*.json")):
    if os.path.basename(path) == ".gitkeep":
        continue
    try:
        with open(path) as f:
            entry = json.load(f)
        skills.append(entry)
    except Exception as e:
        print(f"Warning: skipping {path}: {e}")

index = {
    "version": 1,
    "generated_at": datetime.now(timezone.utc).isoformat(),
    "skill_count": len(skills),
    "skills": skills,
}

with open("index.json", "w") as f:
    json.dump(index, f, indent=2)
    f.write("\n")

print(f"index.json rebuilt with {len(skills)} skill(s)")
