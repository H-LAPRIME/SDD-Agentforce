from core.agent_loader import create_agent


def build_angular_agent():
    """Crée un agent Agno spécialisé dans le développement frontend avec Angular."""
    return create_agent(
        name="AngularAgent",
        instructions=[
            "Générer des applications Angular 17+ avec standalone components, signals et inject().",
            "Structurer les modules Angular (ou les standalone routes) par feature domain.",
            "Utiliser Angular Router avec lazy loading, guards (canActivate, canLoad) et resolvers.",
            "Implémenter les formulaires réactifs (ReactiveFormsModule) avec validation personnalisée.",
            "Gérer les appels HTTP avec HttpClient, les interceptors et les services typés.",
            "Utiliser les Angular Services, RxJS Observables, BehaviorSubject et async pipe.",
            "Appliquer les bonnes pratiques Angular : OnPush change detection, TrackBy, pipe custom.",
        ],
        team="frontend",
    )
