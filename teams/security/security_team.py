from agno.team import Team
from agno.team.mode import TeamMode

from core.agent_loader import get_model
from teams.security.agents.auth_hardening_agent import build_auth_hardening_agent
from teams.security.agents.secrets_agent import build_secrets_agent


def build_security_team() -> Team:
    """Construit une équipe Agno orientée sécurité applicative."""
    members = [
        build_auth_hardening_agent(),
        build_secrets_agent(),
    ]

    return Team(
        name="Security Engineering Team",
        description="Équipe Agno spécialisée dans la sécurité applicative, l'authentification et la gestion des secrets.",
        mode=TeamMode.broadcast,  # Tous les agents auditent en parallèle : Auth + Secrets
        model=get_model(role="team", team="security"),
        members=members,
        instructions=[
            "Auditer et renforcer la sécurité du code produit par les autres teams.",
            "Identifier les vulnérabilités OWASP Top 10 et proposer des correctifs.",
            "S'assurer que les secrets, les credentials et les données sensibles sont protégés.",
        ],
        markdown=True,
    )
