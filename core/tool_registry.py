"""
AgentForge — Tool Registry
Registre central de tous les MCP tools disponibles.
Chaque team/agent importe get_tools_for() pour obtenir ses outils.

Usage :
    from core.tool_registry import get_tools_for, MCPTool
    tools = get_tools_for("frontend")
"""

from __future__ import annotations

from enum import Enum
from typing import Any

from agno.tools.mcp import MCPTools
from mcp import StdioServerParameters
from agno.tools.mcp.params import SSEClientParams

try:
    from core.config import get_mcp_config
except ModuleNotFoundError:
    import sys
    from pathlib import Path
    sys.path.append(str(Path(__file__).resolve().parent.parent))
    from core.config import get_mcp_config


# ── Enum des identifiants MCP ────────────────────────────────────────────────

class MCPTool(str, Enum):
    FILESYSTEM   = "filesystem"
    MEMORY       = "memory"
    FETCH        = "fetch"
    YOU_SEARCH   = "you_search"
    BRAVE_SEARCH = "brave_search"
    GIT          = "git"
    GITHUB       = "github"
    POSTGRES     = "postgres"
    MYSQL        = "mysql"
    SQLITE       = "sqlite"
    MONGODB      = "mongodb"
    REDIS        = "redis"
    PLAYWRIGHT   = "playwright"
    DOCKER       = "docker"
    SUPABASE     = "supabase"
    STRIPE       = "stripe"
    LIGHTHOUSE   = "lighthouse"
    FIGMA        = "figma"
    RESEND       = "resend"
    CLOUDFLARE   = "cloudflare"
    ANALYTICS    = "analytics"


# ── Définition dynamique des MCP servers ──────────────────────────────────────

