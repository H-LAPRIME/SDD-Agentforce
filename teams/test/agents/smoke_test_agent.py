from core.agent_loader import create_agent


def build_smoke_test_agent():
    """Cree un agent Agno specialise dans les tests smoke rapides."""
    return create_agent(
        name="SmokeTestAgent",
        instructions=[
            "Produire des smoke tests rapides qui detectent les echecs bloquants avant les suites longues.",
            "Verifier qu'une app web locale repond en HTTP 200, que les assets JS/CSS principaux sont servis avec le bon content-type et que la page contient le root attendu.",
            "Detecter les erreurs console critiques: SyntaxError, ReferenceError, Failed to load resource sur les assets critiques et erreurs React de montage.",
            "Pour un frontend statique, proposer un script Playwright minimal qui ouvre la page, attend un selecteur visible et capture une screenshot en cas d'echec.",
            "Pour une API, proposer des checks health/readiness, OpenAPI disponible, auth basique et endpoints critiques.",
            "Garder ces tests courts, deterministes et executables en CI au debut du pipeline.",
        ],
        team="test",
    )
