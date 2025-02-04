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
        height: 350px;
    }}
    canvas {{
        border-radius: 50%;
        box-shadow: 0px 10px 20px rgba(0, 0, 0, 0.2);
    }}
    .spin-button {{
        margin-top: 20px;
        padding: 12px 25px;
        background-color: #ff477e;
        color: white;
        font-size: 20px;
        font-weight: bold;
        border: none;
        border-radius: 10px;
        cursor: pointer;
        transition: 0.3s;
    }}
    .spin-button:hover {{
        background-color: #e63966;
    }}
</style>

<div class="wheel-container">
    <canvas id="wheelCanvas" width="300" height="300"></canvas>
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
            ctx.moveTo(150, 150);
            ctx.arc(150, 150, 150, startAngle, endAngle, false);
            ctx.lineTo(150, 150);
            ctx.fill();
            ctx.save();
            ctx.fillStyle = "white";
            ctx.font = "bold 14px Arial";
            ctx.translate(150 + Math.cos(startAngle + arc / 2) * 100, 
                          150 + Math.sin(startAngle + arc / 2) * 100);
            ctx.rotate(startAngle + arc / 2 + Math.PI / 2);
            ctx.fillText(segments[i], -40, 10);
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
selected_prize = st.components.v1.html(spin_wheel_html, height=500)

# Confetti Effect
if selected_prize:
    st.balloons()
    st.success(f"🎉 Congratulations! You won **{selected_prize}**! 💖")
