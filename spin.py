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
            top: -10px; left: 50%;
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
            transition: transform 4s cubic-bezier(0.17, 0.67, 0.83, 0.67);
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
        <img id="wheel" class="wheel" src="https://upload.wikimedia.org/wikipedia/commons/thumb/7/75/Roulette_wheel_blank.svg/300px-Roulette_wheel_blank.svg.png">
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
            
            document.getElementById("wheel").style.transform = `rotate(${totalRotation}deg)`;
            
            setTimeout(() => {
                let finalAngle = totalRotation % 360;  // Normalize to 0-360 degrees
                let prizeIndex = Math.floor((360 - finalAngle + sliceAngle / 2) / sliceAngle) % totalSlices;
                document.getElementById("result").innerText = "🎉 You won: " + prizes[prizeIndex] + "!";
            }, 4000);  // Wait for animation to complete
            
            lastRotation = totalRotation;  // Save rotation state
        }
    </script>
</body>
</html>
"""

# Embed HTML + JS in Streamlit
components.html(html_code, height=500)