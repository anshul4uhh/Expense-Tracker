import streamlit as st

from add_update_ui import add_update_tab
from analytics_ui import analytics_tab
from analytics_ui import analytics_tab_month

st.title("Expense Management System")
tab1,tab2,tab3 = st.tabs(["Add/Update","Analytics_By_Category","Analytics_By_Month"])

with tab1:
    add_update_tab()

with tab2:
    analytics_tab()
with tab3:
    analytics_tab_month()


