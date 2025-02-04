import streamlit as st
import pandas as pd
import random
import sqlite3

# Initialize SQLite database
def init_db():
    try:
        conn = sqlite3.connect("winners.db")
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS winners 
                          (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                           name TEXT NOT NULL, 
                           phone TEXT NOT NULL, 
                           prize TEXT NOT NULL)''')
        conn.commit()
    except sqlite3.Error as e:
        st.error(f"Database error: {e}")
    finally:
        if conn:
            conn.close()

# Save winner details to the database
def save_winner(name, phone, prize):
    try:
        conn = sqlite3.connect("winners.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO winners (name, phone, prize) VALUES (?, ?, ?)", (name, phone, prize))
        conn.commit()
    except sqlite3.Error as e:
        st.error(f"Failed to save winner: {e}")
    finally:
        if conn:
            conn.close()

# Retrieve all winners from the database
def get_winners():
    try:
        conn = sqlite3.connect("winners.db")
        df = pd.read_sql("SELECT * FROM winners ORDER BY id DESC", conn)  # Order by latest winners first
        return df
    except sqlite3.Error as e:
        st.error(f"Failed to retrieve winners: {e}")
        return pd.DataFrame()  # Return an empty DataFrame in case of error
    finally:
        if conn:
            conn.close()

# Get a random prize from the list
def get_random_prize():
    prizes = ["Lipstick", "Perfume", "Makeup Kit", "Nail Polish", "Face Mask", "Gift Voucher"]
    return random.choice(prizes)

# Initialize the database
init_db()

# Streamlit UI Setup
st.set_page_config(page_title="Valentine Spin Wheel", layout="wide")

# Load custom CSS from styles.css
with open("styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Load custom HTML from index.html
with open("index.html") as f:
    st.components.v1.html(f.read(), height=600)

# User Input Form
with st.form("spin_form"):
    name = st.text_input("Enter Your Name", placeholder="John Doe")
    phone = st.text_input("Enter Your Phone Number", placeholder="123-456-7890")
    submitted = st.form_submit_button("Spin the Wheel")
    
    if submitted:
        if not name or not phone:
            st.error("Please enter both your name and phone number.")
        else:
            prize = get_random_prize()
            save_winner(name, phone, prize)
            st.success(f"🎉 Congratulations {name}, You won {prize}! 🎁")

# Display Recent Winners
st.subheader("🎊 Recent Winners 🎊")
winners = get_winners()
if not winners.empty:
    st.table(winners[['name', 'phone', 'prize']])
else:
    st.info("No winners yet. Be the first to spin the wheel!")
