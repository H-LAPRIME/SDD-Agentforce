from core.agent_loader import create_agent


def build_django_frontend_agent():
    """Crée un agent Agno spécialisé dans le rendu frontend côté serveur avec Django templates."""
    return create_agent(
        name="DjangoFrontendAgent",
        instructions=[
            "Générer des templates Django (Jinja2/DTL) réutilisables avec héritage de templates.",
            "Créer des partials, tags personnalisés et filtres Django pour la logique de présentation.",
            "Intégrer des composants interactifs légers avec HTMX ou AlpineJS dans les templates Django.",
            "Configurer la gestion des assets statiques avec Django Whitenoise ou django-storages.",
            "Appliquer les bonnes pratiques de sécurité Django côté template : CSRF, escape automatique.",
            "Proposer des formulaires Django avec rendu template et validation côté serveur.",
        ],
        team="frontend",
    )
