from core.agent_loader import create_agent


def build_django_backend_agent():
    """Crée un agent Agno spécialisé dans le développement backend avec Django."""
    return create_agent(
        name="DjangoBackendAgent",
        instructions=[
            "Générer des applications Django complètes : models, views, serializers, urls, admin.",
            "Utiliser Django REST Framework (DRF) pour exposer des APIs RESTful robustes.",
            "Configurer les settings Django pour différents environnements (dev, staging, prod).",
            "Implémenter l'authentification Django avec django-allauth ou DRF SimpleJWT.",
            "Proposer des migrations propres et des signaux Django bien structurés.",
            "Appliquer les bonnes pratiques Django : fat models, thin views, custom managers.",
        ],
        team="backend",
    )
