import streamlit as st
import random

# Define prizes
prizes = [
    "💄 Free Lipstick", 
    "🌹 10% Off Coupon", 
    "💖 Buy 1 Get 1 Free", 
    "🎁 Mystery Gift", 
    "💌 20% Off Next Purchase",
    "💕 Free Beauty Consultation"
]

# HTML, CSS, and JS for the spinning wheel
spin_wheel_html = f"""
<style>
    .wheel-container {{
        display: flex;
        justify-content: center;
        align-items: center;
        height: 450px;
        position: relative;
    }}
    canvas {{
        border-radius: 50%;
        box-shadow: 0px 10px 20px rgba(0, 0, 0, 0.2);
    }}
    .spin-button {{
        margin-top: 20px;
        padding: 14px 30px;
        background-color: #ff477e;
        color: white;
        font-size: 22px;
        font-weight: bold;
        border: none;
        border-radius: 12px;
        cursor: pointer;
        transition: 0.3s;
    }}
    .spin-button:hover {{
        background-color: #e63966;
    }}
    .indicator {{
        position: absolute;
        top: 0;
        left: 50%;
        transform: translateX(-50%);
        font-size: 30px;
        color: #ff0000;
    }}
</style>

<div class="wheel-container">
    <div class="indicator">🔻</div>
    <canvas id="wheelCanvas" width="400" height="400"></canvas>
</div>
<button class="spin-button" onclick="spinWheel()">💖 Spin Now!</button>

<script>
    let canvas = document.getElementById("wheelCanvas");
    let ctx = canvas.getContext("2d");
    let segments = {prizes};
    let colors = ["#FF477E", "#FF85A2", "#FFC1D2", "#FF6188", "#FF92B1", "#FFD6E0"];
    let arc = Math.PI / (segments.length / 2);
    let angle = 0;
    let spinAngleStart = 10;
    let spinTime = 0;
    let spinTimeTotal = 0;
    let prizeIndex = 0;

    function drawWheel() {{
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        for (let i = 0; i < segments.length; i++) {{
            let startAngle = angle + i * arc;
            let endAngle = startAngle + arc;
            ctx.fillStyle = colors[i];
            ctx.beginPath();
            ctx.moveTo(200, 200);
            ctx.arc(200, 200, 200, startAngle, endAngle, false);
            ctx.lineTo(200, 200);
            ctx.fill();
            ctx.save();
            ctx.fillStyle = "white";
            ctx.font = "bold 16px Arial";
            ctx.translate(200 + Math.cos(startAngle + arc / 2) * 130, 
                          200 + Math.sin(startAngle + arc / 2) * 130);
            ctx.rotate(startAngle + arc / 2 + Math.PI / 2);
            ctx.fillText(segments[i], -50, 10);
            ctx.restore();
        }}
    }}

    function rotateWheel() {{
        let spinAngle = spinAngleStart - (spinTime / spinTimeTotal) * spinAngleStart;
        angle += (spinAngle * Math.PI) / 180;
        drawWheel();
        spinTime += 30;
        if (spinTime < spinTimeTotal) {{
            requestAnimationFrame(rotateWheel);
        }} else {{
            setTimeout(() => {{
                let winningPrize = segments[prizeIndex];
                Streamlit.setComponentValue(winningPrize);
            }}, 500);
        }}
    }}

    function spinWheel() {{
        spinTime = 0;
        spinTimeTotal = Math.random() * 3000 + 2000;
        prizeIndex = Math.floor(Math.random() * segments.length);
        rotateWheel();
    }}

    drawWheel();
</script>
"""

# Streamlit app UI
st.title("💘 Valentine's Spin & Win! 🎡")
st.markdown("""
💄 Spin the wheel and win exciting beauty prizes! 🌹  
Click the **Spin Now!** button and see what you get! 🎁
""")

# Embed HTML for Spin Wheel
selected_prize = st.components.v1.html(spin_wheel_html, height=550)

# Confetti Effect
if selected_prize:
    st.balloons()
    st.success(f"🎉 Congratulations! You won **{selected_prize}**! 💖")
