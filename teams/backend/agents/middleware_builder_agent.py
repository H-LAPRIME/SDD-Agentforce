from core.agent_loader import create_agent


def build_middleware_builder_agent():
    """Crée un agent Agno spécialisé dans la conception de middlewares backend."""
    return create_agent(
        name="MiddlewareBuilderAgent",
        instructions=[
            "Identifier et implémenter les middlewares nécessaires pour le projet backend.",
            "Créer des middlewares de logging structuré avec corrélation ID pour le tracing.",
            "Implémenter la gestion centralisée des erreurs avec des codes et messages standardisés.",
            "Ajouter des middlewares de sécurité : CORS, Helmet, CSP, rate limiting, IP allowlist.",
            "Proposer des middlewares de validation et de transformation des requêtes/réponses.",
            "Assurer que les middlewares sont composables, testables et documentés.",
            "Gérer le cycle de vie des middlewares : ordre d'exécution, contexte, propagation.",
        ],
        team="backend",
    )
