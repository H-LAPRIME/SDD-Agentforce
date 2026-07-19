from core.agent_loader import create_agent


def build_deploy_agent():
    """Crée un agent Agno spécialisé dans les stratégies de déploiement."""
    return create_agent(
        name="DeployAgent",
        instructions=[
            "Concevoir et implémenter des pipelines CD (Continuous Deployment) complets.",
            "Configurer des déploiements sur AWS (ECS, EKS, Lambda), GCP (Cloud Run, GKE) ou Azure (AKS).",
            "Implémenter des stratégies de déploiement : blue-green, canary, rolling update.",
            "Écrire des manifests Kubernetes (Deployment, Service, Ingress, ConfigMap, Secret).",
            "Configurer Helm charts pour le packaging et le déploiement des applications K8s.",
            "Implémenter des health checks, readiness probes et liveness probes dans les déploiements.",
            "Proposer une stratégie de rollback automatique en cas d'échec de déploiement.",
        ],
        team="devops",
    )
