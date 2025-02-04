import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Spin & Win | Valentine's Special", page_icon="🎡")
st.title("🎡 Spin & Win - Valentine's Day Special!")

st.write("Click the **Spin the Wheel** button and try your luck!")

html_code = """
<!DOCTYPE html>
<html>
<head>
    <style>
        body { text-align: center; font-family: Arial, sans-serif; }
        .wheel-container { position: relative; display: inline-block; }
        .wheel { width: 300px; height: 300px; border-radius: 50%; border: 5px solid #ff4081; }
        .pointer { position: absolute; top: -20px; left: 50%; transform: translateX(-50%); width: 30px; height: 30px; background: red; clip-path: polygon(50% 0%, 0% 100%, 100% 100%); }
        button { padding: 12px 20px; font-size: 18px; background: #ff4081; color: white; border: none; cursor: pointer; margin-top: 15px; border-radius: 5px; }
        button:hover { background: #ff0055; }
        #result { font-size: 20px; font-weight: bold; margin-top: 10px; }
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
        const canvas = document.getElementById("wheel");
        const ctx = canvas.getContext("2d");
        const prizes = ["💄 Free Lipstick", "🛍️ 10% Off", "💖 Free Gift", "🎁 20% Off", "💌 Thank You"];
        let spinning = false;
        let angle = 0;
        const sliceAngle = (2 * Math.PI) / prizes.length;

        function drawWheel() {
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            let startAngle = 0;

            for (let i = 0; i < prizes.length; i++) {
                ctx.beginPath();
                ctx.moveTo(150, 150);
                ctx.arc(150, 150, 150, startAngle, startAngle + sliceAngle);
                ctx.fillStyle = i % 2 === 0 ? "#ffcccb" : "#ff4081";
                ctx.fill();
                ctx.closePath();

                ctx.fillStyle = "black";
                ctx.font = "bold 14px Arial";
                ctx.textAlign = "center";
                ctx.save();
                ctx.translate(150, 150);
                ctx.rotate(startAngle + sliceAngle / 2);
                ctx.fillText(prizes[i], 90, 10);
                ctx.restore();

                startAngle += sliceAngle;
            }
        }

        function spinWheel() {
            if (spinning) return;
            spinning = true;
            let rotation = Math.floor(Math.random() * 360) + 360 * 3;
            let spinTime = 3000;
            let start = null;

            function rotate(timestamp) {
                if (!start) start = timestamp;
                let progress = timestamp - start;
                let angleNow = easeOut(progress / spinTime) * rotation;
                ctx.setTransform(1, 0, 0, 1, 150, 150);
                ctx.rotate(angleNow * Math.PI / 180);
                drawWheel();
                if (progress < spinTime) {
                    requestAnimationFrame(rotate);
                } else {
                    spinning = false;
                    let finalAngle = (angleNow % 360);  
                    let prizeIndex = Math.floor((360 - finalAngle) / (360 / prizes.length)) % prizes.length;
                    let selectedPrize = prizes[prizeIndex];
                    document.getElementById("result").innerText = "🎉 You won: " + selectedPrize + "!";
                }
            }

            requestAnimationFrame(rotate);
        }

        function easeOut(t) {
            return --t * t * t + 1;
        }

        drawWheel();
    </script>
</body>
</html>
"""

# Embed JavaScript Wheel in Streamlit
components.html(html_code, height=500)