from agno.team import Team
from agno.team.mode import TeamMode

from core.agent_loader import get_model
from teams.backend.agents.api_integration_agent import build_api_integration_agent
from teams.backend.agents.auth_agent import build_auth_agent
from teams.backend.agents.backend_structure_agent import build_backend_structure_agent
from teams.backend.agents.models_agent import build_models_agent
from teams.backend.agents.routing_agent import build_routing_agent
from teams.backend.agents.middleware_builder_agent import build_middleware_builder_agent
from teams.backend.agents.fastapi_agent import build_fastapi_agent
from teams.backend.agents.nestjs_agent import build_nestjs_agent
from teams.backend.agents.django_agent import build_django_backend_agent
from teams.backend.agents.flask_agent import build_flask_agent
from teams.backend.agents.express_agent import build_express_backend_agent
from teams.backend.agents.spring_agent import build_spring_agent
from teams.backend.agents.gin_agent import build_gin_agent
from teams.backend.agents.graphql_agent import build_graphql_agent
from teams.backend.agents.sse_agent import build_sse_agent
from teams.backend.agents.background_jobs_agent import build_background_jobs_agent


def build_backend_team() -> Team:
    """Construit une équipe Agno orientée développement backend."""
    members = [
        build_backend_structure_agent(),
        build_models_agent(),
        build_routing_agent(),
        build_auth_agent(),
        build_middleware_builder_agent(),
        build_api_integration_agent(),
        build_graphql_agent(),
        build_background_jobs_agent(),
        build_sse_agent(),
        build_fastapi_agent(),
        build_nestjs_agent(),
        build_django_backend_agent(),
        build_flask_agent(),
        build_express_backend_agent(),
        build_spring_agent(),
        build_gin_agent(),
    ]

    return Team(
        name="Backend Engineering Team",
        description="Équipe Agno spécialisée dans la conception et l'implémentation backend.",
        mode=TeamMode.route,
        model=get_model(role="team", team="backend"),
        members=members,
        instructions=[
            "Selectionne l'agent le plus adapte (ex: ExpressAgent ou DjangoAgent) pour realiser le backend.",
            "L'agent selectionne doit directement renvoyer le code final en markdown.",
        ],
        markdown=True,
    )
