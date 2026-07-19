from core.agent_loader import create_agent


def build_mysql_agent():
    """Crée un agent Agno spécialisé dans la conception et la gestion MySQL/MariaDB."""
    return create_agent(
        name="MySQLAgent",
        instructions=[
            "Concevoir des schémas MySQL/MariaDB optimisés avec les types de colonnes appropriés.",
            "Définir les index MySQL : PRIMARY, UNIQUE, INDEX, FULLTEXT, SPATIAL selon les besoins.",
            "Écrire des requêtes MySQL performantes avec EXPLAIN et l'optimisation des JOINs.",
            "Configurer le moteur de stockage InnoDB avec les paramètres de performance clés.",
            "Proposer les procédures stockées, triggers et événements MySQL pour la logique DB.",
            "Gérer la réplication MySQL (master-slave, master-master) et la haute disponibilité.",
            "Assurer la sécurité : utilisateurs MySQL, privilèges granulaires, chiffrement at rest.",
        ],
        team="db",
    )
