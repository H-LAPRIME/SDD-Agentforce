from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from pathlib import Path
import re


@dataclass(slots=True)
class ParsedTask:
    task_id: str
    description: str
    phase: str
    team_hint: str
    done: bool
    raw_line: str


_TASK_LINE_RE = re.compile(r"^\s*-\s+\[(?P<done>[ xX])\]\s+(?P<body>.+?)\s*$")
_TASK_ID_RE = re.compile(r"\bT\d{3,}\b")
_TAG_RE = re.compile(r"\[([^\]]+)\]")

_TEAM_KEYWORDS: list[tuple[str, tuple[str, ...]]] = [
    ("frontend", ("frontend", "ui", "ux", "component", "page", "layout", "tailwind", "react", "next", "angular", "html", "css")),
    ("backend", ("backend", "api", "endpoint", "router", "service", "controller", "auth", "middleware", "validation", "openapi")),
    ("db", ("database", "schema", "migration", "sql", "postgres", "mysql", "sqlite", "mongodb", "redis", "orm", "seed")),
    ("test", ("test", "pytest", "jest", "playwright", "selenium", "smoke", "qa", "coverage")),
    ("doc", ("doc", "documentation", "readme", "architecture", "quickstart", "spec")),
    ("devops", ("devops", "docker", "ci", "cd", "pipeline", "deploy", "k8s", "kubernetes", "helm")),
    ("security", ("security", "secret", "owasp", "cve", "hardening", "auth hardening")),
]


def _infer_team_hint(description: str, explicit_hint: str | None = None) -> str:
    if explicit_hint:
        return explicit_hint

    lowered = description.lower()
    for team, keywords in _TEAM_KEYWORDS:
        if any(keyword in lowered for keyword in keywords):
            return team
    return "backend"


def parse_tasks(tasks_path: str | Path) -> list[ParsedTask]:
    path = Path(tasks_path)
    if not path.exists():
        return []

    tasks: list[ParsedTask] = []
    phase = ""
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        stripped = raw_line.strip()
        if stripped.startswith("## Phase"):
            phase = stripped.lstrip("# ")
            continue

        match = _TASK_LINE_RE.match(raw_line)
        if not match:
            continue

        body = match.group("body")
        tags = _TAG_RE.findall(body)
        explicit_team = None
        task_id = None

        for tag in tags:
            if tag.startswith("team:"):
                explicit_team = tag.split(":", 1)[1].strip().lower() or None
                continue
            if tag == "P" or tag.startswith("US"):
                continue
            if task_id is None and _TASK_ID_RE.fullmatch(tag.strip()):
                task_id = tag.strip()

        if task_id is None:
            task_match = _TASK_ID_RE.search(body)
            if task_match:
                task_id = task_match.group(0)

        description = re.sub(r"\s+", " ", re.sub(r"\[[^\]]+\]", " ", body)).strip()
        if not task_id:
            continue

        tasks.append(
            ParsedTask(
                task_id=task_id,
                description=description,
                phase=phase,
                team_hint=_infer_team_hint(description, explicit_team),
                done=match.group("done").lower() == "x",
                raw_line=raw_line,
            )
        )

    return tasks


def group_tasks_by_team(tasks: list[ParsedTask]) -> dict[str, list[ParsedTask]]:
    grouped: dict[str, list[ParsedTask]] = {}
    for task in tasks:
        grouped.setdefault(task.team_hint, []).append(task)
    return grouped


def tasks_summary(tasks: list[ParsedTask]) -> str:
    counts = Counter(task.team_hint for task in tasks)
    if not counts:
        return "No executable tasks found."
    return ", ".join(f"{team}:{count}" for team, count in sorted(counts.items()))


def build_task_brief(
    *,
    task: ParsedTask,
    spec_text: str,
    plan_text: str,
    tasks_text: str,
    feature_dir: str,
) -> str:
    return (
        f"Feature directory: {feature_dir}\n"
        f"Phase: {task.phase or 'unknown'}\n"
        f"Task ID: {task.task_id}\n"
        f"Team hint: {task.team_hint}\n"
        f"Task: {task.description}\n\n"
        "Hard constraints:\n"
        "- Do not create a new execution plan.\n"
        "- Do not split or rename tasks.\n"
        "- Use the provided spec, plan, and tasks as the only source of truth.\n"
        "- If the task is blocked by missing context, report the blocker explicitly.\n\n"
        "spec.md\n"
        "--------\n"
        f"{spec_text}\n\n"
        "plan.md\n"
        "--------\n"
        f"{plan_text}\n\n"
        "tasks.md\n"
        "--------\n"
        f"{tasks_text}\n\n"
        "Execute only the single task above and return implementation-ready output."
    )


def mark_tasks_completed(tasks_path: str | Path, completed_ids: set[str]) -> list[str]:
    path = Path(tasks_path)
    if not path.exists() or not completed_ids:
        return []

    lines = path.read_text(encoding="utf-8").splitlines()
    updated: list[str] = []
    changed: list[str] = []
    for line in lines:
        match = _TASK_LINE_RE.match(line)
        if not match:
            updated.append(line)
            continue

        body = match.group("body")
        task_match = _TASK_ID_RE.search(body)
        if task_match and task_match.group(0) in completed_ids and match.group("done") != "x":
            line = line.replace("- [ ]", "- [x]", 1)
            changed.append(task_match.group(0))
        updated.append(line)

    path.write_text("\n".join(updated) + "\n", encoding="utf-8")
    return changed