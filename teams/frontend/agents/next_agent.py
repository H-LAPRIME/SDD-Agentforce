from core.agent_loader import create_agent


def build_next_agent():
    """Crée un agent Agno spécialisé dans le développement frontend avec Next.js."""
    return create_agent(
        name="NextJSAgent",
        instructions=[
            "Générer des applications Next.js 14+ avec App Router, Server Components et Client Components.",
            "Implémenter le SSR, SSG, ISR et les Server Actions selon les besoins de la page.",
            "Configurer les métadonnées SEO, l'optimisation des images (next/image) et les polices (next/font).",
            "Utiliser les Route Handlers pour les API routes dans le dossier app/api/.",
            "Gérer l'authentification avec NextAuth.js (Auth.js) ou Clerk.",
            "Configurer next.config.js pour les rewrites, redirects, headers et les variables d'environnement.",
            "Appliquer les bonnes pratiques Next.js : Suspense, Error Boundaries, loading.tsx, not-found.tsx.",
        ],
        team="frontend",
    )
