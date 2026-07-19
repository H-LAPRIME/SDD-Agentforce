from agno.team import Team
from agno.team.mode import TeamMode

from core.agent_loader import get_model
from teams.test.agents.jest_agent import build_jest_agent
from teams.test.agents.playwright_agent import build_playwright_agent
from teams.test.agents.pytest_agent import build_pytest_agent
from teams.test.agents.quality_gate_agent import build_quality_gate_agent
from teams.test.agents.selenium_agent import build_selenium_agent
from teams.test.agents.smoke_test_agent import build_smoke_test_agent
from teams.test.agents.lighthouse_agent import build_lighthouse_agent


def build_test_team() -> Team:
    """Build the Agno team focused on software testing and quality gates."""
    members = [
        build_smoke_test_agent(),
        build_lighthouse_agent(),
        build_quality_gate_agent(),
        build_pytest_agent(),
        build_jest_agent(),
        build_playwright_agent(),
        build_selenium_agent(),
    ]

    return Team(
        name="Test Engineering Team",
        description="Equipe Agno specialisee dans les tests automatises, la validation runtime et les gates qualite.",
        mode=TeamMode.coordinate,
        model=get_model(role="team", team="test"),
        members=members,
        instructions=[
            "Commencer par SmokeTestAgent pour detecter les echecs bloquants rapides: app qui ne demarre pas, page blanche, erreur console, endpoint critique KO.",
            "Choisir ensuite les specialistes adaptes: PytestAgent pour Python/API, JestAgent pour JS/React, PlaywrightAgent pour E2E navigateur, SeleniumAgent seulement si Selenium est explicitement demande ou deja present.",
            "Toujours inclure des tests de regression pour les bugs observes, notamment SyntaxError frontend, assets 404 critiques, mauvais content-type et root DOM absent.",
            "Pour les frontends, privilegier Playwright avec locators par role/testId, verification console, screenshot on failure et tests responsive sur mobile + desktop.",
            "Pour les backends, couvrir happy path, erreurs de validation, auth/permissions, persistence et contrats OpenAPI quand disponibles.",
            "Terminer avec QualityGateAgent: commandes exactes, criteres d'acceptation, seuils de couverture raisonnables et risques residuels.",
            "Retourner des fichiers de tests et commandes executables, pas seulement des recommandations abstraites.",
        ],
        markdown=True,
    )
