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
        body { text-align: center; font-family: Arial, sans-serif; background-color: #ffe6f2; }
        h1 { color: #e60073; }
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
        table {
            width: 70%;
            margin: 20px auto;
            border-collapse: collapse;
            background: white;
        }
        th, td {
            border: 1px solid #ff4081;
            padding: 10px;
            text-align: center;
        }
        th {
            background: #ff4081;
            color: white;
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

    <div class="wheel-container">
        <div class="pointer"></div>
        <canvas id="wheel" width="300" height="300"></canvas>
    </div>

    <br>
    <button id="spinBtn" onclick="spinWheel()">🎰 Spin the Wheel</button>
    <p id="result"></p>

    <h2>🎖 Winners List 🎖</h2>
    <table>
        <thead>
            <tr>
                <th>Customer Name</th>
                <th>Prize Won</th>
                <th>Coupon Code</th>
            </tr>
        </thead>
        <tbody id="winnersTable"></tbody>
    </table>

    <script>
        let playerName = "";
        let playerPhone = "";
        let winnersList = [];

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
            alert(`Welcome ${playerName}! Click below to spin the wheel.`);
        }

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
                let couponCode = generateCouponCode();
                document.getElementById("result").innerText = `🎉 Congratulations ${playerName}! You won: ${finalSector.label} (Code: ${couponCode})`;
                
                // Save winner data
                winnersList.push({ name: playerName, prize: finalSector.label, code: couponCode });
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
            if (!playerName || !playerPhone) {
                alert("Please enter your details first.");
                return;
            }
            if (!angVel) angVel = rand(0.25, 0.45);
            requestAnimationFrame(frame);
        }

        function updateWinnersTable() {
            const tableBody = document.getElementById("winnersTable");
            tableBody.innerHTML = "";
            winnersList.forEach(winner => {
                let row = `<tr><td>${winner.name}</td><td>${winner.prize}</td><td>${winner.code}</td></tr>`;
                tableBody.innerHTML += row;
            });
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
st.components.v1.html(html_code, height=700, scrolling=True)
