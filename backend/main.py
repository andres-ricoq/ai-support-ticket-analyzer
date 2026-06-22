from fastapi import FastAPI
from backend.services.data_cleaner import load_and_clean_data
from backend.database import engine
from backend.models_db import Base
from backend.database import SessionLocal
from backend.models_db import TicketDB
from backend.services.ai_service import analyze_ticket
import os
import google.generativeai as genai
from pydantic import BaseModel
from backend.services.rag_service import (
    load_knowledge_base,
    build_ticket_context,
    answer_question
)
from backend.services.ai_service import (
    normalize_category,
    normalize_priority,
    normalize_team
)

from dotenv import load_dotenv

class AskRequest(BaseModel):
    question: str

# Cargar variables del archivo .env

load_dotenv()

# Obtener API Key

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Configurar Gemini

genai.configure(
    api_key=GEMINI_API_KEY
)

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AI Support Ticket Analyzer",
    version="1.0"
)

@app.get("/")
def home():
    return {
        "message": "API funcionando correctamente"
    }

#Tickets

@app.get("/tickets")
def get_tickets():

    df = load_and_clean_data()

    return df.head(20).to_dict(orient="records")


#Resumen

@app.get("/summary")
def get_summary():

    df = load_and_clean_data()

    return {
        "total_tickets": len(df),
        "total_columns": len(df.columns),
        "ticket_status": df["Ticket Status"].value_counts().to_dict(),
        "ticket_priority": df["Ticket Priority"].value_counts().to_dict(),
        "ticket_channel": df["Ticket Channel"].value_counts().to_dict()
    }


@app.post("/ingest")
def ingest_tickets():

    try:

        # Obtener datos limpios
        df = load_and_clean_data()

        # Abrir conexión
        db = SessionLocal()

        inserted = 0

        for _, row in df.iterrows():

            ticket = TicketDB(
                ticket_id=row["Ticket ID"],
                customer_name=row["Customer Name"],
                customer_email=row["Customer Email"],
                ticket_type=row["Ticket Type"],
                ticket_status=row["Ticket Status"],
                ticket_priority=row["Ticket Priority"],
                ticket_subject=row["Ticket Subject"],
                ticket_description=row["Ticket Description"]
            )

            db.add(ticket)

            inserted += 1

        db.commit()

        return {
            "message": "Tickets cargados correctamente",
            "tickets_inserted": inserted
        }

    except Exception as e:

        return {
            "error": str(e)
        }

    finally:

        if db:
            db.close()

@app.get("/tickets_db")
def get_tickets_db():

    db = SessionLocal()

    tickets = db.query(TicketDB).limit(5).all()

    result = []

    for ticket in tickets:

        result.append({
            "ticket_id": ticket.ticket_id,
            "ticket_type": ticket.ticket_type,
            "ticket_subject": ticket.ticket_subject,
            "ticket_description": ticket.ticket_description,
            "category": ticket.ai_category
        })

    db.close()

    return result

#ia
@app.post("/analyze")
def analyze_all_tickets():

    """
    Analiza todos los tickets pendientes
    utilizando Gemini.
    """

    db = None

    try:

        # Abrir conexión con SQLite
        db = SessionLocal()

        # Solo tickets pendientes de analizar
        tickets = db.query(TicketDB).filter(
            TicketDB.ai_category == None
        ).all()

        print(
            f"Tickets encontrados: {len(tickets)}"
        )

        if len(tickets) > 0:

            print(
                f"Primer ticket pendiente: {tickets[0].ticket_id}"
            )

        analyzed = 0

        # Recorrer tickets pendientes
        for ticket in tickets:

            try:

                print(
                    f"Analizando ticket {ticket.ticket_id}"
                )

                # Llamada al servicio de IA
                result = analyze_ticket(
                    ticket.ticket_type,
                    ticket.ticket_subject,
                    ticket.ticket_description
                )

                # Normalizar resultados
                result["category"] = normalize_category(
                    result["category"]
                )

                result["priority"] = normalize_priority(
                    result["priority"]
                )

                result["team"] = normalize_team(
                    result["team"]
                )

                # Guardar resultados IA
                ticket.ai_category = result["category"]
                ticket.ai_priority = result["priority"]
                ticket.ai_summary = result["summary"]
                ticket.ai_sentiment = result["sentiment"]
                ticket.ai_team = result["team"]

                analyzed += 1

            except Exception as e:

                # Si falla un ticket,
                # continuamos con el siguiente
                print(
                    f"Error ticket {ticket.ticket_id}: {e}"
                )

        # Guardar cambios en SQLite
        db.commit()

        return {
            "message": "Tickets analizados correctamente",
            "tickets_analyzed": analyzed
        }

    except Exception as e:

        return {
            "error": str(e)
        }

    finally:

        # Cerrar conexión siempre
        if db:
            db.close()


@app.get("/analyzed_tickets")
def analyzed_tickets():

    db = SessionLocal()

    # Quitamos el limit para obtener todos los tickets
    tickets = db.query(TicketDB).all()

    result = []

    for ticket in tickets:

        result.append({

            # Información original
            "ticket_id": ticket.ticket_id,
            "customer_name": ticket.customer_name,
            "customer_email": ticket.customer_email,
            "ticket_type": ticket.ticket_type,
            "ticket_status": ticket.ticket_status,

            # Información IA
            "category": ticket.ai_category,
            "priority": ticket.ai_priority,
            "summary": ticket.ai_summary,
            "sentiment": ticket.ai_sentiment,
            "team": ticket.ai_team
        })

    db.close()

    return result


@app.get("/analytics")
def analytics():

    db = SessionLocal()

    tickets = db.query(TicketDB).all()

    total_tickets = len(tickets)

    # Contadores
    category_count = {}
    priority_count = {}
    team_count = {}

    for ticket in tickets:

        # Categorías
        category = ticket.ai_category or "Pending Analysis"
        category_count[category] = category_count.get(category, 0) + 1

        # Prioridades
        priority = ticket.ai_priority or "Pending Analysis"
        priority_count[priority] = priority_count.get(priority, 0) + 1

        # Equipos
        team = ticket.ai_team or "Pending Analysis"
        team_count[team] = team_count.get(team, 0) + 1

    db.close()

    return {
        "total_tickets": total_tickets,
        "categories": category_count,
        "priorities": priority_count,
        "teams": team_count
    }


@app.get("/test_gemini")
def test_gemini():

    model = genai.GenerativeModel(
        "gemini-2.5-flash"
    )

    response = model.generate_content(
        "Responde únicamente: Gemini conectado correctamente"
    )

    return {
        "response": response.text
    }


@app.get("/test_real_ticket")
def test_real_ticket():

    db = SessionLocal()

    ticket = db.query(TicketDB).first()

    db.close()

    result = analyze_ticket(
        ticket.ticket_type,
        ticket.ticket_subject,
        ticket.ticket_description
    )

    return result

#cuantos tickets faltan
@app.get("/pending_tickets")
def pending_tickets():

    db = SessionLocal()

    pending = db.query(TicketDB).filter(
        TicketDB.ai_category == None
    ).count()

    db.close()

    return {
        "pending_tickets": pending
    }

#RAG
@app.post("/ask")
def ask_question(request: AskRequest):

    try:

        db = SessionLocal()

        stats = build_ticket_context(db)

        kb = load_knowledge_base()

        answer = answer_question(
            request.question,
            stats,
            kb
        )

        return {
            "answer": answer
        }

    except Exception as e:

        return {
            "error": str(e)
        }

    finally:

        if db:
            db.close()
