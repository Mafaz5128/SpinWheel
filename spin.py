import streamlit as st
import streamlit.components.v1 as components
import sqlite3

# Set Streamlit Page Config
st.set_page_config(page_title="Spin & Win | Valentine's Special", page_icon="🎡", layout='wide')

# Database Setup
conn = sqlite3.connect("winners.db", check_same_thread=False)
c = conn.cursor()
c.execute("""
    CREATE TABLE IF NOT EXISTS winners (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        phone TEXT,
        prize TEXT
    )
""")
conn.commit()

# Valentine’s Theme Styling
st.markdown(
    """
    <style>
        .stApp { background: url('https://img.freepik.com/free-vector/valentines-day-heart-balloons-background_52683-106376.jpg?w=1800'); 
                 background-size: cover; }
        .title { font-size: 36px; color: #ff4081; text-align: center; font-weight: bold; }
    </style>
    """,
    unsafe_allow_html=True
)

# Title
st.markdown("<h1 class='title'>🎡 Spin & Win - Valentine's Day Special!</h1>", unsafe_allow_html=True)
st.write("Enter your name and phone number, then spin the wheel to win amazing prizes!")

# Customer Input Form
name = st.text_input("Enter Your Name")
phone = st.text_input("Enter Your Phone Number")

# HTML + JavaScript for Spin Wheel
html_code = """
<!DOCTYPE html>
<html>
<head>
    <style>
        body { text-align: center; font-family: Arial, sans-serif; background: #ffe6f2; }
        .wheel-container { position: relative; display: inline-block; margin-top: 20px;}
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
            padding: 12px 20px;
            font-size: 18px;
            background: #ff4081;
            color: white;
            border: none;
            cursor: pointer;
            margin-top: 15px;
            border-radius: 8px;
        }
        button:hover { background: #ff0055; }
        #result {
            font-size: 20px;
            font-weight: bold;
            margin-top: 10px;
            color: #ff4081;
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
            { color: "#FF0000", text: "#FFFFFF", label: "20% Off" },
            { color: "#FF7F00", text: "#FFFFFF", label: "Mystery Box" },
            { color: "#00FF00", text: "#FFFFFF", label: "Buy 1 Get 1" },
            { color: "#0000FF", text: "#FFFFFF", label: "Thank You" },
            { color: "#8B00FF", text: "#FFFFFF", label: "Lipstick" },
            { color: "#4B0082", text: "#FFFFFF", label: "Voucher" }
        ];

        let angVel = 0;
        let ang = 0;
        let spinButtonClicked = false;

        const getIndex = () => Math.floor(sectors.length - (ang / (2 * Math.PI)) * sectors.length) % sectors.length;

        function rotate() {
            const sector = sectors[getIndex()];
            document.querySelector("#wheel").style.transform = `rotate(${ang - Math.PI / 2}rad)`;
        }

        function frame() {
            if (!angVel && spinButtonClicked) {
                const finalSector = sectors[getIndex()];
                document.getElementById("result").innerText = `🎉 You won: ${finalSector.label}`;
                window.parent.postMessage(finalSector.label, "*");  // Send prize to Streamlit
                spinButtonClicked = false;
                return;
            }
            angVel *= 0.991;
            ang += angVel;
            rotate();
        }

        function engine() { frame(); requestAnimationFrame(engine); }

        function init() {
            rotate();
            engine();
            document.querySelector("#spin").addEventListener("click", () => { if (!angVel) angVel = Math.random() * (0.45 - 0.25) + 0.25; spinButtonClicked = true; });
        }

        init();
    </script>
</body>
</html>
"""

# Store Prize after spin
if name and phone:
    prize = st.empty()
    spin = components.html(html_code, height=600)
    
    # Receive prize from JS
    message = st.experimental_get_query_params().get("prize")
    
    if message:
        prize.text(f"🎉 Congratulations {name}, You Won: {message[0]}")
        
        # Save winner to database
        c.execute("INSERT INTO winners (name, phone, prize) VALUES (?, ?, ?)", (name, phone, message[0]))
        conn.commit()

# Show recent winners
st.subheader("Recent Winners")
c.execute("SELECT name, phone, prize FROM winners ORDER BY id DESC LIMIT 5")
winners = c.fetchall()

# Display winners in table format
st.table(winners)