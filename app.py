import streamlit as st
import streamlit.components.v1 as components
import pandas as pd

# Initialize session state to store the winners table and spin status
if 'winners_table' not in st.session_state:
    st.session_state.winners_table = []

if 'has_spun' not in st.session_state:import streamlit as st
import random
import time
import plotly.graph_objects as go

# Valentine's Day Theme Colors
background_color = "#FFE6E6"
button_color = "#FF4C4C"
text_color = "#D63384"
prizes = ["10% Off", "Free Lipstick", "20% Off", "Buy 1 Get 1", "Free Shipping", "Gift Hamper"]
colors = ["#FF9999", "#FF6666", "#FF4C4C", "#FFB6C1", "#FF69B4", "#FF1493"]

# Custom CSS for Valentine's Theme
st.markdown(f"""
    <style>
        body {{
            background-color: {background_color};
            font-family: 'Arial', sans-serif;
        }}
        .stButton>button {{
            background-color: {button_color} !important;
            color: white !important;
            border-radius: 50px !important;
            font-size: 20px !important;
            padding: 12px 24px !important;
            border: none !important;
        }}
        .stTextInput>div>div>input {{
            border-radius: 20px !important;
            border: 2px solid {text_color} !important;
        }}
    </style>
""", unsafe_allow_html=True)

# Function to create a spin wheel
def draw_wheel(rotation_angle=0):
    fig = go.Figure()
    fig.add_trace(go.Pie(
        labels=prizes,
        values=[1] * len(prizes),
        textinfo="label",
        marker=dict(colors=colors, line=dict(color="black", width=1.5)),
        hole=0.2,
    ))
    fig.update_traces(rotation=rotation_angle)
    fig.add_shape(
        type="path",
        path="M 0.5 1 L 0.45 0.8 L 0.55 0.8 Z",
        xref="paper", yref="paper",
        line=dict(color="black"),
        fillcolor="red"
    )
    fig.update_layout(
        showlegend=False,
        margin=dict(l=10, r=10, t=10, b=10),
        height=400,
        width=400,
        annotations=[
            dict(text="🎡 Spin Me!", x=0.5, y=0.5, font_size=20, showarrow=False, font=dict(color="black"))
        ]
    )
    return fig

# UI
st.title("💖 Valentine's Day Spin & Win! 💖")
st.markdown("🎁 Spin the wheel and win exciting prizes! Spread the love this Valentine's Day! 💕")

if "rotation_angle" not in st.session_state:
    st.session_state.rotation_angle = 0
if "wheel_chart" not in st.session_state:
    st.session_state.wheel_chart = st.empty()

st.session_state.wheel_chart.plotly_chart(draw_wheel(st.session_state.rotation_angle))

if st.button("🎡 Spin the Wheel!"):
    with st.spinner("Spinning... 🎠"):
        total_time = 2  # Reduced for better UX
        steps = 50  
        for _ in range(steps):
            st.session_state.rotation_angle += random.randint(15, 30)  
            st.session_state.rotation_angle %= 360  
            if _ % 5 == 0:  # Update less frequently to avoid duplicate errors
                st.session_state.wheel_chart.plotly_chart(draw_wheel(st.session_state.rotation_angle))
            time.sleep(total_time / steps)
    
    sector_size = 360 / len(prizes)
    winning_index = int((st.session_state.rotation_angle % 360) / sector_size)
    selected_prize = prizes[winning_index]

    st.success(f"🎉 Congratulations! You won: {selected_prize} 🎁")

# Collect user details
st.subheader("💌 Claim Your Prize!")
user_name = st.text_input("Enter your name (Optional)")
user_email = st.text_input("Enter your email to receive the prize (Optional)")

if st.button("Submit Details"):
    if user_email:
        st.success("✅ Your prize will be sent to your email soon! 💌")
    else:
        st.warning("⚠ Please enter a valid email to receive the prize.")
    st.session_state.has_spun = False

