# AgentForge — Structure de projet (Agno)

## 1. Arborescence

```
agentforge/
├── project_agent.py                    # Orchestrateur racine — route vers les teams
│
├── core/
│   ├── agent_loader.py                 # Charge et instancie les agents dynamiquement
│   └── tool_registry.py               # Enregistre les tools disponibles par agent
│
├── teams/
│   ├── frontend/
│   │   ├── frontend_team.py           # Orchestrateur team frontend
│   │   ├── agents/
│   │   │   ├── react_agent.py
│   │   │   ├── next_agent.py
│   │   │   ├── angular_agent.py
│   │   │   ├── django_agent.py        # (si SSR/templates front)
│   │   │   ├── nodejs_agent.py
│   │   │   ├── express_agent.py
│   │   │   ├── bootstrap_agent.py
│   │   │   ├── tailwind_agent.py
│   │   │   ├── component_builder_agent.py   # transverse
│   │   │   ├── ui_architect_agent.py        # transverse
│   │   │   └── api_integration_agent.py     # transverse
│   │   └── prompts/
│   │
│   ├── backend/
│   │   ├── backend_team.py            # Orchestrateur team backend
│   │   ├── agents/
│   │   │   ├── express_agent.py
│   │   │   ├── nestjs_agent.py
│   │   │   ├── django_agent.py
│   │   │   ├── flask_agent.py
│   │   │   ├── fastapi_agent.py
│   │   │   ├── spring_agent.py
│   │   │   ├── gin_agent.py
│   │   │   ├── auth_agent.py                # transverse
│   │   │   ├── routing_agent.py             # transverse
│   │   │   ├── models_agent.py              # transverse
│   │   │   ├── middleware_builder_agent.py  # transverse
│   │   │   ├── backend_structure_agent.py   # transverse
│   │   │   └── api_integration_agent.py     # transverse
│   │   └── prompts/
│   │
│   ├── db/
│   │   ├── db_team.py                 # Orchestrateur team base de données
│   │   ├── agents/
│   │   │   ├── postgres_agent.py
│   │   │   ├── mysql_agent.py
│   │   │   ├── sqlite_agent.py
│   │   │   ├── mongo_agent.py
│   │   │   ├── redis_agent.py
│   │   │   ├── faiss_vector_agent.py
│   │   │   ├── orm_agent.py                 # transverse
│   │   │   ├── migration_agent.py           # transverse
│   │   │   └── schema_designer_agent.py     # transverse
│   │   └── prompts/
│   │
│   ├── test/
│   │   ├── test_team.py               # Orchestrateur team tests
│   │   ├── agents/
│   │   │   ├── pytest_agent.py
│   │   │   ├── jest_agent.py
│   │   │   ├── playwright_agent.py
│   │   │   └── selenium_agent.py
│   │   └── prompts/
│   │
│   ├── doc/
│   │   ├── doc_team.py                # Orchestrateur team documentation
│   │   ├── agents/
│   │   │   ├── readme_agent.py
│   │   │   ├── openapi_agent.py
│   │   │   └── architecture_agent.py
│   │   └── prompts/
│   │
│   ├── devops/
│   │   ├── devops_team.py             # Orchestrateur team DevOps
│   │   ├── agents/
│   │   │   ├── docker_agent.py
│   │   │   ├── ci_agent.py
│   │   │   └── deploy_agent.py
│   │   └── prompts/
│   │
│   └── security/
│       ├── security_team.py           # Orchestrateur team sécurité
│       ├── agents/
│       │   ├── auth_hardening_agent.py
│       │   └── secrets_agent.py
│       └── prompts/
│
├── specs/
│   ├── outcomes/                      # Résultats attendus (ODD)
│   ├── nodes/                         # Noeuds de spécification (SDD)
│   └── detected_stack.yaml            # Stack détecté automatiquement
│
├── tests/
├── .env.example
├── requirements.txt
└── README.md
```


### Objectif
AgentForge orchestre des agents Agno pour générer une application fullstack complète à partir d'une requête en langage naturel.

### Flux principal
1. **project_agent** reçoit la requête utilisateur.
2. **project_agent** analyse la requête et détecte le stack technique (`detected_stack.yaml`).
3. **project_agent** route vers les **teams** concernées (frontend / backend / db / test / doc / devops / security).
4. Chaque **team orchestrator** sélectionne les agents *engine-specific* (ex: `react_agent`, `express_agent`) et les agents *transverses* (ex: `auth_agent`, `routing_agent`) pertinents.
5. Les agents génèrent le code / les specs, remontés au **project_agent** pour assemblage final.
