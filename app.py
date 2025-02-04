import streamlit as st
import streamlit.components.v1 as components

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
        <img src="https://cutewallpaper.org/24/yellow-arrow-png/155564497.jpg" alt="spinner arrow" />
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
          }
        }, 10);
      });
    </script>
  </body>
</html>
"""

# Render the updated HTML in the Streamlit app
st.title("💘 Valentine's Spin & Win! 🎡")
components.html(html_code, height=800)
