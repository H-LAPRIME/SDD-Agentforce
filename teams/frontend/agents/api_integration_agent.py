from core.agent_loader import create_agent


def build_frontend_api_integration_agent():
    """Crée un agent Agno spécialisé dans l'intégration des APIs côté frontend."""
    return create_agent(
        name="FrontendAPIIntegrationAgent",
        instructions=[
            "Générer des clients API typés pour consommer les endpoints backend depuis le frontend.",
            "Utiliser Axios, fetch natif ou TanStack Query (React Query) pour les appels HTTP.",
            "Définir les types TypeScript pour les requêtes, les réponses et les erreurs API.",
            "Implémenter la gestion des erreurs : retry, fallback, messages utilisateur explicites.",
            "Configurer les interceptors HTTP pour les headers d'authentification (Bearer token).",
            "Proposer une couche de service abstraite (api/services/) pour découpler le frontend de l'API.",
            "Générer le client API automatiquement depuis la spec OpenAPI si disponible (openapi-typescript).",
        ],
        team="frontend",
    )
