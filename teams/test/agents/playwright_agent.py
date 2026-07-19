from core.agent_loader import create_agent


def build_playwright_agent():
    """Crée un agent Agno spécialisé dans les tests E2E avec Playwright."""
    return create_agent(
        name="PlaywrightAgent",
        instructions=[
            "Écrire des tests End-to-End avec Playwright en TypeScript ou Python.",
            "Utiliser le Page Object Model (POM) pour organiser et réutiliser la logique de navigation.",
            "Configurer playwright.config.ts : navigateurs, retries, reporters, base URL, screenshots.",
            "Implémenter des tests de navigation, de formulaires, d'authentification et de flux utilisateur.",
            "Utiliser les locators Playwright (role, text, testId) robustes et résistants aux changements.",
            "Configurer les fixtures Playwright pour l'état de connexion et les préconditions.",
            "Générer des rapports HTML Playwright et intégrer les screenshots en cas d'échec.",
        ],
        team="test",
    )
