import streamlit as st
import streamlit.components.v1 as components

# Streamlit UI Setup
st.set_page_config(page_title="Valentine Spin Wheel", layout="wide")

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

# JavaScript for Spin Wheel with prize retrieval
html_code = """
<!DOCTYPE html>
<html>
<head>
    <script>
        function sendPrizeToStreamlit(prize) {
            window.parent.postMessage({ "prize": prize }, "*");
        }
        
        window.addEventListener("message", (event) => {
            if (event.data.prize) {
                var prizeInput = window.parent.document.querySelector("input[aria-label='Your Prize:']");
                if (prizeInput) {
                    prizeInput.value = event.data.prize;
                }
            }
        });
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
            ctx.font = "bold 18px 'Lato', sans-serif";
            ctx.fillText(sector.label, rad - 8, 8);
            ctx.restore();
        }

        function rotate() {
            canvas.style.transform = `rotate(${ang - PI / 2}rad)`;
        }

        function frame() {
            if (!angVel) {
                const finalSector = sectors[getIndex()];
                document.getElementById("result").innerText = `🎉 You won: ${finalSector.label}`;
                sendPrizeToStreamlit(finalSector.label);
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

# Embed Spin Wheel
components.html(html_code, height=600)

# Capture Prize
prize_captured = st.text_input("Your Prize:", "", key="prize_input", disabled=True)

if prize_captured:
    st.session_state["prize"] = prize_captured

# Claim Prize Button
if st.button("Claim Prize"):
    if "player_name" in st.session_state and "player_phone" in st.session_state and "prize" in st.session_state:
        st.success(f"🎉 {st.session_state['player_name']}! You've won {st.session_state['prize']}!")
        st.session_state.pop("prize", None)
        st.experimental_rerun()
