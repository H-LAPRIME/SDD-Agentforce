from core.agent_loader import create_agent


def build_docker_agent():
    """Crée un agent Agno spécialisé dans la conteneurisation Docker."""
    return create_agent(
        name="DockerAgent",
        instructions=[
            "Créer des Dockerfiles optimisés avec des images de base légères (alpine, distroless).",
            "Utiliser le multi-stage build pour minimiser la taille des images Docker de production.",
            "Écrire des fichiers docker-compose.yml pour orchestrer les services de développement local.",
            "Configurer les volumes, réseaux et variables d'environnement dans docker-compose.",
            "Appliquer les bonnes pratiques Docker : non-root user, COPY vs ADD, layer caching.",
            "Créer un .dockerignore complet pour exclure les fichiers inutiles du contexte de build.",
            "Tagger et publier les images Docker sur un registry (Docker Hub, GHCR, ECR).",
        ],
        team="devops",
    )
