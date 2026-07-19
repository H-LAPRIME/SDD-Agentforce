from agno.team import Team
from agno.team.mode import TeamMode

from core.agent_loader import get_model
from teams.doc.agents.readme_agent import build_readme_agent
from teams.doc.agents.openapi_agent import build_openapi_agent
from teams.doc.agents.architecture_agent import build_architecture_agent


def build_doc_team() -> Team:
    """Construit une équipe Agno orientée documentation du projet."""
    members = [
        build_readme_agent(),
        build_openapi_agent(),
        build_architecture_agent(),
    ]

    return Team(
        name="Documentation Team",
        description="Équipe Agno spécialisée dans la création et la maintenance de la documentation du projet.",
        mode=TeamMode.coordinate,  # coordinate: lead decides which doc type to produce first
        model=get_model(role="team", team="doc"),
        members=members,
        instructions=[
            "Produire une documentation complète, claire et à jour pour le projet généré.",
            "Couvrir les aspects techniques (API, architecture) et utilisateur (README, guides).",
            "S'assurer que la documentation est cohérente avec le code produit par les autres teams.",
        ],
        markdown=True,
    )
