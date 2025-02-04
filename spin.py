import streamlit as st
import streamlit.components.v1 as components

# Set Streamlit Page Config
st.set_page_config(page_title="Spin & Win | Valentine's Special", page_icon="🎡")

# App Title
st.title("🎡 Spin & Win - Valentine's Day Special!")
st.write("Click the **Spin the Wheel** button and try your luck!")

# HTML + JavaScript for Spin Wheel
html_code = """
<!DOCTYPE html>
<html>
<head>
    <style>
        body { text-align: center; font-family: Arial, sans-serif; }
        .wheel-container { position: relative; display: inline-block; }
        .wheel { width: 300px; height: 300px; border-radius: 50%; border: 5px solid #ff4081; }
        .pointer {
            position: absolute;
            top: -10px; left: 50%;
            transform: translateX(-50%);
            width: 0; height: 0;
            border-left: 15px solid transparent;
            border-right: 15px solid transparent;
            border-bottom: 30px solid red;
        }
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

        function drawWheel(rotationAngle = 0) {
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            ctx.save();
            ctx.translate(150, 150);
            ctx.rotate(rotationAngle);

            let startAngle = 0;
            for (let i = 0; i < prizes.length; i++) {
                ctx.beginPath();
                ctx.moveTo(0, 0);
                ctx.arc(0, 0, 150, startAngle, startAngle + sliceAngle);
                ctx.fillStyle = i % 2 === 0 ? "#ffcccb" : "#ff4081";
                ctx.fill();
                ctx.closePath();

                ctx.fillStyle = "black";
                ctx.font = "bold 14px Arial";
                ctx.textAlign = "center";
                ctx.save();
                ctx.rotate(startAngle + sliceAngle / 2);
                ctx.fillText(prizes[i], 90, 10);
                ctx.restore();

                startAngle += sliceAngle;
            }
            ctx.restore();
        }

        function spinWheel() {
            if (spinning) return;
            spinning = true;
            let totalRotation = Math.random() * 360 + 360 * 5;  
            let spinTime = 3000;
            let startTime = null;

            function rotate(timestamp) {
                if (!startTime) startTime = timestamp;
                let progress = timestamp - startTime;
                let easedProgress = easeOut(progress / spinTime);
                angle = easedProgress * totalRotation * (Math.PI / 180);
                drawWheel(angle);

                if (progress < spinTime) {
                    requestAnimationFrame(rotate);
                } else {
                    spinning = false;
                    let finalAngle = (angle % (2 * Math.PI));  
                    let prizeIndex = Math.floor(((2 * Math.PI) - finalAngle) / sliceAngle) % prizes.length;
                    document.getElementById("result").innerText = "🎉 You won: " + prizes[prizeIndex] + "!";
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

# Embed HTML + JS in Streamlit
components.html(html_code, height=500)