def get_mcp_definitions() -> dict[MCPTool, dict[str, Any]]:
    """Génère la configuration des serveurs MCP dynamiquement avec la config actuelle."""
    
    config = get_mcp_config()
    
    return {
        # 1. Filesystem — lecture/écriture du projet généré
        MCPTool.FILESYSTEM: {
            "command": "npx",
            "args": [
                "-y",
                "@modelcontextprotocol/server-filesystem",
                config.get("output_dir", "./output"),
            ],
            "env": {},
        },
    
        # 2. Memory — mémoire persistante entre agents (knowledge graph)
        MCPTool.MEMORY: {
            "command": "npx",
            "args": ["-y", "@modelcontextprotocol/server-memory"],
            "env": {},
        },
    
        # 3. Fetch — lecture d'URLs distantes (docs, swagger, openapi)
        MCPTool.FETCH: {
            "command": "npx",
            "args": ["-y", "@modelcontextprotocol/server-fetch"],
            "env": {},
        },
    
        # 4. You.com Search — recherche web via serveur MCP distant
        MCPTool.YOU_SEARCH: {
            "url": "https://api.you.com/mcp",
            "headers": {
                "Authorization": "Bearer " + config.get("you_api_key", "")
            },
        },
    
        # 5. Git — opérations VCS sur le projet généré
        MCPTool.GIT: {
            "command": "uvx",
            "args": ["mcp-server-git", "--repository", config.get("git_repo", "./output")],
            "env": {},
        },
    
        # 6. GitHub — API GitHub (repos, PRs, issues, Actions)
        MCPTool.GITHUB: {
            "command": "npx",
            "args": ["-y", "@modelcontextprotocol/server-github"],
            "env": {"GITHUB_PERSONAL_ACCESS_TOKEN": config.get("github_token", "")},
        },
    
        # 7. PostgreSQL — schémas, queries, migrations
        MCPTool.POSTGRES: {
            "command": "npx",
            "args": [
                "-y",
                "@modelcontextprotocol/server-postgres",
                config.get("database_url", ""),
            ],
            "env": {},
        },
        
        # 7.b MySQL — schémas, queries, migrations
        MCPTool.MYSQL: {
            "command": "npx",
            "args": ["-y", "@benborla29/mcp-server-mysql"],
            "env": {
                "MYSQL_HOST":     config.get("mysql_host", "localhost"),
                "MYSQL_PORT":     config.get("mysql_port", "3306"),
                "MYSQL_USER":     config.get("mysql_user", "root"),
                "MYSQL_PASSWORD": config.get("mysql_password", ""),
                "MYSQL_DATABASE": config.get("mysql_database", ""),
            },
        },
    
        # 8. SQLite — base locale légère pour dev/tests
        MCPTool.SQLITE: {
            "command": "npx",
            "args": [
                "-y",
                "@modelcontextprotocol/server-sqlite",
                "--db-path",
                config.get("sqlite_db", "./output/dev.db"),
            ],
            "env": {},
        },
    
        # 9. MongoDB — CRUD collections, agrégations, index
        MCPTool.MONGODB: {
            "command": "npx",
            "args": ["-y", "mcp-mongo-server", config.get("mongodb_uri", "")],
            "env": {},
        },
    
        # 10. Redis — cache, sessions, pub/sub
        MCPTool.REDIS: {
            "command": "npx",
            "args": ["-y", "mcp-server-redis"],
            "env": {"REDIS_URL": config.get("redis_url", "")},
        },
    
        # 11. Playwright — tests E2E, screenshots, navigation navigateur
        MCPTool.PLAYWRIGHT: {
            "command": "npx",
            "args": ["-y", "@playwright/mcp"],
            "env": {},
        },
    
        # 12. Docker — build/run containers, compose, logs
        MCPTool.DOCKER: {
            "command": "npx",
            "args": ["-y", "mcp-server-docker"],
            "env": {},
        },

        # 13. Brave Search — recherche web alternative
        MCPTool.BRAVE_SEARCH: {
            "command": "npx",
            "args": ["-y", "@anthropic/mcp-server-brave-search"],
            "env": {"BRAVE_API_KEY": config.get("brave_api_key", "")},
        },

        # 14. Supabase — BaaS : auth, DB, storage, realtime
        MCPTool.SUPABASE: {
            "command": "npx",
            "args": ["-y", "mcp-server-supabase"],
            "env": {
                "SUPABASE_URL": config.get("supabase_url", ""),
                "SUPABASE_SERVICE_KEY": config.get("supabase_service_key", ""),
            },
        },

        # 15. Stripe — paiements, factures, webhooks
        MCPTool.STRIPE: {
            "command": "npx",
            "args": ["-y", "@stripe/mcp-server-stripe"],
            "env": {"STRIPE_API_KEY": config.get("stripe_api_key", "")},
        },

        # 16. Lighthouse — audit performance, accessibilité, SEO
        MCPTool.LIGHTHOUSE: {
            "command": "npx",
            "args": ["-y", "@anthropic/mcp-server-lighthouse"],
            "env": {},
        },

        # 17. Figma — design tokens, composants, export
        MCPTool.FIGMA: {
            "command": "npx",
            "args": ["-y", "mcp-server-figma"],
            "env": {"FIGMA_ACCESS_TOKEN": config.get("figma_access_token", "")},
        },

        # 18. Resend — emails transactionnels
        MCPTool.RESEND: {
            "command": "npx",
            "args": ["-y", "@resend/mcp-server-resend"],
            "env": {"RESEND_API_KEY": config.get("resend_api_key", "")},
        },

        # 19. Cloudflare — DNS, Workers, Pages, KV, R2
        MCPTool.CLOUDFLARE: {
            "command": "npx",
            "args": ["-y", "mcp-server-cloudflare"],
            "env": {
                "CLOUDFLARE_API_TOKEN": config.get("cloudflare_api_token", ""),
                "CLOUDFLARE_ACCOUNT_ID": config.get("cloudflare_account_id", ""),
            },
        },

        # 20. Analytics — Google Analytics / Plausible / PostHog
        MCPTool.ANALYTICS: {
            "command": "npx",
            "args": ["-y", "mcp-server-analytics"],
            "env": {
                "ANALYTICS_PROVIDER": config.get("analytics_provider", "plausible"),
                "ANALYTICS_API_KEY": config.get("analytics_api_key", ""),
            },
        },
    }


