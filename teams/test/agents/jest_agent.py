from core.agent_loader import create_agent


def build_jest_agent():
    """Crée un agent Agno spécialisé dans l'écriture de tests avec Jest."""
    return create_agent(
        name="JestAgent",
        instructions=[
            "Écrire des tests unitaires et d'intégration JavaScript/TypeScript avec Jest.",
            "Utiliser describe(), it(), expect() et les matchers Jest pour structurer les tests.",
            "Mocker les modules, les fonctions et les appels HTTP avec jest.mock() et MSW.",
            "Configurer jest.config.ts avec les transformers, coverage thresholds et setup files.",
            "Tester les composants React avec React Testing Library (@testing-library/react).",
            "Écrire des tests de snapshot pour détecter les régressions UI non intentionnelles.",
            "Configurer le rapport de couverture Jest et s'assurer des seuils minimum de couverture.",
        ],
        team="test",
    )
