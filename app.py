import streamlit as st
from record_repository import RecordRepository
from sqlmodel import create_engine, SQLModel
from record_visualizer import *

if "repo" not in st.session_state:
    engine = create_engine("sqlite:///records.db")
    if not engine.dialect.has_table(engine.connect(), "record"):
        SQLModel.metadata.create_all(engine)
    st.session_state.repo = RecordRepository(engine)

repo = st.session_state.repo

st.title("Budget Tracker")

overview_tab, records_tab, add_tab = st.tabs(["Overview", "Records", "Add"])

with overview_tab:
    create_all_visualizations(repo)

with records_tab:
    st.write("Select rows and click `Delete` to delete them")
    records = repo.get_all()
    df = pd.DataFrame([record.model_dump() for record in records])
    formatted_df = df.copy(deep=True)
    formatted_df.rename(columns={"name": "Name", "value": "Value", "expense_type": "Expense Type", "date_time": "DateTime"}, inplace=True)
    formatted_df["DateTime"] = formatted_df["DateTime"].dt.strftime("%d/%m/%Y")
    selection_event = st.dataframe(
        formatted_df,
        use_container_width=True,
        on_select="rerun",
        selection_mode="multi-row",
        column_config={
            "id": None 
        }
    )
    if st.button("Delete"):
        print(selection_event)
        selected_rows = selection_event.get("selection", {}).get("rows", [])
        if selected_rows:
            records_to_delete = formatted_df.loc[selected_rows].id.to_list()
            repo.delete_many(records_to_delete)
            st.rerun()
        else:
            st.info("No records to delete")

    
with add_tab:
    EXPENSE_TYPES = repo.get_expense_types()
    expense_type_selection = st.selectbox("Expense Type", EXPENSE_TYPES + ["Other"])

    if expense_type_selection == "Other":
        expense_type = st.text_input("Enter custom expense type")
    else:
        expense_type = expense_type_selection
    with st.form("add_record"):
        name = st.text_input("Name")
        value = st.number_input("Value", min_value=0.0, format="%.2f", step=1.0)
        submitted = st.form_submit_button("Add Record")

    if submitted:
        raw = {"name": name, "value": value, "expense_type": expense_type}
        record = repo.add(raw)
        st.session_state.add_success = f"Record {record.id} added successfully"
        st.rerun()
    if "add_success" in st.session_state:
        st.success(st.session_state.add_success)
        del st.session_state.add_success
