# dashboard/app.py

import streamlit as st
import requests
import pandas as pd
import plotly.express as px

# ---------------------------------
# CONFIGURACIÓN DE LA PÁGINA
# ---------------------------------

st.set_page_config(
    page_title="AI Support Ticket Analyzer",
    layout="wide"
)

# ---------------------------------
# TÍTULO
# ---------------------------------

st.title("🎫 AI Support Ticket Analyzer")

# ---------------------------------
# URL DEL BACKEND FASTAPI
# ---------------------------------

API_URL = "http://127.0.0.1:8000"

# ---------------------------------
# OBTENER DATOS DESDE FASTAPI
# ---------------------------------

analytics = requests.get(
    f"{API_URL}/analytics"
).json()

tickets = requests.get(
    f"{API_URL}/analyzed_tickets"
).json()

# Convertimos la respuesta JSON en DataFrame
df_tickets = pd.DataFrame(tickets)

# ---------------------------------
# KPIs
# ---------------------------------

pending_analysis = analytics[
    "categories"
].get(
    "Pending Analysis",
    0
)

analyzed_tickets = (
    analytics["total_tickets"]
    - pending_analysis
)

real_categories = analytics[
    "categories"
].copy()

real_categories.pop(
    "Pending Analysis",
    None
)

top_category = "N/A"

if len(real_categories) > 0:

    top_category = max(
        real_categories,
        key=real_categories.get
    )

st.subheader("📊 KPIs")

col1, col2, col3, col4 = st.columns(4)

with col1:

    st.metric(
        "Total Tickets",
        analytics["total_tickets"]
    )

with col2:

    st.metric(
        "Analyzed",
        analyzed_tickets
    )

with col3:

    st.metric(
        "Pending",
        pending_analysis
    )

with col4:

    st.metric(
        "Top Category",
        top_category
    )
# ---------------------------------
# FILTROS
# ---------------------------------

st.subheader("🔎 Filtros")

# Filtro de categoría

categories = ["All"] + sorted(
    df_tickets["category"].dropna().unique().tolist()
)

selected_category = st.selectbox(
    "Categoría",
    categories
)

if selected_category != "All":

    df_tickets = df_tickets[
        df_tickets["category"] == selected_category
    ]

# Filtro de prioridad

priorities = ["All"] + sorted(
    df_tickets["priority"].dropna().unique().tolist()
)

selected_priority = st.selectbox(
    "Prioridad",
    priorities
)

if selected_priority != "All":

    df_tickets = df_tickets[
        df_tickets["priority"] == selected_priority
    ]

#Filtro por equipo
teams = ["All"] + sorted(
    df_tickets["team"].dropna().unique().tolist()
)

selected_team = st.selectbox(
    "Team",
    teams
)

if selected_team != "All":

    df_tickets = df_tickets[
        df_tickets["team"] == selected_team
    ]

#Filtro por sentimiento
sentiments = ["All"] + sorted(
    df_tickets["sentiment"].dropna().unique().tolist()
)

selected_sentiment = st.selectbox(
    "Sentiment",
    sentiments
)

if selected_sentiment != "All":

    df_tickets = df_tickets[
        df_tickets["sentiment"] == selected_sentiment
    ]

# ---------------------------------
# GRÁFICO DE CATEGORÍAS
# ---------------------------------

st.subheader("📂 Tickets por Categoría")

category_df = pd.DataFrame(
    list(analytics["categories"].items()),
    columns=["Category", "Count"]
)

category_df = category_df[
    category_df["Category"] != "Pending Analysis"
]

fig_category = px.bar(
    category_df,
    x="Category",
    y="Count",
    title="Distribución por Categoría"
)

st.plotly_chart(
    fig_category,
    width="stretch"
)

# ---------------------------------
# GRÁFICO DE PRIORIDADES
# ---------------------------------

st.subheader("🚨 Prioridades")

priority_df = pd.DataFrame(
    list(analytics["priorities"].items()),
    columns=["Priority", "Count"]
)

priority_df = priority_df[
    priority_df["Priority"] != "Pending Analysis"
]

fig_priority = px.pie(
    priority_df,
    names="Priority",
    values="Count",
    title="Distribución de Prioridades"
)

st.plotly_chart(
    fig_priority,
    width="stretch"
)

# ---------------------------------
# TABLA
# ---------------------------------

st.subheader("📋 Tickets Analizados")

st.write(
    f"Mostrando {len(df_tickets)} tickets"
)

columns_to_show = [
    "ticket_id",
    "category",
    "priority",
    "team",
    "sentiment",
    "summary"
]

df_display = df_tickets[
    columns_to_show
]

st.dataframe(
    df_display,
    width="stretch"
)

# ---------------------------------
# ASK THE AI
# ---------------------------------

st.subheader("🤖 Ask About Your Tickets")

question = st.text_input(
    "Ask a question"
)

if st.button("Ask"):

    response = requests.post(
        f"{API_URL}/ask",
        json={
            "question": question
        }
    )

    answer = response.json()

    st.success(
        answer["answer"]
    )