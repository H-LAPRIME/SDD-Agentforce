from agno.team import Team
from agno.team.mode import TeamMode

from core.agent_loader import get_model
from teams.devops.agents.docker_agent import build_docker_agent
from teams.devops.agents.ci_agent import build_ci_agent
from teams.devops.agents.deploy_agent import build_deploy_agent
from teams.devops.agents.monitoring_agent import build_monitoring_agent
from teams.devops.agents.caching_agent import build_caching_agent


def build_devops_team() -> Team:
    """Construit une équipe Agno orientée DevOps et Infrastructure."""
    members = [
        build_docker_agent(),
        build_ci_agent(),
        build_deploy_agent(),
        build_monitoring_agent(),
        build_caching_agent(),
    ]

    return Team(
        name="DevOps Engineering Team",
        description="Équipe Agno spécialisée dans la conteneurisation, l'intégration continue et le déploiement.",
        mode=TeamMode.coordinate,  # coordinate: lead decides Docker/CI/Deploy order
        model=get_model(role="team", team="devops"),
        members=members,
        instructions=[
            "Automatiser et fiabiliser le cycle de vie applicatif : build, test, deploy.",
            "Garantir des déploiements reproductibles, sécurisés et réversibles.",
            "Proposer des configurations adaptées à l'environnement cible : local, staging, production.",
        ],
        markdown=True,
    )
