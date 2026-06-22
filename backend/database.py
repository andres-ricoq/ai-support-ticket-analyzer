# SQLAlchemy es la librería que permite trabajar con bases de datos usando Python

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Ruta de SQLite
DATABASE_URL = "sqlite:///tickets.db"


# Motor de conexión
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)


# SessionLocal permite abrir sesiones
# para insertar, consultar y actualizar datos

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)