# Embed the updated HTML, CSS, and JS directly into the Streamlit app
html_code = """
<html lang="en">
  <head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Valentine's Spin & Win</title>
    <!-- Google Font -->
    <link
      href="https://fonts.googleapis.com/css2?family=Poppins:wght@500;600&display=swap"
      rel="stylesheet"
    />
    <!-- Stylesheet -->
    <style>
      * {
        padding: 0;
        margin: 0;
        box-sizing: border-box;
        font-family: "Poppins", sans-serif;
      }
      body {
        height: 100vh;
        background: linear-gradient(135deg, #ffcccb, #ff477e);
      }
      .wrapper {
        width: 90%;
        max-width: 34.37em;
        max-height: 90vh;
        background-color: #ffffff;
        position: absolute;
        transform: translate(-50%, -50%);
        top: 50%;
        left: 50%;
        padding: 3em;
        border-radius: 1em;
        box-shadow: 0 4em 5em rgba(27, 8, 53, 0.2);
      }
      .container {
        position: relative;
        width: 100%;
        height: 100%;
      }
      #wheel {
        max-height: inherit;
        width: inherit;
        top: 0;
        padding: 0;
      }
      @keyframes rotate {
        100% {
          transform: rotate(360deg);
        }
      }
      #spin-btn {
        position: absolute;
        transform: translate(-50%, -50%);
        top: 50%;
        left: 50%;
        height: 26%;
        width: 26%;
        border-radius: 50%;
        cursor: pointer;
        border: 0;
        background: radial-gradient(#fdcf3b 50%, #d88a40 85%);
        color: #c66e16;
        text-transform: uppercase;
        font-size: 1.8em;
        letter-spacing: 0.1em;
        font-weight: 600;
      }
      img {
        position: absolute;
        width: 4em;
        top: 45%;
        right: -8%;
      }
      #final-value {
        font-size: 1.5em;
        text-align: center;
        margin-top: 1.5em;
        color: #202020;
        font-weight: 500;
      }
      @media screen and (max-width: 768px) {
        .wrapper {
          font-size: 12px;
        }
        img {
          right: -5%;
        }
      }
    </style>
  </head>
  <body>
    <div class="wrapper">
      <div class="container">
        <canvas id="wheel"></canvas>
        <button id="spin-btn">💖 Spin Now!</button>
        <img src="https://upload.wikimedia.org/wikipedia/commons/3/3e/Heart_arrow.svg" alt="spinner arrow" />
      </div>
      <div id="final-value">
        <p>Click On The Spin Button To Start</p>
      </div>
    </div>
    <!-- Chart JS -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/3.9.1/chart.min.js"></script>
    <!-- Chart JS Plugin for displaying text over chart -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/chartjs-plugin-datalabels/2.1.0/chartjs-plugin-datalabels.min.js"></script>
    <script>
      const wheel = document.getElementById("wheel");
      const spinBtn = document.getElementById("spin-btn");
      const finalValue = document.getElementById("final-value");
      const rotationValues = [
        { minDegree: 0, maxDegree: 30, value: "💄 Free Lipstick" },
        { minDegree: 31, maxDegree: 90, value: "🌹 10% Off Coupon" },
        { minDegree: 91, maxDegree: 150, value: "💖 Buy 1 Get 1 Free" },
        { minDegree: 151, maxDegree: 210, value: "🎁 Mystery Gift" },
        { minDegree: 211, maxDegree: 270, value: "💌 20% Off Next Purchase" },
        { minDegree: 271, maxDegree: 330, value: "💕 Free Beauty Consultation" },
        { minDegree: 331, maxDegree: 360, value: "🎉 Surprise Prize!" },
      ];
      const data = [16, 16, 16, 16, 16, 16];
      var pieColors = [
        "#ff477e",
        "#ff85a2",
        "#ff6188",
        "#ff92b1",
        "#ffccd5",
        "#ffb2d9",
      ];
      let myChart = new Chart(wheel, {
        plugins: [ChartDataLabels],
        type: "pie",
        data: {
          labels: ["💄", "🌹", "💖", "🎁", "💌", "💕"],
          datasets: [
            {
              backgroundColor: pieColors,
              data: data,
            },
          ],
        },
        options: {
          responsive: true,
          animation: { duration: 0 },
          plugins: {
            tooltip: false,
            legend: { display: false },
            datalabels: {
              color: "#ffffff",
              formatter: (_, context) =>
                context.chart.data.labels[context.dataIndex],
              font: { size: 24 },
            },
          },
        },
      });
      const valueGenerator = (angleValue) => {
        for (let i of rotationValues) {
          if (angleValue >= i.minDegree && angleValue <= i.maxDegree) {
            finalValue.innerHTML = `<p>You won: ${i.value}</p>`;
            spinBtn.disabled = false;
            break;
          }
        }
      };
      let count = 0;
      let resultValue = 101;
      spinBtn.addEventListener("click", () => {
        spinBtn.disabled = true;
        finalValue.innerHTML = `<p>Good Luck!</p>`;
        let randomDegree = Math.floor(Math.random() * (355 - 0 + 1) + 0);
        let rotationInterval = window.setInterval(() => {
          myChart.options.rotation = myChart.options.rotation + resultValue;
          myChart.update();
          if (myChart.options.rotation >= 360) {
            count += 1;
            resultValue -= 5;
            myChart.options.rotation = 0;
          } else if (count > 15 && myChart.options.rotation == randomDegree) {
            valueGenerator(randomDegree);
            clearInterval(rotationInterval);
            count = 0;
            resultValue = 101;
            // Add the winner to the table
            let winnerName = document.getElementById("name").value;
            let winnerPhone = document.getElementById("phone").value;
            let prizeWon = finalValue.innerText.replace("You won: ", "");
            let winnerEntry = { name: winnerName, phone: winnerPhone, prize: prizeWon };
            window.parent.postMessage({ action: 'add_winner', winner: winnerEntry }, "*");
            // Set the flag that the user has spun
            window.parent.postMessage({ action: 'set_spin_status', status: true }, "*");
          }
        }, 10);
      });
    </script>
  </body>
</html>
"""

# Display customer details form
st.title("💘 Valentine's Spin & Win! 🎡")
with st.form(key="customer_form"):
    customer_name = st.text_input("Enter your Name:")
    customer_phone = st.text_input("Enter your Phone Number:")
    submit_button = st.form_submit_button("Submit")

# If customer form is submitted, store customer info in session state
if submit_button:
    st.session_state.customer_info = {"name": customer_name, "phone": customer_phone}
    st.session_state.has_spun = False  # Allow them to spin

# If customer has already spun, show message and disable spin
if 'has_spun' in st.session_state and st.session_state.has_spun:
    st.warning("You've already spun the wheel! Thank you for participating.")
else:
    # Display the interactive spin wheel
    if 'customer_info' in st.session_state:
        customer_name = st.session_state.customer_info.get('name', 'N/A')
        customer_phone = st.session_state.customer_info.get('phone', 'N/A')

        st.subheader(f"Welcome, {customer_name} ({customer_phone})!")
        components.html(html_code, height=800)

    # Handle winner updates from the JavaScript message
    message = st.query_params.get('winner', None)
    if message:
        st.session_state.winners_table.append(message)
        st.session_state.has_spun = True  # User has spun, so lock them out for future spins
        st.experimental_rerun()

# Display the winners table interactively
if st.session_state.winners_table:
    st.subheader("🏆 Winners Table 🏆")
    winners_df = pd.DataFrame(st.session_state.winners_table)
    st.dataframe(winners_df)
