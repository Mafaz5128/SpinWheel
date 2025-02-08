import streamlit as st
import streamlit.components.v1 as components
import pandas as pd

# Set page title
st.set_page_config(page_title="Valentine Spin Wheel", layout="wide")

# Initialize session state
if "results" not in st.session_state:
    st.session_state["results"] = []

# Display header
st.markdown("<h1 style='text-align: center; color: #e60073;'>💖 Valentine's Spin & Win 💖</h1>", unsafe_allow_html=True)

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

# JavaScript + HTML for Spin Wheel
html_code = """
<!DOCTYPE html>
<html>
<head>
    <script>
        function sendPrizeToStreamlit(name, phone, prize) {
            window.parent.postMessage({ "name": name, "phone": phone, "prize": prize }, "*");
        }

        window.addEventListener("message", (event) => {
            if (event.data.prize) {
                var prizeInput = window.parent.document.querySelector("input[aria-label='Your Prize:']");
                if (prizeInput) {
                    prizeInput.value = event.data.prize;
                }
                document.getElementById("result").innerText = `🎉 Congratulations! You won: ${event.data.prize}`;
                window.parent.postMessage({
                    "name": event.data.name,
                    "phone": event.data.phone,
                    "prize": event.data.prize
                }, "*");
            }
        });

        function spinWheel() {
            const prizes = ["Get 20% Off", "Mystery Box", "Buy 1 Get 1", "Thank You", "Lipstick", "Voucher"];
            const selectedPrize = prizes[Math.floor(Math.random() * prizes.length)];
            document.getElementById("result").innerText = `🎉 You won: ${selectedPrize}`;
            sendPrizeToStreamlit('""" + st.session_state.get("player_name", "Unknown") + """', 
                                 '""" + st.session_state.get("player_phone", "Unknown") + """', 
                                 selectedPrize);
        }
    </script>
    <style>
        body { text-align: center; font-family: Arial, sans-serif; }
        .wheel-container { position: relative; display: inline-block; margin-top: 50px; }
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
    <button onclick="spinWheel()">🎰 Spin the Wheel</button>
    <p id="result"></p>

    <script>
        const sectors = [
            { color: "#FF0000", text: "#FFFFFF", label: "20% OFF" },
            { color: "#FF7F00", text: "#FFFFFF", label: "Free Delivery" },
            { color: "#00FF00", text: "#FFFFFF", label: "Win a Perfume!" },
            { color: "#0000FF", text: "#FFFFFF", label: "BOGO – Any Item!" },
            { color: "#8B00FF", text: "#FFFFFF", label: "Couple Watch!" },
            { color: "#4B0082", text: "#FFFFFF", label: "LKR 5000 Voucher" }
        ];

        const rand = (m, M) => Math.random() * (M - m) + m;
        const tot = sectors.length;
        const spinEl = document.querySelector("button");
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

        const getIndex = () => Math.floor(tot - (ang / TAU) * tot) % tot;

        function drawSector(sector, i) {
            const ang = arc * i;
            ctx.save();
            ctx.beginPath();
            ctx.fillStyle = sector.color;
            ctx.moveTo(rad, rad);
            ctx.arc(rad, rad, rad, ang, ang + arc);
            ctx.lineTo(rad, rad);
            ctx.fill();
            ctx.translate(rad, rad);
            ctx.rotate(ang + arc / 2);
            ctx.textAlign = "right";
            ctx.fillStyle = sector.text;
            ctx.font = "bold 18px Arial";
            ctx.fillText(sector.label, rad - 10, 10);
            ctx.restore();
        }

        function rotate() {
            canvas.style.transform = `rotate(${ang - PI / 2}rad)`;
        }

        function frame() {
            if (!angVel) {
                const finalSector = sectors[getIndex()];
                document.getElementById("result").innerText = `🎉 You won: ${finalSector.label}`;
                sendPrizeToStreamlit('""" + st.session_state.get("player_name", "Unknown") + """', 
                                     '""" + st.session_state.get("player_phone", "Unknown") + """', 
                                     finalSector.label);
                return;
            }
            angVel *= friction;
            if (angVel < 0.002) angVel = 0;
            ang += angVel;
            ang %= TAU;
            rotate();
            requestAnimationFrame(frame);
        }

        function init() {
            sectors.forEach(drawSector);
            rotate();
            spinEl.addEventListener("click", () => {
                if (!angVel) angVel = rand(0.25, 0.45);
                requestAnimationFrame(frame);
            });
        }

        init();
    </script>
</body>
</html>
"""

# Embed the spin wheel
components.html(html_code, height=600)

# Display Spin Results
st.markdown("## 🎉 Spin Results")
df = pd.DataFrame(st.session_state["results"], columns=["Name", "Phone", "Prize"])
st.dataframe(df)
