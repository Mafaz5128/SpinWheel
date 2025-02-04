import streamlit as st
import pandas as pd
import random
import sqlite3

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

# Get a random prize from the list
def get_random_prize():
    prizes = ["Lipstick", "Perfume", "Makeup Kit", "Nail Polish", "Face Mask", "Gift Voucher"]
    return random.choice(prizes)

# Initialize the database
init_db()

# Streamlit UI Setup
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
    name = st.text_input("Enter Your Name", placeholder="John Doe")
    phone = st.text_input("Enter Your Phone Number", placeholder="123-456-7890")
    submitted = st.form_submit_button("Spin the Wheel")
    
    if submitted:
        if not name or not phone:
            st.error("Please enter both your name and phone number.")
        else:
            prize = get_random_prize()
            save_winner(name, phone, prize)
            st.success(f"🎉 Congratulations {name}, You won {prize}! 🎁")

            # Spin wheel HTML & JS Integration
            spin_wheel_html = """
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta http-equiv="X-UA-Compatible" content="IE=edge">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Spin Wheel</title>
                <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.2.1/css/all.min.css" />
                <script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/3.9.1/chart.min.js"></script>
                <script src="https://cdnjs.cloudflare.com/ajax/libs/chartjs-plugin-datalabels/2.1.0/chartjs-plugin-datalabels.min.js"></script>
                <style>
                    body { background-color: #f7f7f7; font-family: 'PT Serif', serif; }
                    h1 { color: #ff007f; text-align: center; font-size: 2rem; margin-top: 50px; }
                    .container { max-width: 600px; margin: auto; text-align: center; }
                    #spinWheel { width: 100%; height: 400px; }
                    #spin_btn { background-color: #ff007f; border: none; color: white; padding: 15px 32px; font-size: 18px; cursor: pointer; border-radius: 50px; }
                    #text { font-size: 1.5rem; margin-top: 20px; color: #ff007f; }
                </style>
            </head>
            <body>
                <div class="container">
                    <h1>Spin the Wheel and Win!</h1>
                    <canvas id="spinWheel"></canvas>
                    <button id="spin_btn">Spin</button>
                    <div id="text"><p>Good Luck!</p></div>
                </div>
                <script>
                    const spinWheel = document.getElementById("spinWheel");
                    const spinBtn = document.getElementById("spin_btn");
                    const text = document.getElementById("text");
                    
                    const spinValues = [
                        { minDegree: 61, maxDegree: 90, value: 100 },
                        { minDegree: 31, maxDegree: 60, value: 200 },
                        { minDegree: 0, maxDegree: 30, value: 300 },
                        { minDegree: 331, maxDegree: 360, value: 400 },
                        { minDegree: 301, maxDegree: 330, value: 500 },
                        { minDegree: 271, maxDegree: 300, value: 600 },
                        { minDegree: 241, maxDegree: 270, value: 700 },
                        { minDegree: 211, maxDegree: 240, value: 800 },
                        { minDegree: 181, maxDegree: 210, value: 900 },
                        { minDegree: 151, maxDegree: 180, value: 1000 },
                        { minDegree: 121, maxDegree: 150, value: 1100 },
                        { minDegree: 91, maxDegree: 120, value: 1200 },
                    ];
                    
                    const spinColors = ["#E74C3C", "#7D3C98", "#2E86C1", "#138D75", "#F1C40F", "#D35400", "#138D75", "#F1C40F", "#b163da", "#E74C3C", "#7D3C98", "#138D75"];
                    const size = [10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10];
                    
                    let spinChart = new Chart(spinWheel, {
                        type: "pie",
                        data: {
                            labels: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
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
                        for (let i of spinValues) {
                            if (angleValue >= i.minDegree && angleValue <= i.maxDegree) {
                                text.innerHTML = `<p>Congratulations, You Have Won ${i.value}!</p>`;
                                spinBtn.disabled = false;
                                break;
                            }
                        }
                    };
                    
                    let count = 0;
                    let resultValue = 101;
                    spinBtn.addEventListener("click", () => {
                        spinBtn.disabled = true;
                        text.innerHTML = `<p>Best Of Luck!</p>`;
                        let randomDegree = Math.floor(Math.random() * (355 - 0 + 1) + 0);
                        let rotationInterval = window.setInterval(() => {
                            spinChart.options.rotation = spinChart.options.rotation + resultValue;
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
            </body>
            </html>
            """
            st.components.v1.html(spin_wheel_html, height=600)

# Display Recent Winners
st.subheader("🎊 Recent Winners 🎊")
winners = get_winners()
if not winners.empty:
    st.table(winners[['name', 'phone', 'prize']])
else:
    st.info("No winners yet. Be the first to spin the wheel!")
