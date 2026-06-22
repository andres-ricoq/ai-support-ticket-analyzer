# backend/services/rag_service.py

from pathlib import Path


def load_knowledge_base():
    """
    Lee la base de conocimiento.
    """

    kb_path = Path(
        "knowledge_base/support_policies.md"
    )

    with open(
        kb_path,
        "r",
        encoding="utf-8"
    ) as f:

        return f.read()
    
#función para estadísticas

def build_ticket_context(db):

    """
    Genera estadísticas simples
    sobre los tickets analizados.
    """

    from backend.models_db import TicketDB

    tickets = db.query(TicketDB).all()

    total_tickets = len(tickets)

    categories = {}

    priorities = {}

    teams = {}

    for ticket in tickets:

        if ticket.ai_category:

            categories[ticket.ai_category] = (
                categories.get(
                    ticket.ai_category,
                    0
                ) + 1
            )

        if ticket.ai_priority:

            priorities[ticket.ai_priority] = (
                priorities.get(
                    ticket.ai_priority,
                    0
                ) + 1
            )

        if ticket.ai_team:

            teams[ticket.ai_team] = (
                teams.get(
                    ticket.ai_team,
                    0
                ) + 1
            )

    return {
        "total_tickets": total_tickets,
        "categories": categories,
        "priorities": priorities,
        "teams": teams
    }


def answer_question(question, stats, knowledge_base):

    question = question.lower()

    # Categorías

    if "category" in question:

        if len(stats["categories"]) == 0:

            return "No categories available."

        top_category = max(
            stats["categories"],
            key=stats["categories"].get
        )

        return (
            f"The category with the most tickets is "
            f"{top_category} "
            f"with {stats['categories'][top_category]} tickets."
        )

    # Prioridad

    elif "high priority" in question:

        high_count = (
            stats["priorities"].get("High", 0)
            +
            stats["priorities"].get("high", 0)
        )

        return (
            f"There are {high_count} high priority tickets."
        )

    # Equipos

    elif "team" in question:

        return (
            f"Teams currently handling tickets: "
            f"{', '.join(stats['teams'].keys())}"
        )

    # SLA

    elif "sla" in question:

        sla_section = knowledge_base.split("SLA")[-1]

        return sla_section

    # Billing

    elif "billing" in question:

        return (
            "Billing Team handles billing inquiries, "
            "subscription issues and payment failures."
        )

    # Refund

    elif "refund" in question:

        return (
            "Refund Team handles refund requests "
            "and charge disputes."
        )

    return (
        "I could not answer that question yet. "
        "Try asking about categories, priorities, teams, "
        "billing, refunds or SLA."
    )