"""
AgentForge skill registry.

Discovers markdown skills from skills/*/SKILL.md and returns compact
agent-specific references that can be injected into Agno agent instructions.
"""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
import re


ROOT_DIR = Path(__file__).resolve().parent.parent
SKILLS_DIR = ROOT_DIR / "skills"
try:
    from core.config import RUN_PROFILE
except ModuleNotFoundError:
    import sys
    from pathlib import Path
    sys.path.append(str(Path(__file__).resolve().parent.parent))
    from core.config import RUN_PROFILE

if RUN_PROFILE == "fast":
    MAX_SKILLS_PER_AGENT = 2
elif RUN_PROFILE == "quality":
    MAX_SKILLS_PER_AGENT = 4
else:
    MAX_SKILLS_PER_AGENT = 8
FRONTMATTER_READ_LIMIT = 4096


@dataclass(frozen=True)
class SkillRef:
    name: str
    path: str
    description: str


_TEAM_SKILL_HINTS: dict[str, tuple[str, ...]] = {
    "frontend": (
        "react",
        "next",
        "angular",
        "tailwind",
        "bootstrap",
        "webapp",
        "playwright",
        "accessibility",
        "api",
    ),
    "backend": (
        "api",
        "openapi",
        "fastapi",
        "django",
        "flask",
        "express",
        "node",
        "spring",
        "security",
        "auth",
    ),
    "db": (
        "sql",
        "postgres",
        "mysql",
        "sqlite",
        "mongodb",
        "redis",
        "migration",
        "orm",
        "database",
    ),
    "test": (
        "test",
        "pytest",
        "jest",
        "playwright",
        "selenium",
        "coverage",
        "webapp-testing",
    ),
    "doc": (
        "readme",
        "openapi",
        "architecture",
        "specification",
        "blueprint",
        "adr",
        "docs",
    ),
    "devops": (
        "docker",
        "deployment",
        "deploy",
        "ci",
        "github-action",
        "terraform",
        "cloud",
    ),
    "security": (
        "security",
        "secret",
        "owasp",
        "supply-chain",
        "audit",
        "auth",
        "mcp-security",
    ),
}

_AGENT_SKILL_HINTS: dict[str, tuple[str, ...]] = {
    "APIIntegrationAgent": ("api", "openapi", "typespec-api"),
    "FrontendAPIIntegrationAgent": ("api", "openapi", "typespec-api"),
    "AuthAgent": ("auth", "security", "owasp"),
    "AuthHardeningAgent": ("auth", "security", "owasp"),
    "BackendStructureAgent": ("architecture", "api", "blueprint"),
    "ModelsAgent": ("orm", "database", "sql"),
    "RoutingAgent": ("api", "openapi"),
    "MiddlewareBuilderAgent": ("api", "security"),
    "FastAPIAgent": ("fastapi", "api", "openapi"),
    "NestJSAgent": ("node", "api", "openapi"),
    "DjangoBackendAgent": ("django", "api", "security"),
    "DjangoFrontendAgent": ("django", "frontend"),
    "FlaskAgent": ("flask", "api", "openapi"),
    "ExpressBackendAgent": ("express", "node", "api"),
    "ExpressFrontendAgent": ("express", "node", "frontend"),
    "SpringBootAgent": ("spring", "spring-boot", "java"),
    "GinAgent": ("go", "api", "openapi"),
    "PostgresAgent": ("postgres", "postgresql", "sql"),
    "MySQLAgent": ("mysql", "sql"),
    "SQLiteAgent": ("sqlite", "sql"),
    "MongoDBAgent": ("mongodb", "mongo"),
    "RedisAgent": ("redis", "cache"),
    "MigrationAgent": ("migration", "postgres", "sql"),
    "ORMAgent": ("orm", "database", "sql"),
    "SchemaDesignerAgent": ("schema", "database", "sql"),
    "FAISSVectorAgent": ("vector", "qdrant", "embedding"),
    "StateManagementAgent": ("redux", "zustand", "pinia", "ngrx", "recoil", "jotai", "state-management"),
    "FormHandlingAgent": ("form", "react-hook-form", "formik", "vee-validate", "validation"),
    "SEOAgent": ("seo", "lighthouse", "structured-data", "core-web-vitals", "meta-tags"),
    "i18nAgent": ("i18n", "i18next", "localization", "internationalization", "react-intl"),
    "GraphQLAgent": ("graphql", "apollo", "hasura", "relay", "graphql-yoga"),
    "SSEAgent": ("websocket", "socket-io", "sse", "realtime", "django-channels"),
    "BackgroundJobsAgent": ("celery", "bullmq", "sidekiq", "hangfire", "background-jobs", "task-queue"),
    "MonitoringAgent": ("prometheus", "grafana", "opentelemetry", "elk", "sentry", "monitoring"),
    "CachingAgent": ("caching", "redis-cache", "cdn", "cloudflare", "performance"),
    "LighthouseAgent": ("lighthouse", "performance-audit", "core-web-vitals", "accessibility-audit"),
    "ReactAgent": ("react", "react18", "react19", "webapp-testing"),
    "NextJSAgent": ("next", "react", "webapp-testing"),
    "AngularAgent": ("angular", "webapp-testing"),
    "TailwindAgent": ("tailwind", "web-design", "frontend"),
    "BootstrapAgent": ("bootstrap", "frontend"),
    "ComponentBuilderAgent": ("react", "component", "frontend"),
    "AccessibilityAgent": ("accessibility", "a11y", "web-design", "frontend"),
    "UIArchitectAgent": ("architecture", "web-design", "frontend"),
    "VisualQAAgent": ("webapp-testing", "web-design", "ui-screenshots", "playwright"),
    "NodeJSFrontendAgent": ("node", "javascript", "typescript"),
    "DockerAgent": ("docker", "multi-stage-dockerfile"),
    "CIAgent": ("ci", "github-action", "workflow"),
    "DeployAgent": ("deploy", "deployment", "terraform"),
    "ReadmeAgent": ("readme", "docs"),
    "OpenAPIAgent": ("openapi", "api", "typespec"),
    "ArchitectureAgent": ("architecture", "blueprint", "adr"),
    "SecretsAgent": ("secret", "security", "audit"),
    "PytestAgent": ("pytest", "coverage", "test"),
    "JestAgent": ("jest", "javascript", "test"),
    "PlaywrightAgent": ("playwright", "webapp-testing", "test"),
    "SeleniumAgent": ("selenium", "test", "webapp-testing"),
    "SmokeTestAgent": ("smoke", "playwright", "webapp-testing", "test"),
    "QualityGateAgent": ("quality", "coverage", "ci", "test"),
}


