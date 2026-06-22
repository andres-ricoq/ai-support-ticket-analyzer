# AI Support Ticket Analyzer

## Descripción

AI Support Ticket Analyzer es una aplicación desarrollada para analizar tickets de soporte utilizando Inteligencia Artificial.

El sistema permite:

* Ingerir y limpiar datos de tickets desde un archivo CSV.
* Almacenar los tickets en una base de datos SQLite.
* Analizar tickets mediante Gemini para generar:

  * Categoría.
  * Prioridad.
  * Resumen.
  * Sentimiento.
  * Equipo responsable.
* Consultar métricas agregadas mediante una API FastAPI.
* Visualizar resultados en un dashboard interactivo desarrollado con Streamlit.
* Realizar preguntas sobre los tickets y políticas de soporte mediante un endpoint tipo RAG simplificado.

---

## Características

* Ingesta y limpieza de tickets desde CSV.
* Persistencia en SQLite mediante SQLAlchemy.
* Clasificación automática de tickets con Gemini.
* Generación de prioridad, resumen y sentimiento.
* Asignación automática del equipo responsable.
* Dashboard interactivo desarrollado con Streamlit.
* Métricas agregadas mediante FastAPI.
* Consultas sobre tickets y políticas mediante un enfoque RAG simplificado.

---

## Arquitectura

```text
CSV Dataset
     ↓
Data Cleaning
     ↓
SQLite Database
     ↓
FastAPI Backend
     ↓
Gemini Analysis
     ↓
Dashboard (Streamlit)
```

---

## Tecnologías Utilizadas

### Backend

* FastAPI
* SQLAlchemy
* SQLite

### Inteligencia Artificial

* Google Gemini 2.5 Flash

### Dashboard

* Streamlit
* Plotly
* Pandas

### Configuración

* Python 3.11+
* python-dotenv

---

## Estructura del Proyecto

```text
ai-support-ticket-analyzer/

├── backend/
│   ├── services/
│   │   ├── ai_service.py
│   │   ├── data_cleaner.py
│   │   └── rag_service.py
│   │
│   ├── database.py
│   ├── main.py
│   ├── models.py
│   └── models_db.py
│
├── dashboard/
│   └── app.py
│
├── dataset/
│   └── tickets.csv
│
├── knowledge_base/
│   └── support_policies.md
│
├── requirements.txt
├── .gitignore
└── README.md
```

---

## Instalación

### 1. Clonar el repositorio

```bash
git clone <repository_url>
cd ai-support-ticket-analyzer
```

### 2. Crear entorno virtual

```bash
python -m venv venv
```

Windows:

