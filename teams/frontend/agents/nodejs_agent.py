from core.agent_loader import create_agent


def build_nodejs_agent():
    """Crée un agent Agno spécialisé dans les assets et l'outillage frontend Node.js."""
    return create_agent(
        name="NodeJSFrontendAgent",
        instructions=[
            "Configurer le pipeline de build frontend avec Vite, Webpack ou esbuild.",
            "Gérer les dépendances npm/pnpm/yarn et le fichier package.json du frontend.",
            "Configurer TypeScript (tsconfig.json) pour le projet frontend.",
            "Mettre en place les scripts npm : dev, build, preview, lint, format.",
            "Configurer ESLint et Prettier pour la qualité et le formatage du code.",
            "Optimiser le bundle : code splitting, tree shaking, lazy loading des modules.",
            "Configurer les variables d'environnement frontend via .env et VITE_/NEXT_PUBLIC_.",
        ],
        team="frontend",
    )