def _slug_tokens(value: str) -> set[str]:
    spaced = re.sub(r"(?<!^)(?=[A-Z])", "-", value)
    return {token for token in re.split(r"[^a-z0-9]+", spaced.lower()) if token}


def _read_frontmatter(text: str) -> dict[str, str]:
    if not text.startswith("---"):
        return {}

    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}

    data: dict[str, str] = {}
    for line in parts[1].splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        data[key.strip().lower()] = value.strip().strip("'\"")
    return data


@lru_cache(maxsize=1)
def discover_skills() -> tuple[SkillRef, ...]:
    """Return every local markdown skill with a stable relative path."""
    if not SKILLS_DIR.exists():
        return ()

    skills: list[SkillRef] = []
    for skill_file in sorted(SKILLS_DIR.glob("*/SKILL.md")):
        try:
            with skill_file.open("r", encoding="utf-8", errors="replace") as handle:
                text = handle.read(FRONTMATTER_READ_LIMIT)
        except OSError:
            continue

        frontmatter = _read_frontmatter(text)
        name = frontmatter.get("name") or skill_file.parent.name
        description = frontmatter.get("description", "")
        rel_path = skill_file.relative_to(ROOT_DIR).as_posix()
        skills.append(SkillRef(name=name, path=rel_path, description=description))

    return tuple(skills)


def _score_skill(skill: SkillRef, hints: set[str], priority_hints: set[str] | None = None) -> int:
    haystack = " ".join([skill.name, skill.path, skill.description]).lower()
    skill_tokens = _slug_tokens(skill.name) | _slug_tokens(skill.path)
    priority_hints = priority_hints or set()

    score = 0
    for hint in hints:
        hint = hint.lower()
        weight = 2 if hint in priority_hints else 1
        if hint in haystack:
            score += 3 * weight
        if hint in skill_tokens:
            score += 2 * weight
    return score


def get_skill_refs_for(agent_name: str, team: str | None = None, max_skills: int | None = None) -> list[SkillRef]:
    """Return the most relevant local skills for an agent/team pair."""
    limit = max_skills if max_skills is not None else MAX_SKILLS_PER_AGENT
    priority_hints = set(_slug_tokens(agent_name))
    priority_hints.update(_AGENT_SKILL_HINTS.get(agent_name, ()))
    hints = set(priority_hints)
    if team:
        hints.update(_slug_tokens(team))
        hints.update(_TEAM_SKILL_HINTS.get(team, ()))

    scored = [
        (score, skill)
        for skill in discover_skills()
        if (score := _score_skill(skill, hints, priority_hints)) > 0
    ]
    scored.sort(key=lambda item: (-item[0], item[1].name))

    return [skill for _, skill in scored[:limit]]


def build_skill_instructions(agent_name: str, team: str | None = None, max_skills: int | None = None) -> list[str]:
    """Build compact instructions linking an agent to local markdown skills."""
    skills = get_skill_refs_for(agent_name, team, max_skills=max_skills)
    if not skills:
        return []

    lines = [
        "Skills liees disponibles dans le repo; applique-les quand elles correspondent a la tache:",
    ]
    for skill in skills:
        description = f" - {skill.description}" if skill.description else ""
        lines.append(f"- {skill.name}: {skill.path}{description}")

    return ["\n".join(lines)]
