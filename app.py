import streamlit as st
import pandas as pd
import random
import sqlite3

def init_db():
    conn = sqlite3.connect("winners.db")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS winners 
                      (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, phone TEXT, prize TEXT)''')
    conn.commit()
    conn.close()

def save_winner(name, phone, prize):
    conn = sqlite3.connect("winners.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO winners (name, phone, prize) VALUES (?, ?, ?)", (name, phone, prize))
    conn.commit()
    conn.close()

def get_winners():
    conn = sqlite3.connect("winners.db")
    df = pd.read_sql("SELECT * FROM winners", conn)
    conn.close()
    return df

def get_random_prize():
    prizes = ["Lipstick", "Perfume", "Makeup Kit", "Nail Polish", "Face Mask", "Gift Voucher"]
    return random.choice(prizes)

# Initialize DB
init_db()

# UI Setup
st.set_page_config(page_title="Valentine Spin Wheel", layout="wide")
st.markdown(""" 
    <style>
    .stApp { background-color: #ffebf0; }
    .title { text-align: center; font-size: 40px; color: #e60073; font-weight: bold; }
    .winner-box { background-color: #ffccdd; padding: 15px; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<div class='title'>💖 Valentine's Spin & Win 💖</div>", unsafe_allow_html=True)

# User Input Form
with st.form("spin_form"):
    name = st.text_input("Enter Your Name")
    phone = st.text_input("Enter Your Phone Number")
    submitted = st.form_submit_button("Spin the Wheel")
    
    if submitted and name and phone:
        prize = get_random_prize()
        save_winner(name, phone, prize)
        st.success(f"🎉 Congratulations {name}, You won {prize}! 🎁")
        
        # Show Spin Wheel
        spin_wheel_html = """
        <html>
        <head>
        <style>
            .ui-wheel-of-fortune {
                --_items: 6;
                all: unset;
                aspect-ratio: 1 / 1;
                container-type: inline-size;
                display: grid;
                position: relative;
                width: 100%;
            }

            .ui-wheel-of-fortune::after {
                aspect-ratio: 1/cos(30deg);
                background-color: crimson;
                clip-path: polygon(50% 100%,100% 0,0 0);
                content: "";
                height: 4cqi;
                position: absolute;
                place-self: start center;
                scale: 1.4;
            }

            .ui-wheel-of-fortune > * { position: absolute; }

            button {
                aspect-ratio: 1 / 1;
                background: hsla(0, 0%, 100%, .8);
                border: 0;
                border-radius: 50%;
                cursor: pointer;
                font-size: 5cqi;
                place-self: center;
                width: 20cqi;
            }

            ul {
                all: unset;
                clip-path: inset(0 0 0 0 round 50%);
                display: grid;
                inset: 0;
                place-content: center start;

                li {
                    align-content: center;
                    aspect-ratio: 1 / calc(2 * tan(180deg / var(--_items)));
                    background: hsl(calc(360deg / var(--_items) * calc(var(--_idx))), 100%, 75%);
                    clip-path: polygon(0% 0%, 100% 50%, 0% 100%);
                    display: grid;
                    font-size: 5cqi;
                    grid-area: 1 / -1;
                    padding-left: 1ch;
                    rotate: calc(360deg / var(--_items) * calc(var(--_idx) - 1));
                    transform-origin: center right;
                    user-select: none;
                    width: 50cqi;
                }

                li:nth-of-type(1) { --_idx: 1; }
                li:nth-of-type(2) { --_idx: 2; }
                li:nth-of-type(3) { --_idx: 3; }
                li:nth-of-type(4) { --_idx: 4; }
                li:nth-of-type(5) { --_idx: 5; }
                li:nth-of-type(6) { --_idx: 6; }
            }
        </style>
        <script>
            function wheelOfFortune(selector) {
                const node = document.querySelector(selector);
                if (!node) return;

                const spin = node.querySelector('button');
                const wheel = node.querySelector('ul');
                let animation;
                let previousEndDegree = 0;

                spin.addEventListener('click', () => {
                    if (animation) {
                        animation.cancel();
                    }

                    const randomAdditionalDegrees = Math.random() * 360 + 1800;
                    const newEndDegree = previousEndDegree + randomAdditionalDegrees;

                    animation = wheel.animate([
                        { transform: `rotate(${previousEndDegree}deg)` },
                        { transform: `rotate(${newEndDegree}deg)` }
                    ], {
                        duration: 4000,
                        direction: 'normal',
                        easing: 'cubic-bezier(0.440, -0.205, 0.000, 1.130)',
                        fill: 'forwards',
                        iterations: 1
                    });

                    previousEndDegree = newEndDegree;
                });
            }
            wheelOfFortune('.ui-wheel-of-fortune');
        </script>
        </head>
        <body>
        <div class="ui-wheel-of-fortune">
            <ul>
                <li>Lipstick</li>
                <li>Perfume</li>
                <li>Makeup Kit</li>
                <li>Nail Polish</li>
                <li>Face Mask</li>
                <li>Gift Voucher</li>
            </ul>
            <button type="button">SPIN</button>
        </div>
        </body>
        </html>
        """
        st.components.v1.html(spin_wheel_html, height=500)

# Display Winners List
st.subheader("🎊 Recent Winners 🎊")
winners = get_winners()
st.table(winners[['name', 'phone', 'prize']])
