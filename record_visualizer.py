import streamlit as st
from collections import defaultdict
import plotly.express as px
from record import Record
from record_repository import RecordRepository
import pandas as pd

def create_all_visualizations(repo: RecordRepository):
    all_records = repo.get_all()
    df = pd.DataFrame([record.model_dump() for record in all_records])
    create_pie_chart(df)
    create_bar_graph(df)
    create_montly_bar_graph(df)

def create_pie_chart(df: pd.DataFrame):
    fig = px.pie(names = "expense_type",values = "value",data_frame = df,title="Expenses by Category",hole=0.4)
    st.plotly_chart(fig, use_container_width=True)

def create_bar_graph(df: pd.DataFrame):
    st.title("Expenses Bar Chart")
    st.bar_chart(df, x="expense_type", y="value", x_label="Expense Type", y_label="Value")

def create_montly_bar_graph(df: pd.DataFrame):
    grouped_df = df.groupby(df['date_time'].dt.date)['value'].sum().reset_index()
    grouped_df['date_time'] = grouped_df['date_time'].astype(str)
    st.title("Expenses by Day")
    st.bar_chart(grouped_df, x="date_time", y="value", x_label="Date", y_label="Value")
