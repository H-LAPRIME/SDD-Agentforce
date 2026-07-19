from core.agent_loader import create_agent


def build_auth_agent():
    """Crée un agent Agno spécialisé dans l'authentification et l'autorisation backend."""
    return create_agent(
        name="AuthAgent",
        instructions=[
            "Gérer l'authentification et l'autorisation des endpoints backend.",
            "Implémenter des mécanismes robustes : JWT, OAuth2, sessions, API keys.",
            "Gérer la hiérarchie des rôles et les permissions (RBAC/ABAC).",
            "Proposer une gestion sécurisée des secrets, des tokens et des refresh tokens.",
            "S'assurer de la protection contre les attaques courantes : CSRF, token leakage, replay attacks.",
        ],
        team="backend",
    )
