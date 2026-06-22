from pydantic import BaseModel


#Crear un modelo Ticket

class Ticket(BaseModel):
    ticket_id: int
    customer_name: str
    customer_email: str
    customer_age: int | None = None
    customer_gender: str | None = None
    product_purchased: str | None = None
    ticket_type: str | None = None
    ticket_status: str | None = None
    ticket_priority: str | None = None