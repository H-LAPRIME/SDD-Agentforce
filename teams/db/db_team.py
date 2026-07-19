from agno.team import Team
from agno.team.mode import TeamMode

from core.agent_loader import get_model
from teams.db.agents.postgres_agent import build_postgres_agent
from teams.db.agents.mysql_agent import build_mysql_agent
from teams.db.agents.sqlite_agent import build_sqlite_agent
from teams.db.agents.mongo_agent import build_mongo_agent
from teams.db.agents.redis_agent import build_redis_agent
from teams.db.agents.faiss_vector_agent import build_faiss_vector_agent
from teams.db.agents.orm_agent import build_orm_agent
from teams.db.agents.migration_agent import build_migration_agent
from teams.db.agents.schema_designer_agent import build_schema_designer_agent


def build_db_team(mode: TeamMode = TeamMode.route) -> Team:
    """Construit une équipe Agno orientée conception et gestion des bases de données."""
    members = [
        build_schema_designer_agent(),
        build_orm_agent(),
        build_migration_agent(),
        build_postgres_agent(),
        build_mysql_agent(),
        build_sqlite_agent(),
        build_mongo_agent(),
        build_redis_agent(),
        build_faiss_vector_agent(),
    ]

    return Team(
        name="Database Engineering Team",
        description="Équipe Agno spécialisée dans la conception, la gestion et l'optimisation des bases de données.",
        mode=mode,  # Route vers le spécialiste DB exact : Postgres, Mongo, Redis...
        model=get_model(role="team", team="db"),
        members=members,
        instructions=[
            "Coordonner le travail de modélisation et d'accès aux données.",
            "Choisir le bon type de base de données selon les besoins : SQL, NoSQL, vectoriel, cache.",
            "Produire des schémas cohérents, des migrations réversibles et des requêtes optimisées.",
            "En mode bridge, agrèger une réponse directe sans tenter de reformuler le plan.",
        ],
        markdown=True,
    )
