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
    .spin-wheel-container { display: flex; flex-direction: column; align-items: center; justify-content: center; }
    .arrow { position: absolute; top: 35%; left: 50%; transform: translate(-50%, -100%); font-size: 50px; color: #ff007f; }
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
    spin_wheel_html = """
    <div style='text-align: center;'>
        <canvas id='spinWheel' width='300' height='300'></canvas>
        <br>
        <button id='spin_btn' style='padding: 10px 20px; font-size: 16px; background-color: #ff007f; color: white; border: none; cursor: pointer; border-radius: 5px;'>Spin</button>
        <p id='result' style='font-size: 18px; font-weight: bold;'></p>
    </div>
    
    <script>
        const prizes = ["Lipstick", "Perfume", "Makeup Kit", "Nail Polish", "Face Mask", "Gift Voucher"];
        const spinBtn = document.getElementById("spin_btn");
        const resultText = document.getElementById("result");
        const canvas = document.getElementById("spinWheel");
        const ctx = canvas.getContext("2d");

        function drawWheel() {
            const colors = ["#E74C3C", "#7D3C98", "#2E86C1", "#138D75", "#F1C40F", "#D35400"];
            const arc = Math.PI * 2 / prizes.length;
            for (let i = 0; i < prizes.length; i++) {
                ctx.beginPath();
                ctx.fillStyle = colors[i];
                ctx.moveTo(150, 150);
                ctx.arc(150, 150, 150, arc * i, arc * (i + 1));
                ctx.lineTo(150, 150);
                ctx.fill();
            }
        }
        
        drawWheel();

        spinBtn.addEventListener("click", () => {
            let angle = Math.floor(Math.random() * 360);
            canvas.style.transform = `rotate(${angle}deg)`;
            setTimeout(() => {
                let prizeIndex = Math.floor((angle / 60) % prizes.length);
                resultText.innerText = `🎉 You won: ${prizes[prizeIndex]}! 🎉`;
                window.parent.postMessage({"event": "winner", "prize": prizes[prizeIndex]}, "*");
            }, 2000);
        });
    </script>
    """
    st.components.v1.html(spin_wheel_html, height=400)

# Handle Winner Data
if "winner" in st.session_state:
    winner_info = st.session_state["winner"]
    save_winner(st.session_state["player_name"], st.session_state["player_phone"], winner_info["prize"])
    st.success(f"🎉 Congratulations {st.session_state['player_name']}, you won a {winner_info['prize']}! 🎉")

# Display Recent Winners
st.subheader("🎊 Recent Winners 🎊")
winners_df = get_winners()
if not winners_df.empty:
    st.table(winners_df[['name', 'phone', 'prize']])
else:
    st.info("No winners yet. Be the first to spin the wheel!")