# ── Profils de vitesse ────────────────────────────────────────────────────────

# "fast"    → outils minimaux pour démarrer vite (projets simples)
# "quality" → outils complets pour projets standards (comportement actuel)
# "full"    → tous les outils disponibles (qualité + exploration)

_TOOL_PROFILES: dict[str, dict[str, list[MCPTool]]] = {
    "fast": {
        "project_agent": [
            MCPTool.FILESYSTEM,
            MCPTool.FETCH,
        ],
        "frontend": [
            MCPTool.FILESYSTEM,
            MCPTool.FETCH,
        ],
        "backend": [
            MCPTool.FILESYSTEM,
            MCPTool.SQLITE,
        ],
        "db": [
            MCPTool.FILESYSTEM,
            MCPTool.SQLITE,
        ],
        "test": [
            MCPTool.FILESYSTEM,
            MCPTool.PLAYWRIGHT,
        ],
        "doc": [
            MCPTool.FILESYSTEM,
        ],
        "devops": [
            MCPTool.FILESYSTEM,
            MCPTool.DOCKER,
        ],
        "security": [
            MCPTool.FILESYSTEM,
        ],
    },
    "quality": {
        "project_agent": [
            MCPTool.FILESYSTEM,
            MCPTool.MEMORY,
            MCPTool.FETCH,
            MCPTool.YOU_SEARCH,
            MCPTool.BRAVE_SEARCH,
        ],
        "frontend": [
            MCPTool.FILESYSTEM,
            MCPTool.GIT,
            MCPTool.GITHUB,
            MCPTool.PLAYWRIGHT,
            MCPTool.FETCH,
            MCPTool.YOU_SEARCH,
            MCPTool.BRAVE_SEARCH,
            MCPTool.FIGMA,
            MCPTool.MEMORY,
        ],
        "backend": [
            MCPTool.FILESYSTEM,
            MCPTool.GIT,
            MCPTool.GITHUB,
            MCPTool.FETCH,
            MCPTool.YOU_SEARCH,
            MCPTool.SQLITE,
            MCPTool.SUPABASE,
            MCPTool.MEMORY,
        ],
        "db": [
            MCPTool.FILESYSTEM,
            MCPTool.POSTGRES,
            MCPTool.MYSQL,
            MCPTool.SQLITE,
            MCPTool.MONGODB,
            MCPTool.YOU_SEARCH,
            MCPTool.FETCH,
            MCPTool.MEMORY,
        ],
        "test": [
            MCPTool.FILESYSTEM,
            MCPTool.GIT,
            MCPTool.PLAYWRIGHT,
            MCPTool.FETCH,
            MCPTool.YOU_SEARCH,
            MCPTool.LIGHTHOUSE,
            MCPTool.MEMORY,
        ],
        "doc": [
            MCPTool.FILESYSTEM,
            MCPTool.GIT,
            MCPTool.FETCH,
            MCPTool.YOU_SEARCH,
            MCPTool.MEMORY,
        ],
        "devops": [
            MCPTool.FILESYSTEM,
            MCPTool.DOCKER,
            MCPTool.GIT,
            MCPTool.GITHUB,
            MCPTool.PLAYWRIGHT,
            MCPTool.YOU_SEARCH,
            MCPTool.CLOUDFLARE,
            MCPTool.MEMORY,
        ],
        "security": [
            MCPTool.POSTGRES,
            MCPTool.MYSQL,
            MCPTool.MONGODB,
            MCPTool.YOU_SEARCH,
            MCPTool.SUPABASE,
            MCPTool.MEMORY,
        ],
    },
    "full": {
        "project_agent": [
            MCPTool.FILESYSTEM,
            MCPTool.MEMORY,
            MCPTool.FETCH,
            MCPTool.YOU_SEARCH,
            MCPTool.BRAVE_SEARCH,
        ],
        "frontend": [
            MCPTool.FILESYSTEM,
            MCPTool.GIT,
            MCPTool.GITHUB,
            MCPTool.PLAYWRIGHT,
            MCPTool.FETCH,
            MCPTool.YOU_SEARCH,
            MCPTool.BRAVE_SEARCH,
            MCPTool.FIGMA,
            MCPTool.LIGHTHOUSE,
            MCPTool.ANALYTICS,
            MCPTool.MEMORY,
        ],
        "backend": [
            MCPTool.FILESYSTEM,
            MCPTool.GIT,
            MCPTool.GITHUB,
            MCPTool.FETCH,
            MCPTool.YOU_SEARCH,
            MCPTool.SUPABASE,
            MCPTool.STRIPE,
            MCPTool.RESEND,
            MCPTool.POSTGRES,
            MCPTool.MYSQL,
            MCPTool.SQLITE,
            MCPTool.MONGODB,
            MCPTool.REDIS,
            MCPTool.MEMORY,
        ],
        "db": [
            MCPTool.FILESYSTEM,
            MCPTool.POSTGRES,
            MCPTool.MYSQL,
            MCPTool.SQLITE,
            MCPTool.MONGODB,
            MCPTool.REDIS,
            MCPTool.YOU_SEARCH,
            MCPTool.FETCH,
            MCPTool.MEMORY,
        ],
        "test": [
            MCPTool.FILESYSTEM,
            MCPTool.GIT,
            MCPTool.GITHUB,
            MCPTool.PLAYWRIGHT,
            MCPTool.FETCH,
            MCPTool.YOU_SEARCH,
            MCPTool.LIGHTHOUSE,
            MCPTool.MEMORY,
        ],
        "doc": [
            MCPTool.FILESYSTEM,
            MCPTool.GIT,
            MCPTool.FETCH,
            MCPTool.YOU_SEARCH,
            MCPTool.BRAVE_SEARCH,
            MCPTool.MEMORY,
        ],
        "devops": [
            MCPTool.FILESYSTEM,
            MCPTool.DOCKER,
            MCPTool.GIT,
            MCPTool.GITHUB,
            MCPTool.PLAYWRIGHT,
            MCPTool.YOU_SEARCH,
            MCPTool.CLOUDFLARE,
            MCPTool.MEMORY,
        ],
        "security": [
            MCPTool.FILESYSTEM,
            MCPTool.POSTGRES,
            MCPTool.MYSQL,
            MCPTool.MONGODB,
            MCPTool.SUPABASE,
            MCPTool.YOU_SEARCH,
            MCPTool.MEMORY,
        ],
    },
}


