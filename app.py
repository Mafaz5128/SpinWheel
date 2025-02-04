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
        spin_wheel_html = """
        <html>
        <head>
        <style>
            .wheel-container { position: relative; width: 300px; height: 300px; }
            .wheel { width: 100%; height: 100%; border-radius: 50%; background: conic-gradient(
                red 0deg 60deg, yellow 60deg 120deg, green 120deg 180deg,
                blue 180deg 240deg, orange 240deg 300deg, purple 300deg 360deg);
                transition: transform 3s ease-out; }
            .arrow { position: absolute; top: 50%; left: 50%; width: 20px; height: 20px;
                background: red; clip-path: polygon(100% 0, 0 50%, 100% 100%);
                transform: translate(-50%, -50%) rotate(-90deg); }
        </style>
        <script>
            function spinWheel() {
                let wheel = document.getElementById('wheel');
                let randomDegree = 1800 + Math.floor(Math.random() * 360);
                wheel.style.transform = 'rotate(' + randomDegree + 'deg)';
            }
        </script>
        </head>
        <body>
        <div class='wheel-container'>
            <div class='arrow'></div>
            <div class='wheel' id='wheel'></div>
        </div>
        <button onclick='spinWheel()'>Spin</button>
        </body>
        </html>
        """
        st.components.v1.html(spin_wheel_html, height=400)

# Display Winners List
st.subheader("🎊 Recent Winners 🎊")
winners = get_winners()
st.table(winners[['name', 'phone', 'prize']])
