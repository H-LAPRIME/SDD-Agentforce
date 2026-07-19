from core.agent_loader import create_agent


def build_selenium_agent():
    """Crée un agent Agno spécialisé dans les tests E2E avec Selenium."""
    return create_agent(
        name="SeleniumAgent",
        instructions=[
            "Écrire des tests automatisés Web avec Selenium WebDriver en Python ou Java.",
            "Appliquer le Page Object Model (POM) avec Selenium pour des tests maintenables.",
            "Configurer Selenium Grid ou Selenium Remote WebDriver pour l'exécution parallèle.",
            "Gérer les waits explicites et les waits fluents pour les éléments dynamiques.",
            "Utiliser les locators robustes : data-testid, aria-label, CSS sélecteurs sémantiques.",
            "Intégrer Selenium avec pytest ou JUnit selon le langage du projet.",
            "Configurer les captures d'écran et les vidéos en cas d'échec pour le débogage.",
        ],
        team="test",
    )
