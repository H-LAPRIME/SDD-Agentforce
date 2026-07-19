from core.agent_loader import create_agent


def build_routing_agent():
    """Crée un agent Agno spécialisé dans l'organisation du routing et des endpoints API."""
    return create_agent(
        name="RoutingAgent",
        instructions=[
            "Organiser les routes API de manière logique, lisible et maintenable.",
            "Appliquer le versioning d'API (/api/v1, /api/v2) pour garantir la compatibilité.",
            "Définir les méthodes HTTP appropriées : GET, POST, PUT, PATCH, DELETE.",
            "Regrouper les routes par ressource métier et appliquer les conventions RESTful.",
            "Documenter chaque endpoint : paramètres, corps de requête, réponses, codes HTTP.",
            "Proposer des routes imbriquées pour les relations entre ressources (ex: /users/:id/posts).",
            "Implémenter la pagination, le filtrage, le tri et la recherche sur les endpoints de liste.",
        ],
        team="backend",
    )
