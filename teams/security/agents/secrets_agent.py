from core.agent_loader import create_agent


def build_secrets_agent():
    """Crée un agent Agno spécialisé dans la gestion sécurisée des secrets."""
    return create_agent(
        name="SecretsAgent",
        instructions=[
            "Auditer le code source pour détecter les secrets codés en dur (API keys, passwords, tokens).",
            "Configurer un gestionnaire de secrets : HashiCorp Vault, AWS Secrets Manager, Azure Key Vault.",
            "Implémenter la rotation automatique des secrets et des clés API.",
            "Configurer git-secrets ou detect-secrets pour prévenir les commits avec des secrets.",
            "Proposer l'utilisation de variables d'environnement avec des fichiers .env.example documentés.",
            "Chiffrer les secrets au repos et en transit, et auditer les accès aux secrets.",
            "Documenter la politique de gestion des secrets et le processus d'onboarding sécurisé.",
        ],
        team="security",
    )
