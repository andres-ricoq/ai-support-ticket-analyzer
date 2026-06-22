# backend/models_db.py

from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String

from sqlalchemy.orm import declarative_base

# Base es la clase padre
# de todas las tablas que creemos

Base = declarative_base()


class TicketDB(Base):

    # Nombre de la tabla en SQLite

    __tablename__ = "tickets"

    # Columnas

    id = Column(Integer, primary_key=True)

    ticket_id = Column(Integer)

    customer_name = Column(String)

    customer_email = Column(String)

    ticket_type = Column(String)

    ticket_subject = Column(String)

    ticket_description = Column(String)

    ticket_status = Column(String)

    ticket_priority = Column(String)
    
    # Campos IA
    # Los llenaremos más adelante

    ai_category = Column(String)

    ai_priority = Column(String)

    ai_summary = Column(String)

    ai_sentiment = Column(String)

    ai_team = Column(String)