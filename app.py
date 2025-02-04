import streamlit as st
import sqlite3
import pandas as pd
import random

# Initialize SQLite database
def init_db():
    try:
        conn = sqlite3.connect("winners.db")
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS winners 
                          (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                           name TEXT NOT NULL, 
                           phone TEXT NOT NULL, 
                           prize TEXT NOT NULL)''')
        conn.commit()
    except sqlite3.Error as e:
        st.error(f"Database error: {e}")
    finally:
        if conn:
            conn.close()

# Save winner details to the database
def save_winner(name, phone, prize):
    try:
        conn = sqlite3.connect("winners.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO winners (name, phone, prize) VALUES (?, ?, ?)", (name, phone, prize))
        conn.commit()
    except sqlite3.Error as e:
        st.error(f"Failed to save winner: {e}")
    finally:
        if conn:
            conn.close()

# Retrieve all winners from the database
def get_winners():
    try:
        conn = sqlite3.connect("winners.db")
        df = pd.read_sql("SELECT * FROM winners ORDER BY id DESC", conn)  # Order by latest winners first
        return df
    except sqlite3.Error as e:
        st.error(f"Failed to retrieve winners: {e}")
        return pd.DataFrame()  # Return an empty DataFrame in case of error
    finally:
        if conn:
            conn.close()

# Initialize the database
init_db()

# Streamlit UI Setup
st.set_page_config(page_title="Valentine Spin Wheel", layout="wide")
st.markdown(""" 
    <style>
    .stApp { background-color: #ffebf0; }
    .title { text-align: center; font-size: 40px; color: #e60073; font-weight: bold; }
    .winner-box { background-color: #ffccdd; padding: 15px; border-radius: 10px; }
    .spin-wheel-container { width: 100%; height: 100%; display: flex; justify-content: center; align-items: center; }
    #spinWheel { width: 90% !important; height: 90% !important; }
    #spin_btn { background-color: #ff007f; border: none; color: white; padding: 15px 32px; font-size: 18px; cursor: pointer; border-radius: 50px; }
    #text { font-size: 1.5rem; margin-top: 20px; color: #ff007f; }
    .arrow { position: absolute; top: 50%; left: 50%; transform: translate(-50%, -100%); font-size: 30px; color: #ff007f; }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<div class='title'>💖 Valentine's Spin & Win 💖</div>", unsafe_allow_html=True)

# User Input Form
with st.form("spin_form"):
    name = st.text_input("Enter Your Name", placeholder="John Doe")
    phone = st.text_input("Enter Your Phone Number", placeholder="123-456-7890")
    submitted = st.form_submit_button("Spin the Wheel")
    
    if submitted:
        if not name or not phone:
            st.error("Please enter both your name and phone number.")
        else:
            st.success(f"🎉 Good Luck {name}! Spin the wheel and win a prize!")

            # Spin wheel HTML & JS Integration
            spin_wheel_html = """
            <div class="spin-wheel-container">
                <canvas id="spinWheel"></canvas>
                <div class="arrow">↑</div>
            </div>
            <button id="spin_btn">Spin</button>
            <div id="text"><p>Good Luck!</p></div>

            <script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/3.9.1/chart.min.js"></script>
            <script>
                const spinWheel = document.getElementById("spinWheel");
                const spinBtn = document.getElementById("spin_btn");
                const text = document.getElementById("text");

                const prizes = ["Lipstick", "Perfume", "Makeup Kit", "Nail Polish", "Face Mask", "Gift Voucher"];
                const spinColors = ["#E74C3C", "#7D3C98", "#2E86C1", "#138D75", "#F1C40F", "#D35400"];
                const size = [10, 10, 10, 10, 10, 10];

                let spinChart = new Chart(spinWheel, {
                    type: "pie",
                    data: {
                        labels: prizes,
                        datasets: [{
                            backgroundColor: spinColors,
                            data: size,
                        }],
                    },
                    options: {
                        responsive: true,
                        animation: { duration: 0 },
                        plugins: {
                            tooltip: { enabled: false },
                            legend: { display: false },
                            datalabels: {
                                rotation: 90,
                                color: "#ffffff",
                                formatter: (_, context) => context.chart.data.labels[context.dataIndex],
                                font: { size: 24 },
                            },
                        },
                    },
                });

                const generateValue = (angleValue) => {
                    const sliceAngle = 360 / prizes.length;
                    const prizeIndex = Math.floor((angleValue + (sliceAngle / 2)) / sliceAngle) % prizes.length;
                    text.innerHTML = `<p>Congratulations! You won ${prizes[prizeIndex]}</p>`;
                    spinBtn.disabled = false;

                    // Save the winner to Streamlit backend using postMessage
                    window.parent.postMessage({ "event": "winner", "prize": prizes[prizeIndex] }, "*");
                };

                let count = 0;
                let resultValue = 101;
                spinBtn.addEventListener("click", () => {
                    spinBtn.disabled = true;
                    text.innerHTML = `<p>Best Of Luck!</p>`;
                    let randomDegree = Math.floor(Math.random() * (355 - 0 + 1) + 0);
                    let rotationInterval = window.setInterval(() => {
                        spinChart.options.rotation += resultValue;
                        spinChart.update();
                        if (spinChart.options.rotation >= 360) {
                            count += 1;
                            resultValue -= 5;
                            spinChart.options.rotation = 0;
                        } else if (count > 15 && spinChart.options.rotation == randomDegree) {
                            generateValue(randomDegree);
                            clearInterval(rotationInterval);
                            count = 0;
                            resultValue = 101;
                        }
                    }, 10);
                });
            </script>
            """
            st.components.v1.html(spin_wheel_html, height=600)

# Handle Winner Data (Python backend)
if st.session_state.get('winner'):
    winner_info = st.session_state['winner']
    save_winner(name, phone, winner_info['prize'])
    st.subheader(f"🎉 Congratulations {name}, you won a {winner_info['prize']}! 🎉")

# Display Recent Winners
st.subheader("🎊 Recent Winners 🎊")
winners_df = get_winners()
if not winners_df.empty:
    st.table(winners_df[['name', 'phone', 'prize']])
else:
    st.info("No winners yet. Be the first to spin the wheel!")
