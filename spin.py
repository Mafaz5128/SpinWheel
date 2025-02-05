import streamlit as st
import streamlit.components.v1 as components

# Set Streamlit Page Config
st.set_page_config(page_title="Spin & Win | Valentine's Special", page_icon="🎡", layout ='wide')

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
            top: -15px; left: 50%;
            transform: translateX(-50%);
            width: 0; height: 0;
            border-left: 12px solid transparent;
            border-right: 12px solid transparent;
            border-bottom: 25px solid red;
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
    </style>
</head>
<body>
    <div class="wheel-container">
        <div class="pointer"></div>
        <canvas id="wheel" width="300" height="300"></canvas>
    </div>
    <br>
    <button id="spin">🎰 Spin the Wheel</button>
    <p id="result"></p>

    <script>
        const sectors = [
            { color: "#FF0000", text: "#333333", label: "Get 20% Off" },
            { color: "#FF7F00", text: "#333333", label: "Mystry Box" },
            { color: "#00FF00", text: "#333333", label: "Buy 1 Get 1" },
            { color: "#0000FF", text: "#333333", label: "Thank You" },
            { color: "#8B00FF", text: "#333333", label: "Lip Stick" },
            { color: "#4B0082", text: "#333333", label: "Voucher" }
        ];

        const events = {
            listeners: {},
            addListener: function (eventName, fn) {
                this.listeners[eventName] = this.listeners[eventName] || [];
                this.listeners[eventName].push(fn);
            },
            fire: function (eventName, ...args) {
                if (this.listeners[eventName]) {
                    for (let fn of this.listeners[eventName]) {
                        fn(...args);
                    }
                }
            }
        };

        const rand = (m, M) => Math.random() * (M - m) + m;
        const tot = sectors.length;
        const spinEl = document.querySelector("#spin");
        const canvas = document.querySelector("#wheel");
        const ctx = canvas.getContext("2d");
        const dia = canvas.width;
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

            // COLOR
            ctx.beginPath();
            ctx.fillStyle = sector.color;
            ctx.moveTo(rad, rad);
            ctx.arc(rad, rad, rad, ang, ang + arc);
            ctx.lineTo(rad, rad);
            ctx.fill();

            // TEXT
            ctx.translate(rad, rad);
            ctx.rotate(ang + arc / 2);
            ctx.textAlign = "right";
            ctx.fillStyle = sector.text;
            ctx.font = "bold 18px 'Lato', sans-serif";
            ctx.fillText(sector.label, rad - 8, 8);

            ctx.restore();
        }

        function rotate() {
            const sector = sectors[getIndex()];
            canvas.style.transform = `rotate(${ang - PI / 2}rad)`;

            spinEl.textContent = !angVel ? "SPIN" : sector.label;
            spinEl.style.background = sector.color;
            spinEl.style.color = sector.text;
        }

        function frame() {
            if (!angVel && spinButtonClicked) {
                const finalSector = sectors[getIndex()];
                events.fire("spinEnd", finalSector);
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

        events.addListener("spinEnd", (sector) => {
            document.getElementById("result").innerText = `🎉 You won: ${sector.label}`;
        });
    </script>
</body>
</html>
"""

# Embed HTML + JS in Streamlit
components.html(html_code, height=400)