```bash
venv\Scripts\activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

---

## Variables de Entorno

Crear un archivo `.env` en la raíz del proyecto:

```env
GEMINI_API_KEY=YOUR_API_KEY
```

---

## Cómo Ejecutar el Backend

Desde la raíz del proyecto:

```bash
uvicorn backend.main:app --reload
```

La API estará disponible en:

```text
http://127.0.0.1:8000
```

Documentación Swagger:

```text
http://127.0.0.1:8000/docs
```

---

## Cómo Ejecutar el Dashboard

En una segunda terminal:

```bash
streamlit run dashboard/app.py
```

El dashboard estará disponible en:

```text
http://localhost:8501
```

---

## Flujo de Prueba Recomendado

### 1. Ingerir tickets

```http
POST /ingest
```

Carga los tickets limpios desde el CSV hacia SQLite.

---

### 2. Analizar tickets con IA

```http
POST /analyze
```

Analiza los tickets pendientes utilizando Gemini.

---

### 3. Consultar métricas

```http
GET /analytics
```

Devuelve:

* Categorías.
* Prioridades.
* Equipos responsables.
* Total de tickets.

---

### 4. Abrir dashboard

```text
http://localhost:8501
```

Permite visualizar:

* KPIs.
* Categorías.
* Prioridades.
* Filtros.
* Tickets analizados.

---

### 5. Realizar preguntas

```http
POST /ask
```

Ejemplo:

```json
{
  "question": "What category has the most tickets?"
}
```

---

## Endpoints Principales

| Método | Endpoint          | Descripción                         |
| ------ | ----------------- | ----------------------------------- |
| GET    | /                 | Health Check                        |
| POST   | /ingest           | Carga tickets en SQLite             |
| POST   | /analyze          | Analiza tickets con IA              |
| GET    | /tickets_db       | Consulta tickets almacenados        |
| GET    | /analyzed_tickets | Consulta resultados IA              |
| GET    | /analytics        | Métricas agregadas                  |
| POST   | /ask              | Preguntas sobre tickets y políticas |

---

## Decisiones Técnicas

### FastAPI

Se eligió FastAPI por su simplicidad, velocidad de desarrollo y documentación automática mediante Swagger.

### SQLite

Se utilizó SQLite por ser una base de datos ligera, suficiente para el volumen de datos de esta prueba técnica.

### Gemini

Se utilizó Gemini 2.5 Flash para enriquecer los tickets mediante clasificación, priorización, resumen y asignación de equipos.

### Streamlit

Se utilizó Streamlit para construir rápidamente un dashboard interactivo sin necesidad de desarrollar un frontend tradicional.

### Knowledge Base

Se implementó una base de conocimiento simple utilizando un archivo Markdown para soportar consultas tipo RAG simplificado.

---

## Uso de IA Durante el Desarrollo

Durante el desarrollo del proyecto utilicé ChatGPT como asistente técnico para acelerar tareas de implementación, depuración y documentación.

### Actividades apoyadas por IA

* Diseño inicial de la arquitectura del proyecto.
* Estructuración de carpetas y módulos.
* Generación y refactorización de endpoints FastAPI.
* Construcción del dashboard en Streamlit.
* Diseño del flujo de preguntas basado en una Knowledge Base.
* Identificación y corrección de errores de SQLAlchemy, Streamlit y FastAPI.

### Validación Manual

Todo el código generado fue revisado y probado manualmente.

Se realizaron validaciones sobre:

* Funcionamiento de endpoints.
* Persistencia en SQLite.
* Integración con Gemini.
* Resultados de clasificación.
* Consistencia de métricas.
* Visualizaciones del dashboard.

### Enfoque

La IA fue utilizada como herramienta de productividad y asistencia técnica.

Las decisiones de arquitectura, selección de tecnologías, pruebas y validación final fueron realizadas manualmente.

---

## Cómo se Trabajaron los Datos

El dataset contiene inconsistencias intencionales.

Durante la etapa de limpieza se realizaron acciones como:

* Normalización de texto.
* Eliminación de valores problemáticos.
* Conversión de tipos.
* Manejo de valores faltantes.

Adicionalmente se normalizaron:

* Categorías generadas por IA.
* Prioridades generadas por IA.
* Equipos generados por IA.

Con el fin de mantener consistencia en métricas y visualizaciones.

---

## Limitaciones Conocidas

* El endpoint `/ask` utiliza un enfoque RAG simplificado basado en estadísticas y una base de conocimiento local.
* No se implementó una base vectorial.
* SQLite no está pensado para cargas de producción.
* La cuota gratuita de Gemini puede limitar la cantidad de tickets analizados durante una ejecución.
* Durante el desarrollo solo fue posible analizar una parte del dataset debido a las restricciones de cuota.
* Los tickets pendientes de análisis se muestran como `Pending Analysis`.
* La arquitectura soporta el procesamiento completo del dataset cuando se dispone de una API Key con cuota suficiente.

### Nota sobre Gemini

El proyecto requiere una API Key válida de Google Gemini para ejecutar los endpoints que utilizan Inteligencia Artificial (`/analyze` y `/ask`).

Durante el desarrollo se utilizó la cuota gratuita disponible, por lo que la cantidad de tickets analizados puede variar dependiendo de los límites de la cuenta utilizada.

---

## Mejoras Futuras

* Implementar RAG completo con embeddings y búsqueda semántica.
* Incorporar una base vectorial.
* Procesamiento asíncrono de tickets.
* Autenticación y autorización.
* Persistencia en PostgreSQL.
* Despliegue en la nube.
* Monitoreo y observabilidad.

---

## Conclusión

La solución fue diseñada priorizando simplicidad, claridad y mantenibilidad. Se implementó un flujo completo de análisis de tickets mediante Inteligencia Artificial, almacenamiento persistente, visualización de métricas y consultas sobre políticas de soporte, manteniendo una arquitectura modular y fácil de extender.

Debido a las restricciones de cuota del plan gratuito de Gemini, solo una parte del dataset pudo analizarse durante el desarrollo. Sin embargo, la arquitectura permite procesar la totalidad de los tickets cuando se dispone de una cuota suficiente.
