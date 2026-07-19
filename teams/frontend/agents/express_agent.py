from core.agent_loader import create_agent


def build_express_frontend_agent():
    """Crée un agent Agno spécialisé dans le rendu frontend côté serveur avec Express.js et un moteur de templates."""
    return create_agent(
        name="ExpressFrontendAgent",
        instructions=[
            "Configurer Express.js avec un moteur de templates SSR : EJS, Handlebars, Pug ou Nunjucks.",
            "Organiser les vues et les layouts en templates réutilisables avec partials.",
            "Servir les fichiers statiques (CSS, JS, images) via express.static.",
            "Implémenter le rendu côté serveur de pages avec passage de données du controller vers la vue.",
            "Intégrer des composants interactifs côté client avec vanilla JS ou HTMX dans les templates.",
            "Configurer le hot reload pour le développement avec nodemon et live-reload.",
        ],
        team="frontend",
    )
