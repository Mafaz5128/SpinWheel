import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Valentine Spin Wheel", layout="wide")
# HTML and CSS for the Spin Wheel App
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
        .balloon {
            position: absolute;
            width: 50px;
            height: 80px;
            background-color: #4169E1;
            border-radius: 50%;
            animation: floatBalloon 5s infinite ease-in-out, moveBalloon 10s linear infinite;
        }
        .heart {
            position: absolute;
            font-size: 40px;
            color: red;
            animation: floatHeart 4s infinite ease-in-out, moveHeart 7s linear infinite;
        }

        @keyframes floatBalloon {
            0% {
                bottom: -80px;
                left: 50%;
                opacity: 1;
            }
            100% {
                bottom: 100%;
                left: 50%;
                opacity: 0.5;
            }
        }

        @keyframes moveBalloon {
            0% {
                left: 50%;
                transform: rotate(0deg);
            }
            25% {
                left: 60%;
                transform: rotate(15deg);
            }
            50% {
                left: 40%;
                transform: rotate(-15deg);
            }
            75% {
                left: 30%;
                transform: rotate(10deg);
            }
            100% {
                left: 50%;
                transform: rotate(0deg);
            }
        }

        @keyframes floatHeart {
            0% {
                bottom: -50px;
                left: 50%;
                opacity: 1;
            }
            100% {
                bottom: 100%;
                left: 50%;
                opacity: 0.5;
            }
        }

        @keyframes moveHeart {
            0% {
                left: 50%;
            }
            25% {
                left: 60%;
            }
            50% {
                left: 40%;
            }
            75% {
                left: 20%;
            }
            100% {
                left: 50%;
            }
        }
    </style>
</head>
<body>

    <h1>💖 Valentine's Spin & Win 💖</h1>

    <div>
        <input type="text" id="name" placeholder="Enter Your Name">
        <button onclick="startSpin()">Proceed to Spin</button>
    </div>

    <div id="goodLuck"></div>

    <div class="wheel-container">
        <div class="pointer"></div>
        <canvas id="wheel" width="300" height="300"></canvas>
    </div>

    <br>
    <button id="spinBtn" onclick="spinWheel()">🎰 Spin the Wheel</button>
    <p id="result"></p>
    <p id="instructions"></p>
    <script>
        let playerName = "";
        let winnersList = JSON.parse(localStorage.getItem('winnersList')) || [];

        function generateCouponCode() {
            return 'VC-' + Math.random().toString(36).substring(2, 8).toUpperCase();
        }

        function startSpin() {
            playerName = document.getElementById("name").value;

            if (!playerName) {
                alert("Please enter your name.");
                return;
            }
            document.getElementById("goodLuck").innerText = `Good luck, ${playerName}! Click below to spin the wheel.`;
            showBalloonsAndHearts();
        }

        const sectors = [
            { color: "#FF0000", text: "#FFFFFF", label: "20% OFF 🎉" },
            { color: "#FF7F00", text: "#FFFFFF", label: "Free Delivery 🚚" },
            { color: "#00FF00", text: "#FFFFFF", label: "Win a Perfume! 💐" },
            { color: "#0000FF", text: "#FFFFFF", label: "BOGO – Any Item! 🛍️" },
            { color: "#8B00FF", text: "#FFFFFF", label: "Couple Watch! ⌚" },
            { color: "#4B0082", text: "#FFFFFF", label: "LKR 5000 Voucher 💵" }
        ];

        // Define weights for each prize. The higher the number, the more likely it is to be chosen.
        const weights = [1, 1, 1, 0, 0, 0]; // The second prize (Free Delivery) has a weight of 0, meaning it will never be selected

        const rand = (m, M) => Math.random() * (M - m) + m;
        const tot = sectors.length;
        const canvas = document.querySelector("#wheel");
        const ctx = canvas.getContext("2d");
        const dia = canvas.width;
        const rad = dia / 2;
        const PI = Math.PI;
        const TAU = 2 * PI;
        const arc = TAU / tot;

        let angVel = 0;
        let ang = 0;
        const friction = 0.991;
        const getIndex = () => {
            let totalWeight = weights.reduce((sum, weight) => sum + weight, 0); // Calculate total weight
            let randomWeight = Math.random() * totalWeight; // Select a random weight

            // Find the index based on the random weight
            let accumulatedWeight = 0;
            for (let i = 0; i < weights.length; i++) {
                accumulatedWeight += weights[i];
                if (randomWeight < accumulatedWeight) {
                    return i;
                }
            }
            return 0; // Default case if no index is found (shouldn't happen)
        };

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
            ctx.font = "bold 10px Arial";
            ctx.fillText(sector.label, rad - 10, 10);
            ctx.restore();
        }

        function rotate() {
            canvas.style.transform = `rotate(${ang - PI / 2}rad)`;
        }

        function frame() {
            if (!angVel) {
                const finalSector = sectors[getIndex()];
                let couponCode = generateCouponCode();
                document.getElementById("result").innerText = `🎉 Congratulations ${playerName}! You won: ${finalSector.label} (Code: ${couponCode})`;
                document.getElementById("instructions").innerHTML = `📸 Take a screenshot and send it to Shop4me.lk on <a href='https://wa.me/94784727313' target='_blank'>WhatsApp</a> to claim your prize!`;
                // Save winner data
                winnersList.push({ name: playerName, prize: finalSector.label, code: couponCode });
                localStorage.setItem('winnersList', JSON.stringify(winnersList));
                updateWinnersTable();

                return;
            }
            angVel *= friction;
            if (angVel < 0.002) angVel = 0;
            ang += angVel;
            ang %= TAU;
            rotate();
            requestAnimationFrame(frame);
        }

        function spinWheel() {
            if (!playerName) {
                alert("Please enter your name first.");
                return;
            }
            if (!angVel) angVel = rand(0.25, 0.45);
            requestAnimationFrame(frame);
        }

        function showBalloonsAndHearts() {
            for (let i = 0; i < 5; i++) {
                const balloon = document.createElement("div");
                balloon.classList.add("balloon");
                balloon.style.left = `${Math.random() * 100}%`;
                balloon.style.animationDuration = `${Math.random() * 2 + 4}s`;
                document.body.appendChild(balloon);
            }
            for (let i = 0; i < 3; i++) {
                const heart = document.createElement("div");
                heart.classList.add("heart");
                heart.innerText = "❤️";
                heart.style.left = `${Math.random() * 100}%`;
                heart.style.animationDuration = `${Math.random() * 2 + 4}s`;
                document.body.appendChild(heart);
            }
        }

        function init() {
            sectors.forEach(drawSector);
            rotate();
            updateWinnersTable();
        }

        init();
    </script>

</body>
</html>
"""

# Embed HTML in Streamlit
st.components.v1.html(html_code, height=1000, scrolling=True)
