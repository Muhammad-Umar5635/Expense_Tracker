import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os

# File to store expenses
EXPENSE_FILE = "expenses.csv"

# Ensure the file exists
if not os.path.exists(EXPENSE_FILE):
    df = pd.DataFrame(columns=["Date", "Category", "Amount", "Description"])
    df.to_csv(EXPENSE_FILE, index=False)

# Load expense data
def load_data():
    return pd.read_csv(EXPENSE_FILE)

# Save new expense
def save_expense(date, category, amount, description):
    df = load_data()
    new_data = pd.DataFrame([[date, category, amount, description]], 
                            columns=["Date", "Category", "Amount", "Description"])
    df = pd.concat([df, new_data], ignore_index=True)
    df.to_csv(EXPENSE_FILE, index=False)

# Streamlit UI
st.title("💰 Personal Expense Tracker")

# Expense Input Form
st.subheader("Add New Expense")
date = st.date_input("Date")
category = st.selectbox("Category", ["Food", "Transport", "Shopping", "Bills", "Other"])
amount = st.number_input("Amount", min_value=0.01, format="%.2f")
description = st.text_area("Description")
if st.button("Add Expense"):
    save_expense(date, category, amount, description)
    st.success("Expense added successfully!")

# Show Expenses
st.subheader("📜 Expense History")
df = load_data()
st.dataframe(df)

# Expense Analysis
st.subheader("📊 Expense Analysis")
if not df.empty:
    df["Amount"] = pd.to_numeric(df["Amount"])
    
    # Category-wise breakdown
    category_summary = df.groupby("Category")["Amount"].sum()
    fig, ax = plt.subplots()
    category_summary.plot(kind="bar", ax=ax, color="skyblue")
    ax.set_ylabel("Total Amount")
    st.pyplot(fig)
    
    # Show total expenses
    total_spent = df["Amount"].sum()
    st.metric("Total Expenses", f"${total_spent:.2f}")
else:
    st.warning("No expenses recorded yet.")

# Download CSV
st.subheader("📥 Download Report")
st.download_button("Download CSV", df.to_csv(index=False), "expenses.csv", "text/csv")

