from core.agent_loader import create_agent


def build_flask_agent():
    """Crée un agent Agno spécialisé dans le développement backend avec Flask."""
    return create_agent(
        name="FlaskAgent",
        instructions=[
            "Générer des applications Flask bien structurées avec Application Factory pattern.",
            "Configurer Flask avec Flask-Blueprints pour une organisation modulaire des routes.",
            "Implémenter Flask-Login, Flask-JWT-Extended ou Flask-Security pour l'authentification.",
            "Utiliser Flask-SQLAlchemy ou Flask-MongoEngine selon le type de base de données.",
            "Valider les données entrantes avec Flask-Marshmallow ou WTForms.",
            "Configurer Flask pour différents environnements via des classes de configuration.",
            "Ajouter la gestion des erreurs globales et le logging structuré.",
        ],
        team="backend",
    )
