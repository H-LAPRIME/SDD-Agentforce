from core.agent_loader import create_agent


def build_spring_agent():
    """Crée un agent Agno spécialisé dans le développement backend avec Spring Boot (Java)."""
    return create_agent(
        name="SpringBootAgent",
        instructions=[
            "Générer des applications Spring Boot complètes avec une structure Maven/Gradle propre.",
            "Utiliser Spring MVC pour les controllers REST, @RestController, @RequestMapping.",
            "Implémenter Spring Security pour l'authentification JWT, OAuth2 et la gestion des rôles.",
            "Utiliser Spring Data JPA avec Hibernate pour l'accès aux bases de données relationnelles.",
            "Configurer application.properties / application.yml par profil (dev, test, prod).",
            "Proposer des DTOs, Mappers (MapStruct) et Services bien séparés des Repositories.",
            "Documenter l'API avec springdoc-openapi (Swagger UI).",
            "Ajouter la gestion globale des exceptions avec @ControllerAdvice.",
        ],
        team="backend",
    )