# ── API publique ─────────────────────────────────────────────────────────────

def build_mcp_tool(tool: MCPTool) -> MCPTools:
    """Instancie un MCPTools Agno à partir de sa définition générée dynamiquement."""
    definitions = get_mcp_definitions()
    definition = definitions[tool]
    
    if "url" in definition:
        # Config HTTP/SSE
        server_params = SSEClientParams(
            url=definition["url"],
            headers=definition.get("headers", {})
        )
    else:
        # Config classique Stdio (npx, uvx, etc.)
        env = definition.get("env") or {}
        server_params = StdioServerParameters(
            command=definition["command"],
            args=definition["args"],
            env=env,
        )
        
    return MCPTools(server_params=server_params)


def get_tools_for(team: str, profile: str = "fast") -> list[MCPTools]:
    """
    Retourne la liste des MCPTools Agno pour une team donnée, selon un profil.

    Args:
        team: Nom de la team (ex: "frontend", "db", "devops").
        profile: Profil de vitesse ("fast", "quality", "full").

    Returns:
        Liste d'instances MCPTools prêtes à passer à create_agent().
    """
    profile_map = _TOOL_PROFILES.get(profile, _TOOL_PROFILES["fast"])
    tool_ids = profile_map.get(team, [MCPTool.FILESYSTEM])
    return [build_mcp_tool(t) for t in tool_ids]


def get_tool(tool: MCPTool) -> MCPTools:
    """Retourne un MCPTool individuel par son identifiant."""
    return build_mcp_tool(tool)
