import streamlit as st
from datetime import datetime
import requests

import os


API_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

environment = "PRODUCTION" if "railway" in os.getenv("BACKEND_URL", "") else "LOCAL"
st.sidebar.markdown(f"**Environment:** {environment}")

def add_update_tab():
    selected_date = st.date_input("Enter Date", datetime(2024, 8, 1), label_visibility="collapsed")
    response = requests.get(f"{API_URL}/expenses/{selected_date}")
    if response.status_code == 200:
        existing_expenses = response.json()
    else:
        st.error("Failed to retrieve expenses")
        existing_expenses = []

    categories = ["Rent", "Food", "Shopping", "Entertainment", "Other"]

    with st.form(key="expense_form"):
        col1, col2, col3 = st.columns(3)
        with col1:
            st.text("Amount")
        with col2:
            st.text("Category")
        with col3:
            st.text("Notes")

        expenses = []
        for i in range(5):
            if i < len(existing_expenses):
                amount = existing_expenses[i]['amount']
                category = existing_expenses[i]['category'].capitalize()
                if category not in categories:
                    category = "Other"
                notes = existing_expenses[i]['notes']
            else:
                amount = 0.0
                category = "Shopping"
                notes = ""

            col1, col2, col3 = st.columns(3)
            with col1:
                amount_input = st.number_input(
                    label="Amount", min_value=0.0, step=1.0, value=amount,
                    key=f"amount_{i}", label_visibility="collapsed"
                )
            with col2:
                category_input = st.selectbox(
                    label="Category", options=categories,
                    index=categories.index(category),
                    key=f"categories_{i}", label_visibility="collapsed"
                )
            with col3:
                notes_input = st.text_input(
                    label="Notes", value=notes, key=f"notes_{i}",
                    label_visibility="collapsed"
                )

            expenses.append({
                'amount': amount_input,
                'category': category_input,
                'notes': notes_input
            })

        # ✅ Added submit button inside the form
        submit_button = st.form_submit_button("Submit")

        if submit_button:
            filtered_expenses = [expense for expense in expenses if expense['amount'] > 0]
            response = requests.post(f"{API_URL}/expenses/{selected_date}", json=filtered_expenses)
            if response.status_code == 200:
                st.success("Expense updated successfully")
            else:
                st.error("Failed to update expenses.")
