#!/usr/bin/env python3
"""Write gate result back into a skill JSON file."""

import json
import os
from datetime import datetime, timezone

skill_file = os.environ["SKILL_FILE"]
decision = os.environ["DECISION"]
lint_score = os.environ["LINT_SCORE"]
security_risk = os.environ["SECURITY_RISK"]
gate_version = os.environ["GATE_VERSION"]

with open(skill_file) as f:
    d = json.load(f)

d["gate_result"] = {
    "decision": decision,
    "lint_score": int(lint_score) if lint_score not in ["-1", ""] else -1,
    "security_risk": float(security_risk) if security_risk not in ["-1", ""] else -1,
    "validated_at": datetime.now(timezone.utc).isoformat(),
    "gate_version": gate_version,
}

with open(skill_file, "w") as f:
    json.dump(d, f, indent=2)
