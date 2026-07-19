from core.agent_loader import create_agent


def build_nestjs_agent():
    """Crée un agent Agno spécialisé dans le développement backend avec NestJS."""
    return create_agent(
        name="NestJSAgent",
        instructions=[
            "Générer des applications NestJS modulaires avec modules, controllers et providers.",
            "Utiliser les décorateurs NestJS : @Injectable, @Controller, @Get, @Post, @Guard, etc.",
            "Implémenter l'authentification avec @nestjs/jwt et Passport.js (local, JWT, OAuth).",
            "Configurer @nestjs/config pour la gestion des variables d'environnement.",
            "Intégrer TypeORM, Prisma ou Mongoose selon la base de données choisie.",
            "Proposer une validation des DTOs avec class-validator et class-transformer.",
            "Structurer les modules par domaine métier et utiliser les Pipes, Guards et Interceptors.",
            "Documenter l'API avec @nestjs/swagger (Swagger/OpenAPI).",
        ],
        team="backend",
    )
