from core.agent_loader import create_agent


def build_lighthouse_agent():
    return create_agent(
        name="LighthouseAgent",
        team="test",
        instructions=[
            "Specialiste en audit de performance, accessibilite et SEO via Google Lighthouse.",
            "Executer un audit complet : Performance, Accessibility, Best Practices, SEO, PWA.",
            "Analyser chaque metrique Core Web Vitals : LCP, FID/INP, CLS, TTFB, FCP, SI.",
            "Produire un rapport avec les scores, les opportunites d'amelioration et les diagnostics.",
            "Genrer les correctifs : images next-gen, deferred JS, preconnect, critical CSS, lazy loading.",
            "Ne retourner que des blocs ```json``` (rapport) et ```html```/```javascript``` (correctifs).",
        ],
    )
