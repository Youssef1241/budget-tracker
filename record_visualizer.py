import streamlit as st
from collections import defaultdict
import plotly.express as px
from record import Record
from record_repository import RecordRepository
import pandas as pd

def create_all_visualizations():
    repo = RecordRepository()
    all_records = repo.get_all()
    create_pie_chart(all_records)
    create_bar_graph(all_records)
    create_montly_bar_graph(all_records)

def create_pie_chart(all_records: list[Record]):
    grouped_expenses = defaultdict(float)
    for exp in all_records:
        grouped_expenses[exp.expense_type] += exp.value
    fig = px.pie(
        names = list(grouped_expenses.keys()),
        values = list(grouped_expenses.values()),
        title="Expenses by Category",
        hole=0.4
    )
    st.plotly_chart(fig, use_container_width=True)

def create_bar_graph(all_records: list[Record]):
    df = pd.DataFrame([record.model_dump() for record in all_records])
    st.bar_chart(df, x="expense_type", y="value")

def create_montly_bar_graph(all_records: list[Record]):
    df = pd.DataFrame([record.model_dump() for record in all_records])
    grouped_df = df.groupby(df['date_time'].dt.date)['value'].sum().to_dict()
    st.bar_chart(grouped_df, x="date_time", y="value")
