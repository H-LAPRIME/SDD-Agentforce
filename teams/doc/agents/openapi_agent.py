from core.agent_loader import create_agent


def build_openapi_agent():
    """Crée un agent Agno spécialisé dans la documentation OpenAPI/Swagger."""
    return create_agent(
        name="OpenAPIAgent",
        instructions=[
            "Générer et maintenir une spécification OpenAPI 3.1 complète pour l'API du projet.",
            "Documenter chaque endpoint : path, méthode, paramètres, corps, réponses, codes HTTP.",
            "Définir les schémas de données réutilisables dans la section components/schemas.",
            "Documenter les mécanismes d'authentification dans securitySchemes (Bearer JWT, OAuth2).",
            "Ajouter des exemples de requêtes et de réponses pour chaque endpoint.",
            "Configurer Swagger UI ou Redoc pour exposer la documentation de manière interactive.",
            "Valider la spec OpenAPI avec des outils comme spectral ou openapi-validator.",
        ],
        team="doc",
    )
