import streamlit as st
import sqlite3
import pandas as pd
import random
import time

# Initialize SQLite database
def init_db():
    conn = sqlite3.connect("winners.db")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS winners 
                      (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                       name TEXT NOT NULL, 
                       phone TEXT NOT NULL, 
                       prize TEXT NOT NULL)''')
    conn.commit()
    conn.close()

# Save winner details to the database
def save_winner(name, phone, prize):
    conn = sqlite3.connect("winners.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO winners (name, phone, prize) VALUES (?, ?, ?)", (name, phone, prize))
    conn.commit()
    conn.close()

# Retrieve all winners from the database
def get_winners():
    conn = sqlite3.connect("winners.db")
    df = pd.read_sql("SELECT * FROM winners ORDER BY id DESC", conn)
    conn.close()
    return df

# Initialize the database
init_db()

# Streamlit UI Setup
st.set_page_config(page_title="Valentine Spin Wheel", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #ffebf0; }
    .title { text-align: center; font-size: 40px; color: #e60073; font-weight: bold; }
    .winner-box { background-color: #ffccdd; padding: 15px; border-radius: 10px; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<div class='title'>💖 Valentine's Spin & Win 💖</div>", unsafe_allow_html=True)

# Prizes List
prizes = ["Lipstick", "Perfume", "Makeup Kit", "Nail Polish", "Face Mask", "Gift Voucher"]

# User Input Form
with st.form("spin_form"):
    name = st.text_input("Enter Your Name", placeholder="John Doe")
    phone = st.text_input("Enter Your Phone Number", placeholder="123-456-7890")
    submitted = st.form_submit_button("Proceed to Spin")
    
if submitted:
    if not name or not phone:
        st.error("Please enter both your name and phone number.")
    else:
        st.session_state["player_name"] = name
        st.session_state["player_phone"] = phone
        st.session_state["can_spin"] = True
        st.success(f"🎉 Welcome {name}! Click below to spin the wheel.")

# Display the Spin Wheel
if st.session_state.get("can_spin", False):
    if st.button("Spin the Wheel 🎡"):
        with st.spinner("Spinning the wheel..."):
            time.sleep(2)
            selected_prize = random.choice(prizes)
            st.session_state["winner_prize"] = selected_prize
            save_winner(st.session_state["player_name"], st.session_state["player_phone"], selected_prize)
            st.success(f"🎉 Congratulations {st.session_state['player_name']}, you won a {selected_prize}! 🎉")

# Display Recent Winners
st.subheader("🎊 Recent Winners 🎊")
winners_df = get_winners()
if not winners_df.empty:
    st.table(winners_df[['name', 'phone', 'prize']])
else:
    st.info("No winners yet. Be the first to spin the wheel!")
