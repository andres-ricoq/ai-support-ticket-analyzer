import os
import json
import google.generativeai as genai

from dotenv import load_dotenv

load_dotenv()

genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)

model = genai.GenerativeModel(
    "gemini-2.5-flash"
)


def analyze_ticket(
    ticket_type,
    ticket_subject,
    ticket_description
):
    """
    Analiza un ticket usando Gemini.
    """

    prompt = f"""
    Analyze this support ticket.

    Ticket Type:
    {ticket_type}

    Ticket Subject:
    {ticket_subject}

    Ticket Description:
    {ticket_description}

    Return ONLY valid JSON.

    {{
      "category":"",
      "priority":"",
      "summary":"",
      "sentiment":"",
      "team":""
    }}
    """

    response = model.generate_content(
        prompt
    )

    text = response.text

    # Eliminar markdown si Gemini lo agrega

    text = text.replace(
        "```json",
        ""
    )

    text = text.replace(
        "```",
        ""
    )

    text = text.strip()

    return json.loads(text)

def normalize_category(category):

    category = str(category).strip().lower()

    mapping = {

        "technical support":
            "Technical Support",

        "technical_support":
            "Technical Support",

        "technical issue":
            "Technical Support",

        "technical_issue":
            "Technical Support",

        "hardware issue":
            "Technical Support",

        "connectivity issue":
            "Technical Support",

        "technical support - network connectivity":
            "Technical Support",

        "billing":
            "Billing",

        "billing / subscription":
            "Billing",

        "refund request":
            "Refund Request",

        "account access":
            "Account Access",

        "cancellation":
            "Cancellation",

        "product issue":
            "Product Inquiry",

        "usage/how-to":
            "Product Inquiry"
    }

    return mapping.get(
        category,
        category.title()
    )

def normalize_priority(priority):

    """
    Estandariza prioridades.
    """

    priority = str(priority).strip().lower()

    mapping = {

        "high": "High",

        "medium": "Medium",

        "low": "Low"
    }

    return mapping.get(
        priority,
        priority.title()
    )

def normalize_team(team):

    """
    Estandariza nombres de equipos.
    """

    team = str(team).strip().lower()

    mapping = {

        "technical support":
            "Technical Support",

        "technical_support":
            "Technical Support",

        "billing":
            "Billing",

        "billing team":
            "Billing",

        "customer support":
            "Customer Support",

        "customer service":
            "Customer Support",

        "returns & refunds":
            "Refund Team",

        "refund team":
            "Refund Team"
    }

    return mapping.get(
        team,
        team.title()
    )