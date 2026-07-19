from core.agent_loader import create_agent


def build_api_integration_agent():
    """Crée un agent Agno spécialisé dans l'intégration d'API backend."""
    return create_agent(
        name="APIIntegrationAgent",
        instructions=[
            "Concevoir et documenter des intégrations API backend propres et testables.",
            "Privilégier des contrats clairs, des timeouts, des retries et un mapping d'erreurs explicite.",
            "Proposer si besoin des schémas compatibles OpenAPI et des tests de bout en bout.",
        ],
        team="backend",
    )
