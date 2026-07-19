from core.agent_loader import create_agent


def build_pytest_agent():
    """Crée un agent Agno spécialisé dans l'écriture de tests avec Pytest."""
    return create_agent(
        name="PytestAgent",
        instructions=[
            "Écrire des tests unitaires et d'intégration Python avec Pytest.",
            "Utiliser les fixtures Pytest pour préparer et nettoyer les données de test.",
            "Implémenter les mocks et les patches avec unittest.mock ou pytest-mock.",
            "Configurer pytest.ini / pyproject.toml pour les marqueurs, coverage et les plugins.",
            "Écrire des tests paramétrés avec @pytest.mark.parametrize pour couvrir les cas limites.",
            "Configurer pytest-cov pour le rapport de couverture de code (coverage HTML, XML).",
            "Proposer des tests d'intégration avec des bases de données de test isolées (TestContainers).",
        ],
        team="test",
    )
