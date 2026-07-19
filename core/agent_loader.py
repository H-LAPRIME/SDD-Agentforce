import os

from agno.agent import Agent
from agno.models.openai.like import OpenAILike

try:
    from core.config import MODEL_CONFIG, NVIDIA_BASE_URL
    from core.skill_registry import build_skill_instructions, get_skill_refs_for
    from core.tool_registry import get_tools_for
except ModuleNotFoundError:
    import sys
    from pathlib import Path
    sys.path.append(str(Path(__file__).resolve().parent.parent))
    from core.config import MODEL_CONFIG, NVIDIA_BASE_URL
    from core.skill_registry import build_skill_instructions, get_skill_refs_for
    from core.tool_registry import get_tools_for


def get_model(role: str = "worker", team: str | None = None) -> OpenAILike:
    """
    Retourne une instance du modele LLM, avec overrides par role/team.
    """
    config = _model_config_for(role=role, team=team)
    return OpenAILike(
        id=config["model"],
        api_key=config["api_key"],
        base_url=config.get("base_url", NVIDIA_BASE_URL),
        temperature=config["temperature"],
        top_p=config["top_p"],
        max_tokens=config["max_tokens"],
        seed=config["seed"],
    )


def get_model_for_simple_frontend() -> OpenAILike:
    """
    Retourne un modele leger dedie aux pages simples (landing page, home page).
    Utilise SIMPLE_FRONTEND_MODEL_NAME si defini, sinon FRONTEND_MODEL_NAME.
    Tokens reduits via SIMPLE_FRONTEND_MAX_TOKENS pour eviter les reponses vides.
    """
    cfg = dict(MODEL_CONFIG)
    simple_model = _env_first("SIMPLE_FRONTEND_MODEL_NAME", "FRONTEND_MODEL_NAME") or cfg["model"]
    simple_key   = _env_first("SIMPLE_FRONTEND_API_KEY", "FRONTEND_API_KEY") or cfg["api_key"]
    simple_url   = _env_first("SIMPLE_FRONTEND_BASE_URL", "FRONTEND_BASE_URL") or cfg.get("base_url", NVIDIA_BASE_URL)
    max_tokens_str = _env_first("SIMPLE_FRONTEND_MAX_TOKENS") or str(cfg["max_tokens"])
    temperature_str = _env_first("SIMPLE_FRONTEND_TEMPERATURE", "FRONTEND_TEMPERATURE") or str(cfg.get("temperature", 0.6))
    return OpenAILike(
        id=simple_model,
        api_key=simple_key,
        base_url=simple_url,
        temperature=float(temperature_str),
        top_p=cfg["top_p"],
        max_tokens=int(max_tokens_str),
        seed=cfg["seed"],
    )


def _env_first(*names: str) -> str | None:
    """Return the first non-empty env var value from a priority list."""
    for name in names:
        value = os.getenv(name, "").strip()
        if value:
            return value
    return None


def _model_config_for(role: str = "worker", team: str | None = None) -> dict:
    """
    Build model config with optional role/team overrides.

    Priority:
      1. TEAM_ROLE_* vars, e.g. FRONTEND_WORKER_MODEL_NAME
      2. TEAM_* vars, e.g. FRONTEND_MODEL_NAME
      3. ROLE_* vars, e.g. ROUTER_MODEL_NAME
      4. Global MODEL_CONFIG
    """
    cfg = dict(MODEL_CONFIG)
    role_key = (role or "worker").upper()
    team_key = (team or "").upper()
    prefixes: list[str] = []
    if team_key:
        prefixes.extend([f"{team_key}_{role_key}", team_key])
    prefixes.append(role_key)

    cfg["model"] = _env_first(*(f"{prefix}_MODEL_NAME" for prefix in prefixes)) or cfg["model"]
    cfg["api_key"] = _env_first(*(f"{prefix}_API_KEY" for prefix in prefixes)) or cfg["api_key"]
    cfg["base_url"] = _env_first(*(f"{prefix}_BASE_URL" for prefix in prefixes)) or cfg.get("base_url", NVIDIA_BASE_URL)

    temperature = _env_first(*(f"{prefix}_TEMPERATURE" for prefix in prefixes))
    max_tokens = _env_first(*(f"{prefix}_MAX_TOKENS" for prefix in prefixes))
    if temperature is not None:
        cfg["temperature"] = float(temperature)
    if max_tokens is not None:
        cfg["max_tokens"] = int(max_tokens)
    return cfg


def get_model(role: str = "worker", team: str | None = None) -> OpenAILike:
    """
    Retourne une instance du modele LLM, avec overrides par role/team.
    """
    config = _model_config_for(role=role, team=team)
    return OpenAILike(
        id=config["model"],
        api_key=config["api_key"],
        base_url=config.get("base_url", NVIDIA_BASE_URL),
        temperature=config["temperature"],
        top_p=config["top_p"],
        max_tokens=config["max_tokens"],
        seed=config["seed"],
    )


def create_agent(
    name: str,
    instructions: list[str],
    team: str | None = None,
    tools: list | None = None,
    markdown: bool = True,
    show_tool_calls: bool = True,
    tool_profile: str = "fast",
    skip_tools: bool = False,
    **kwargs,
) -> Agent:
    """
    Fabrique un agent Agno pre-configure avec le modele et ses outils MCP par team.

    Args:
        skip_tools: Si True, aucun outil MCP n'est charge (gain de latence important
                    pour les pages simples — evite de demarrer des processus npx).
    """
    if skip_tools:
        all_tools = tools or []
    else:
        mcp_tools = get_tools_for(team, profile=tool_profile) if team else []
        all_tools = mcp_tools + (tools or [])

    max_skills = 2 if tool_profile == "fast" else (4 if tool_profile == "quality" else 8)
    skill_refs = get_skill_refs_for(name, team, max_skills=max_skills)
    all_instructions = instructions + build_skill_instructions(name, team, max_skills=max_skills)
    metadata = kwargs.pop("metadata", {}) or {}
    metadata["skills"] = [
        {"name": skill.name, "path": skill.path, "description": skill.description}
        for skill in skill_refs
    ]

    return Agent(
        name=name,
        model=get_model(role="worker", team=team),
        instructions=all_instructions,
        tools=all_tools,
        markdown=markdown,
        debug_mode=True,
        metadata=metadata,
        **kwargs,
    )
