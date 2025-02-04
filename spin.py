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
        .pointer {
            position: absolute;
            top: -20px; left: 50%;
            transform: translateX(-50%);
            width: 0; height: 0;
            border-left: 15px solid transparent;
            border-right: 15px solid transparent;
            border-bottom: 30px solid red;
            z-index: 10;
        }
        .wheel {
            width: 300px; height: 300px;
            border-radius: 50%;
            border: 5px solid #ff4081;
            position: relative;
            display: inline-block;
            transition: transform 4s cubic-bezier(0.17, 0.67, 0.83, 0.67);
            background: conic-gradient(#ffcccb 0deg 72deg, #ff4081 72deg 144deg, #ff9966 144deg 216deg, #ff6600 216deg 288deg, #ff9933 288deg 360deg);
        }
        .wheel-text {
            position: absolute;
            top: 50%; left: 50%;
            transform-origin: center center;
            font-size: 14px;
            font-weight: bold;
            color: white;
            z-index: 1;
            text-align: center;
        }
        button {
            padding: 12px 20px;
            font-size: 18px;
            background: #ff4081;
            color: white;
            border: none;
            cursor: pointer;
            margin-top: 15px;
            border-radius: 5px;
        }
        button:hover { background: #ff0055; }
        #result {
            font-size: 20px;
            font-weight: bold;
            margin-top: 10px;
        }
    </style>
</head>
<body>
    <div class="wheel-container">
        <div class="pointer"></div>
        <div id="wheel" class="wheel">
            <!-- Each slice text is positioned in the center -->
            <div class="wheel-text" style="transform: translate(-50%, -50%) rotate(0deg) translateY(-120px)">💄 Free Lipstick</div>
            <div class="wheel-text" style="transform: translate(-50%, -50%) rotate(72deg) translateY(-120px)">🛍️ 10% Off</div>
            <div class="wheel-text" style="transform: translate(-50%, -50%) rotate(144deg) translateY(-120px)">💖 Free Gift</div>
            <div class="wheel-text" style="transform: translate(-50%, -50%) rotate(216deg) translateY(-120px)">🎁 20% Off</div>
            <div class="wheel-text" style="transform: translate(-50%, -50%) rotate(288deg) translateY(-120px)">💌 Thank You</div>
        </div>
    </div>
    <br>
    <button onclick="spinWheel()">🎰 Spin the Wheel</button>
    <p id="result"></p>

    <script>
        const prizes = ["💄 Free Lipstick", "🛍️ 10% Off", "💖 Free Gift", "🎁 20% Off", "💌 Thank You"];
        const totalSlices = prizes.length;
        const sliceAngle = 360 / totalSlices;
        let lastRotation = 0;

        function spinWheel() {
            let randomExtraSpins = Math.floor(Math.random() * 3 + 5) * 360;  // Ensures multiple full spins
            let randomOffset = Math.floor(Math.random() * 360);  // Random stop position
            let totalRotation = lastRotation + randomExtraSpins + randomOffset;

            // Apply the CSS rotation to the wheel
            document.getElementById("wheel").style.transform = `rotate(${totalRotation}deg)`;
            
            // Determine the prize based on the final rotation
            setTimeout(() => {
                let finalAngle = totalRotation % 360;  // Normalize to 0-360 degrees
                let prizeIndex = Math.floor((360 - finalAngle + sliceAngle / 2) / sliceAngle) % totalSlices;
                document.getElementById("result").innerText = "🎉 You won: " + prizes[prizeIndex] + "!";
            }, 4000);  // Wait for animation to complete
            
            lastRotation = totalRotation;  // Save rotation state for next spin
        }
    </script>
</body>
</html>
"""

# Embed HTML + JS in Streamlit
components.html(html_code, height=500)