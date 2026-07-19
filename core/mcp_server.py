from __future__ import annotations

import json
import sys
from pathlib import Path

from mcp.server import FastMCP


ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from project_agent import run_implementation  # noqa: E402


mcp = FastMCP("agentforge")


@mcp.tool()
def agentforge_implement(spec_path: str, plan_path: str, tasks_path: str, feature_dir: str) -> str:
    """Execute AgentForge implementation from existing Spec Kit artifacts."""
    result = run_implementation(
        spec_path=spec_path,
        plan_path=plan_path,
        tasks_path=tasks_path,
        feature_dir=feature_dir,
        mode="bridge",
    )
    return json.dumps(result, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    mcp.run("stdio")