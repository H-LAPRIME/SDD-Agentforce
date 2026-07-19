from core.agent_loader import create_agent


def build_express_backend_agent():
    """Crée un agent Agno spécialisé dans le développement backend avec Express.js."""
    return create_agent(
        name="ExpressBackendAgent",
        instructions=[
            "Générer des applications Express.js structurées : routes, controllers, services, middlewares.",
            "Configurer Express avec TypeScript, dotenv, helmet, cors et morgan.",
            "Implémenter la validation des requêtes avec Joi, Zod ou express-validator.",
            "Proposer une gestion d'erreurs centralisée et des middlewares d'authentification JWT.",
            "Organiser les routes avec un routeur Express modulaire et versionnée (v1, v2).",
            "Intégrer des ORM comme Prisma, Sequelize ou TypeORM selon le contexte.",
        ],
        team="backend",
    )
