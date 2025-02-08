import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Valentine Spin Wheel", layout="wide")
html_code = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Valentine's Spin Wheel</title>
    <style>
        body {
            text-align: center;
            font-family: Arial, sans-serif;
            background-color: #ffe6f2;
            overflow: hidden;
        }
        h1 {
            color: #e60073;
        }
        .wheel-container {
            position: relative;
            display: inline-block;
            margin-top: 50px;
        }
        .pointer {
            position: absolute;
            top: -10px;
            left: 50%;
            transform: translateX(-50%);
            width: 0; height: 0;
            border-left: 15px solid transparent;
            border-right: 15px solid transparent;
            border-bottom: 30px solid black;
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
        button:hover {
            background: #ff0055;
        }
        #result {
            font-size: 18px;
            font-weight: bold;
            margin-top: 10px;
        }
        #goodLuck {
            font-size: 22px;
            font-weight: bold;
            color: #ff4081;
            margin-top: 20px;
        }
    </style>
</head>
<body>

    <h1>💖 Valentine's Spin & Win 💖</h1>

    <div>
        <input type="text" id="name" placeholder="Enter Your Name">
        <input type="text" id="phone" placeholder="Enter Your Phone Number">
        <button onclick="startSpin()">Proceed to Spin</button>
    </div>

    <div id="goodLuck"></div>

    <div class="wheel-container">
        <div class="pointer"></div>
        <canvas id="wheel" width="500" height="500"></canvas>
    </div>

    <br>
    <button id="spinBtn" onclick="spinWheel()">🎰 Spin the Wheel</button>
    <p id="result"></p>
    <p id="instructions"></p>

    <script>
        let playerName = "";
        let playerPhone = "";

        function generateCouponCode() {
            return 'VC-' + Math.random().toString(36).substring(2, 8).toUpperCase();
        }

        function startSpin() {
            playerName = document.getElementById("name").value;
            playerPhone = document.getElementById("phone").value;

            if (!playerName || !playerPhone) {
                alert("Please enter your name and phone number.");
                return;
            }
            document.getElementById("goodLuck").innerText = `Good luck, ${playerName}! Click below to spin the wheel.`;
        }

        const sectors = [
            { color: "#FF0000", text: "#FFFFFF", label: "20% OFF 🎉" },
            { color: "#FF7F00", text: "#FFFFFF", label: "Free Delivery 🚚" },
            { color: "#00FF00", text: "#FFFFFF", label: "Win a Perfume! 💐" },
            { color: "#0000FF", text: "#FFFFFF", label: "BOGO – Any Item! 🛍️" },
            { color: "#8B00FF", text: "#FFFFFF", label: "Couple Watch! ⌚" },
            { color: "#4B0082", text: "#FFFFFF", label: "LKR 5000 Voucher 💵" }
        ];

        const canvas = document.querySelector("#wheel");
        const ctx = canvas.getContext("2d");
        const dia = canvas.width;
        const rad = dia / 2;
        const PI = Math.PI;
        const TAU = 2 * PI;
        const arc = TAU / sectors.length;

        let angVel = 0;
        let ang = 0;
        const friction = 0.98;

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
            if (angVel > 0.002) {
                angVel *= friction; // Smooth slowing down
                ang += angVel;
                ang %= TAU;
                rotate();
                requestAnimationFrame(frame);
            } else {
                angVel = 0;
                let winningIndex = 3; // CHOOSE THE PRIZE INDEX HERE (0-5)
                let winningAngle = TAU - (winningIndex * arc) - (arc / 2);
                ang = winningAngle;
                rotate();

                let finalSector = sectors[winningIndex];
                let couponCode = generateCouponCode();
                document.getElementById("result").innerText = `🎉 Congratulations ${playerName}! You won: ${finalSector.label} (Code: ${couponCode})`;
                document.getElementById("instructions").innerHTML = `📸 Take a screenshot and send it to Shop4me.lk on <a href='https://wa.me/94701234567' target='_blank'>WhatsApp</a> to claim your prize!`;
            }
        }

        function spinWheel() {
            if (!playerName || !playerPhone) {
                alert("Please enter your details first.");
                return;
            }
            angVel = Math.random() * 0.4 + 0.25;
            requestAnimationFrame(frame);
        }

        function init() {
            sectors.forEach(drawSector);
            rotate();
        }

        init();
    </script>

</body>
</html>
"""
# Embed HTML in Streamlit
st.components.v1.html(html_code, height=1000, scrolling=True)
