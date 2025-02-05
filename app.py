import streamlit as st
import sqlite3
import pandas as pd
import streamlit.components.v1 as components

# Function to initialize the database
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

st.markdown("""<style>
    .stApp { background-color: #ffebf0; }
    .title { text-align: center; font-size: 40px; color: #e60073; font-weight: bold; }
    .winner-box { background-color: #ffccdd; padding: 15px; border-radius: 10px; text-align: center; }
    </style>""", unsafe_allow_html=True)

st.markdown("<div class='title'>💖 Valentine's Spin & Win 💖</div>", unsafe_allow_html=True)

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

# JavaScript for Spin Wheel
html_code = """
<script>
    let prize = "";
    function capturePrize(value) {
        prize = value;
        fetch('/update_prize', { method: 'POST', body: JSON.stringify({ prize: prize }) });
    }
</script>
<canvas id="wheel" width="300" height="300"></canvas>
<button id="spin">🎰 Spin the Wheel</button>
<p id="result"></p>
<script>
    const sectors = [
        { color: "#FF0000", text: "#FFFFFF", label: "Get 20% Off" },
        { color: "#FF7F00", text: "#FFFFFF", label: "Mystery Box" },
        { color: "#00FF00", text: "#FFFFFF", label: "Buy 1 Get 1" },
        { color: "#0000FF", text: "#FFFFFF", label: "Thank You" },
        { color: "#8B00FF", text: "#FFFFFF", label: "Lipstick" },
        { color: "#4B0082", text: "#FFFFFF", label: "Voucher" }
    ];
    let angVel = 0;
    let ang = 0;
    const friction = 0.991;
    const canvas = document.getElementById("wheel");
    const ctx = canvas.getContext("2d");
    const rad = canvas.width / 2;
    const arc = (2 * Math.PI) / sectors.length;
    
    function drawWheel() {
        sectors.forEach((sector, i) => {
            const angle = i * arc;
            ctx.beginPath();
            ctx.fillStyle = sector.color;
            ctx.moveTo(rad, rad);
            ctx.arc(rad, rad, rad, angle, angle + arc);
            ctx.lineTo(rad, rad);
            ctx.fill();
            ctx.translate(rad, rad);
            ctx.rotate(angle + arc / 2);
            ctx.fillStyle = sector.text;
            ctx.fillText(sector.label, rad - 20, 8);
            ctx.restore();
        });
    }
    
    function spin() {
        angVel = Math.random() * (0.45 - 0.25) + 0.25;
        requestAnimationFrame(rotateWheel);
    }
    
    function rotateWheel() {
        if (angVel > 0.002) {
            angVel *= friction;
            ang += angVel;
            ang %= 2 * Math.PI;
            canvas.style.transform = `rotate(${ang}rad)`;
            requestAnimationFrame(rotateWheel);
        } else {
            const winnerIndex = Math.floor(sectors.length - (ang / (2 * Math.PI)) * sectors.length) % sectors.length;
            document.getElementById("result").innerText = `🎉 You won: ${sectors[winnerIndex].label}`;
            capturePrize(sectors[winnerIndex].label);
        }
    }

    drawWheel();
    document.getElementById("spin").addEventListener("click", spin);
</script>
"""

# Embed Spin Wheel
components.html(html_code, height=600)

# Backend API to Capture Prize (Manually Set in Session State)
if "prize" not in st.session_state:
    st.session_state["prize"] = ""

with st.form("prize_form"):
    prize = st.text_input("Prize", value=st.session_state["prize"], disabled=True)
    claim_prize = st.form_submit_button("Claim Prize")

if claim_prize:
    name = st.session_state.get("player_name", "")
    phone = st.session_state.get("player_phone", "")
    prize = st.session_state.get("prize", "")

    if name and phone and prize:
        save_winner(name, phone, prize)
        st.success(f"🎉 {name}, your prize has been saved!")
        st.session_state["prize"] = ""
        st.experimental_rerun()

# Display updated winners table
winners_df = get_winners()
if not winners_df.empty:
    st.dataframe(winners_df)
else:
    st.info("No winners yet. Be the first to spin the wheel!")
