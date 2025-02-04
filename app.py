import streamlit as st
import pandas as pd
import random
import sqlite3

def init_db():
    conn = sqlite3.connect("winners.db")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS winners 
                      (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, phone TEXT, prize TEXT)''')
    conn.commit()
    conn.close()

def save_winner(name, phone, prize):
    conn = sqlite3.connect("winners.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO winners (name, phone, prize) VALUES (?, ?, ?)", (name, phone, prize))
    conn.commit()
    conn.close()

def get_winners():
    conn = sqlite3.connect("winners.db")
    df = pd.read_sql("SELECT * FROM winners", conn)
    conn.close()
    return df

def get_random_prize():
    prizes = ["Lipstick", "Perfume", "Makeup Kit", "Nail Polish", "Face Mask", "Gift Voucher"]
    return random.choice(prizes)

# Initialize DB
init_db()

# UI Setup
st.set_page_config(page_title="Valentine Spin Wheel", layout="wide")
st.markdown("""
    <style>
    .stApp { background-color: #ffebf0; }
    .title { text-align: center; font-size: 40px; color: #e60073; font-weight: bold; }
    .winner-box { background-color: #ffccdd; padding: 15px; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<div class='title'>💖 Valentine's Spin & Win 💖</div>", unsafe_allow_html=True)

# User Input Form
with st.form("spin_form"):
    name = st.text_input("Enter Your Name")
    phone = st.text_input("Enter Your Phone Number")
    submitted = st.form_submit_button("Spin the Wheel")
    
    if submitted and name and phone:
        prize = get_random_prize()
        save_winner(name, phone, prize)
        st.success(f"🎉 Congratulations {name}, You won {prize}! 🎁")
        
        # Show Spin Wheel
        st.components.v1.html(open("spin_wheel.html").read(), height=500)

# Display Winners List
st.subheader("🎊 Recent Winners 🎊")
winners = get_winners()
st.table(winners[['name', 'phone', 'prize']])
