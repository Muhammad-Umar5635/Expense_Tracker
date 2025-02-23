import streamlit as st
import pandas as pd
import os

# File to store user data
USER_DATA_FILE = "user_data.csv"

# Ensure the file exists
if not os.path.exists(USER_DATA_FILE):
    df = pd.DataFrame(columns=["User Password", "Date", "Category", "Amount", "Description"])
    df.to_csv(USER_DATA_FILE, index=False)

# Load expense data
def load_data():
    return pd.read_csv(USER_DATA_FILE)

# Save new expense (for specific user)
def save_expense(user_password, date, category, amount, description):
    df = load_data()
    
    # Add new entry
    new_data = pd.DataFrame([[user_password, date, category, amount, description]], 
                            columns=["User Password", "Date", "Category", "Amount", "Description"])
    
    df = pd.concat([df, new_data], ignore_index=True)
    
    # Sort by Date in Descending Order
    df["Date"] = pd.to_datetime(df["Date"])
    df = df.sort_values(by="Date", ascending=False)

    df.to_csv(USER_DATA_FILE, index=False)

# Delete an entry
def delete_entry(user_password, entry_index):
    df = load_data()
    
    # Filter only user-specific data
    user_df = df[df["User Password"] == user_password]
    
    # Get row index to delete
    if entry_index < len(user_df):
        user_df = user_df.drop(user_df.index[entry_index])
        
        # Update main dataframe
        df = df[df["User Password"] != user_password]  # Remove old user data
        df = pd.concat([df, user_df], ignore_index=True)
        df.to_csv(USER_DATA_FILE, index=False)
        return True
    return False

# Streamlit UI
st.set_page_config(page_title="Expense Tracker", page_icon="💰", layout="wide")

st.sidebar.title("🔐 Login")
user_password = st.sidebar.text_input("Enter Your Unique Password:", type="password")

if user_password:
    st.sidebar.success("✅ Access Granted!")
    
    # Tabs for better navigation
    tab1, tab2, tab3 = st.tabs(["➕ Add Expense", "📜 View History", "📥 Download & Delete"])

    with tab1:
        st.header("➕ Add New Expense")
        col1, col2 = st.columns(2)
        with col1:
            date = st.date_input("📅 Date")
        with col2:
            category = st.selectbox("📂 Category", ["Food", "Transport", "Shopping", "Bills", "Other"])
        
        amount = st.number_input("💰 Amount", min_value=0.01, format="%.2f")
        description = st.text_area("📝 Description")

        if st.button("✔ Add Expense", use_container_width=True):
            save_expense(user_password, date, category, amount, description)
            st.success("✅ Expense added successfully!")

    with tab2:
        st.header("📜 Your Expense History (Newest First)")
        df = load_data()
        
        # Filter expenses for the current user
        user_df = df[df["User Password"] == user_password].drop(columns=["User Password"])
        st.dataframe(user_df, height=400, use_container_width=True)

    with tab3:
        st.header("📥 Download & Delete Entries")

        # **Download CSV Report**
        if not user_df.empty:
            st.download_button("📥 Download CSV", user_df.to_csv(index=False), "your_expenses.csv", "text/csv")

        # **Delete an Entry**
        if not user_df.empty:
            entry_index = st.number_input("❌ Enter Entry Index to Delete", min_value=0, max_value=len(user_df)-1, step=1)
            if st.button("🗑 Delete Entry", use_container_width=True):
                if delete_entry(user_password, entry_index):
                    st.success("✅ Entry Deleted Successfully!")
                else:
                    st.error("❌ Invalid Entry Number!")

else:
    st.sidebar.error("❌ Please Enter Your Password to Access Your Data.")

