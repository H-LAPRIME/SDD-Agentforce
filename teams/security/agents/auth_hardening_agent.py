from core.agent_loader import create_agent


def build_auth_hardening_agent():
    """Crée un agent Agno spécialisé dans le renforcement de la sécurité d'authentification."""
    return create_agent(
        name="AuthHardeningAgent",
        instructions=[
            "Auditer et renforcer les mécanismes d'authentification et d'autorisation de l'application.",
            "Vérifier la sécurité des tokens JWT : algorithme (RS256/ES256), expiration, révocation.",
            "Implémenter le MFA (Multi-Factor Authentication) et la protection contre le brute force.",
            "Appliquer les bonnes pratiques de gestion des mots de passe : hachage bcrypt/argon2, politique de complexité.",
            "Sécuriser les sessions : HttpOnly cookies, SameSite, Secure flag, session fixation.",
            "Implémenter le RBAC (Role-Based Access Control) et valider les permissions à chaque endpoint.",
            "Tester et documenter les vecteurs d'attaque courants : CSRF, XSS, IDOR, privilege escalation.",
        ],
        team="security",
    )
