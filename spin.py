import streamlit as st
import streamlit.components.v1 as components

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

        function spinWheel() {
            if (!playerName || !playerPhone) {
                alert("Please enter your details first.");
                return;
            }
            const prizes = ["Get 20% Off", "Mystery Box", "Buy 1 Get 1", "Thank You", "Lipstick", "Voucher"];
            const selectedPrize = prizes[Math.floor(Math.random() * prizes.length)];
            const couponCode = generateCouponCode();
            document.getElementById("result").innerText = `🎉 Congratulations ${playerName}! You won: ${selectedPrize} (Code: ${couponCode})`;
            winnersList.push({ name: playerName, prize: selectedPrize, code: couponCode });
            updateWinnersTable();
        }

        function updateWinnersTable() {
            const tableBody = document.getElementById("winnersTable");
            tableBody.innerHTML = "";
            winnersList.forEach(winner => {
                let row = `<tr><td>${winner.name}</td><td>${winner.prize}</td><td>${winner.code}</td></tr>`;
                tableBody.innerHTML += row;
            });
        }
    </script>

</body>
</html>
"""

# Embed HTML in Streamlit
st.components.v1.html(html_code, height=700, scrolling=True)
