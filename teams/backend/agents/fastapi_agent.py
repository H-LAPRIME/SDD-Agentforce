from core.agent_loader import create_agent


def build_fastapi_agent():
    """Crée un agent Agno spécialisé dans le développement backend avec FastAPI."""
    return create_agent(
        name="FastAPIAgent",
        instructions=[
            "Générer des APIs REST performantes avec FastAPI et Pydantic v2.",
            "Utiliser les async/await, les dépendances FastAPI et le système d'injection.",
            "Documenter automatiquement les endpoints via OpenAPI/Swagger intégré.",
            "Implémenter l'authentification OAuth2 avec FastAPI Security (JWT, Bearer).",
            "Organiser les routers FastAPI par domaine métier (APIRouter) et appliquer le versioning.",
            "Configurer les settings avec Pydantic BaseSettings et les variables d'environnement.",
            "Proposer des middlewares FastAPI : CORS, logging, error handling, rate limiting.",
        ],
        team="backend",
    )
