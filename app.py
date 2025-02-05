import streamlit as st
import sqlite3
import pandas as pd
import random
import time
import streamlit.components.v1 as components

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

# HTML + JavaScript for Spin Wheel (Updated Version)
html_code = """
<!DOCTYPE html>
<html>
<head>
    <style>
        body { text-align: center; font-family: Arial, sans-serif; }
        .wheel-container { position: relative; display: inline-block; margin-top: 50px;}
        .pointer {
            position: absolute;
            top: -15px; left: 50%;
            transform: translateX(-50%);
            width: 0; height: 0;
            border-left: 12px solid transparent;
            border-right: 12px solid transparent;
            border-bottom: 25px solid black;
            z-index: 10;
        }
        canvas {
            border-radius: 50%;
            border: 5px solid #ff4081;
        }
        button {
            padding: 10px 18px;
            font-size: 16px;
            background: #ff4081;
            color: white;
            border: none;
            cursor: pointer;
            margin-top: 15px;
            border-radius: 5px;
        }
        button:hover { background: #ff0055; }
        #result {
            font-size: 18px;
            font-weight: bold;
            margin-top: 10px;
        }
    </style>
</head>
<body>
    <div class="wheel-container">
        <div class="pointer"></div>
        <canvas id="wheel" width="300" height="300"></canvas>
    </div>
    <br>
    <button id="spin">🎰 Spin the Wheel</button>
    <p id="result"></p>

    <script>
        const sectors = [
            { color: "#FF0000", text: "#FFFFFF", label: "Get 20% Off" },
            { color: "#FF7F00", text: "#FFFFFF", label: "Mystry Box" },
            { color: "#00FF00", text: "#FFFFFF", label: "Buy 1 Get 1" },
            { color: "#0000FF", text: "#FFFFFF", label: "Thank You" },
            { color: "#8B00FF", text: "#FFFFFF", label: "Lip Stick" },
            { color: "#4B0082", text: "#FFFFFF", label: "Voucher" }
        ];

        const events = {
            listeners: {},
            addListener: function (eventName, fn) {
                this.listeners[eventName] = this.listeners[eventName] || [];
                this.listeners[eventName].push(fn);
            },
            fire: function (eventName, ...args) {
                if (this.listeners[eventName]) {
                    for (let fn of this.listeners[eventName]) {
                        fn(...args);
                    }
                }
            }
        };

        const rand = (m, M) => Math.random() * (M - m) + m;
        const tot = sectors.length;
        const spinEl = document.querySelector("#spin");
        const canvas = document.querySelector("#wheel");
        const ctx = canvas.getContext("2d");
        const dia = canvas.width;
        const rad = dia / 2;
        const PI = Math.PI;
        const TAU = 2 * PI;
        const arc = TAU / sectors.length;

        const friction = 0.991;
        let angVel = 0;
        let ang = 0;
        let spinButtonClicked = false;

        const getIndex = () => Math.floor(tot - (ang / TAU) * tot) % tot;

        function drawSector(sector, i) {
            const ang = arc * i;
            ctx.save();

            // COLOR
            ctx.beginPath();
            ctx.fillStyle = sector.color;
            ctx.moveTo(rad, rad);
            ctx.arc(rad, rad, rad, ang, ang + arc);
            ctx.lineTo(rad, rad);
            ctx.fill();

            // TEXT
            ctx.translate(rad, rad);
            ctx.rotate(ang + arc / 2);
            ctx.textAlign = "right";
            ctx.fillStyle = sector.text;
            ctx.font = "bold 18px 'Lato', sans-serif";
            ctx.fillText(sector.label, rad - 8, 8);

            ctx.restore();
        }

        function rotate() {
            const sector = sectors[getIndex()];
            canvas.style.transform = `rotate(${ang - PI / 2}rad)`;

            spinEl.textContent = !angVel ? "SPIN" : sector.label;
            spinEl.style.background = sector.color;
            spinEl.style.color = sector.text;
        }

        function frame() {
            if (!angVel && spinButtonClicked) {
                const finalSector = sectors[getIndex()];
                events.fire("spinEnd", finalSector);
                spinButtonClicked = false;
                return;
            }

            angVel *= friction;
            if (angVel < 0.002) angVel = 0;
            ang += angVel;
            ang %= TAU;
            rotate();
        }

        function engine() {
            frame();
            requestAnimationFrame(engine);
        }

        function init() {
            sectors.forEach(drawSector);
            rotate();
            engine();
            spinEl.addEventListener("click", () => {
                if (!angVel) angVel = rand(0.25, 0.45);
                spinButtonClicked = true;
            });
        }

        init();

        events.addListener("spinEnd", (sector) => {
            document.getElementById("result").innerText = `🎉 You won: ${sector.label}`;
            Streamlit.setComponentValue(sector.label);
        });
    </script>
</body>
</html>
"""

# Embed the updated HTML code for Spin Wheel
result = components.html(html_code, height=1024)

# Save the result to the database and update the recent winners table
if result and "player_name" in st.session_state and "player_phone" in st.session_state:
    prize = result
    name = st.session_state["player_name"]
    phone = st.session_state["player_phone"]
    save_winner(name, phone, prize)
    st.session_state["can_spin"] = False
    st.success(f"🎉 Congratulations {name}! You won: {prize}")

# Display Recent Winners
st.subheader("🎊 Recent Winners 🎊")
winners_df = get_winners()
if not winners_df.empty:
    st.table(winners_df[['name', 'phone', 'prize']])
else:
    st.info("No winners yet. Be the first to spin the wheel!"), the error is File "/mount/src/spinwheel/app.py", line 239, in <module>
    save_winner(name, phone, prize)
