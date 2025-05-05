import streamlit as st
from datetime import datetime
import requests
import pandas as pd


API_URL = "http://web-production-6a46.up.railway.app"


def analytics_tab():
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("Start Date", datetime(2024, 8, 1))
    with col2:
        end_date = st.date_input("End Date", datetime(2024, 8, 5))

    if st.button("Get Analytics"):
        payload = {
            "start_date": start_date.strftime("%Y-%m-%d"),
            "end_date": end_date.strftime("%Y-%m-%d")
        }
        response = requests.post(f"{API_URL}/analytics", json=payload)
        if response.status_code != 200:
            st.error("Failed to retrieve analytics data.")
            return

        response = response.json()
        if not response:
            st.warning("No expenses found for the selected range.")
            return

        df = pd.DataFrame({
            "Category": list(response.keys()),
            "Total": [response[cat]["total"] for cat in response],
            "Percentage": [response[cat]["percentage"] for cat in response]
        })
        df_sorted = df.sort_values(by="Percentage", ascending=False)
        st.title("Expense Breakdown By Category")
        st.bar_chart(data=df_sorted.set_index("Category")["Percentage"], use_container_width=True)

        df_sorted["Total"] = df_sorted["Total"].map("{:.2f}".format)
        df_sorted["Percentage"] = df_sorted["Percentage"].map("{:.2f}".format)
        df_sorted.reset_index(drop=True, inplace=True)

        st.subheader("Detailed Table")
        st.table(df_sorted)



def analytics_tab_month():
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("Start Date", datetime(2024, 1, 1))
    with col2:
        end_date = st.date_input("End Date", datetime(2024, 12, 31))

    if st.button("Get Analytics By Month"):
        payload = {
            "start_date": start_date.strftime("%Y-%m-%d"),
            "end_date": end_date.strftime("%Y-%m-%d")
        }
        response = requests.post(f"{API_URL}/analyticsmonth", json=payload)
        if response.status_code != 200:
            st.error("Failed to retrieve monthly analytics.")
            return

        data = response.json()
        if not data:
            st.warning("No expenses found for the selected period.")
            return

        df = pd.DataFrame(data)

        month_order = [
            'January', 'February', 'March', 'April', 'May', 'June',
            'July', 'August', 'September', 'October', 'November', 'December'
        ]
        df['month'] = pd.Categorical(df['month'], categories=month_order, ordered=True)
        df = df.sort_values('month')

        st.title("Expense Breakdown By Months")
        st.bar_chart(df.set_index('month'), use_container_width=True)

        st.subheader("Detailed Table")
        st.table(df)


