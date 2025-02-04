import streamlit as st
import streamlit.components.v1 as components

# HTML and JavaScript code for the Valentine's Day spin wheel
spin_wheel_html = """
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
            width: 350px; height: 350px;
            border-radius: 50%;
            border: 5px solid #ff4081;
            position: relative;
            display: inline-block;
            transition: transform 4s cubic-bezier(0.17, 0.67, 0.83, 0.67);
            background: conic-gradient(#FFB6C1 0deg 45deg, #FF69B4 45deg 90deg, #FFB6C1 90deg 135deg, #FF69B4 135deg 180deg, #FFB6C1 180deg 225deg, #FF69B4 225deg 270deg, #FFB6C1 270deg 315deg, #FF69B4 315deg 360deg);
        }
        .wheel-text {
            position: absolute;
            top: 50%; left: 50%;
            transform-origin: center center;
            font-size: 16px;
            font-weight: bold;
            color: white;
            z-index: 1;
            text-align: center;
        }
        button {
            padding: 12px 20px;
            font-size: 18px;
            background: #FF4081;
            color: white;
            border: none;
            cursor: pointer;
            margin-top: 15px;
            border-radius: 5px;
        }
        button:hover { background: #FF0055; }
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
            <div class="wheel-text" style="transform: translate(-50%, -50%) rotate(0deg) translateY(-120px)">💝 Free Rose</div>
            <div class="wheel-text" style="transform: translate(-50%, -50%) rotate(45deg) translateY(-120px)">💐 10% Off</div>
            <div class="wheel-text" style="transform: translate(-50%, -50%) rotate(90deg) translateY(-120px)">🌹 Free Chocolate</div>
            <div class="wheel-text" style="transform: translate(-50%, -50%) rotate(135deg) translateY(-120px)">💖 Free Gift</div>
            <div class="wheel-text" style="transform: translate(-50%, -50%) rotate(180deg) translateY(-120px)">🍫 20% Off</div>
            <div class="wheel-text" style="transform: translate(-50%, -50%) rotate(225deg) translateY(-120px)">💌 Thank You</div>
            <div class="wheel-text" style="transform: translate(-50%, -50%) rotate(270deg) translateY(-120px)">🎁 Free Lipstick</div>
            <div class="wheel-text" style="transform: translate(-50%, -50%) rotate(315deg) translateY(-120px)">💍 Free Jewelry</div>
        </div>
    </div>
    <br>
    <button id="spin">🎰 Spin the Wheel</button>
    <p id="result"></p>

    <script>
        const sectors = [
          { color: "#FFB6C1", text: "#333333", label: "💝 Free Rose" },
          { color: "#FF69B4", text: "#333333", label: "💐 10% Off" },
          { color: "#FFB6C1", text: "#333333", label: "🌹 Free Chocolate" },
          { color: "#FF69B4", text: "#333333", label: "💖 Free Gift" },
          { color: "#FFB6C1", text: "#333333", label: "🍫 20% Off" },
          { color: "#FF69B4", text: "#333333", label: "💌 Thank You" },
          { color: "#FFB6C1", text: "#333333", label: "🎁 Free Lipstick" },
          { color: "#FF69B4", text: "#333333", label: "💍 Free Jewelry" }
        ];

        const rand = (m, M) => Math.random() * (M - m) + m;
        const tot = sectors.length;
        const spinEl = document.querySelector("#spin");
        const ctx = document.querySelector("#wheel").getContext("2d");
        const dia = ctx.canvas.width;
        const rad = dia / 2;
        const PI = Math.PI;
        const TAU = 2 * PI;
        const arc = TAU / sectors.length;

        const friction = 0.991; 
        let angVel = 0; 
        let ang = 0; 

        let spinButtonClicked = false;

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
          ctx.font = "bold 16px 'Lato', sans-serif";
          ctx.fillText(sector.label, rad - 10, 10);

          ctx.restore();
        }

        function rotate() {
          const sector = sectors[getIndex()];
          ctx.canvas.style.transform = `rotate(${ang - PI / 2}rad)`;

          spinEl.textContent = !angVel ? "SPIN" : sector.label;
          spinEl.style.background = sector.color;
          spinEl.style.color = sector.text;
        }

        function frame() {
          if (!angVel && spinButtonClicked) {
            const finalSector = sectors[getIndex()];
            document.getElementById("result").innerText = `🎉 You won: ${finalSector.label}`;
            spinButtonClicked = false; 
            return;
          }

          angVel *= friction; 
          if (angVel < 0.002) angVel = 0; 
          ang += angVel; 
          ang %= TAU; 
          rotate();
        }

        function engine() {
          frame();
          requestAnimationFrame(engine);
        }

        function init() {
          sectors.forEach(drawSector);
          rotate(); 
          engine(); 
          spinEl.addEventListener("click", () => {
            if (!angVel) angVel = rand(0.25, 0.45);
            spinButtonClicked = true;
          });
        }

        init();
    </script>
</body>
</html>
"""

# Streamlit app
st.title("Valentine's Day Spin Wheel")

# Render the HTML and JS code inside a Streamlit component
components.html(spin_wheel_html, height=600)

# Display the result of the spin
st.write("Spin the wheel to see what you win!")