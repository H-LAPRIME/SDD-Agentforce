from core.agent_loader import create_agent


def build_gin_agent():
    """Crée un agent Agno spécialisé dans le développement backend avec Gin (Go)."""
    return create_agent(
        name="GinAgent",
        instructions=[
            "Générer des APIs performantes avec le framework Gin en Go.",
            "Structurer les projets Go selon les conventions : cmd/, internal/, pkg/, api/.",
            "Implémenter les middlewares Gin : auth JWT, CORS, logging, rate limiting, recovery.",
            "Utiliser GORM ou sqlx pour l'accès aux bases de données PostgreSQL/MySQL.",
            "Valider les requêtes avec go-playground/validator et les binding Gin.",
            "Documenter l'API avec swaggo/swag pour la génération OpenAPI automatique.",
            "Proposer des patterns Go idiomatiques : interfaces, error wrapping, context propagation.",
        ],
        team="backend",
    )
