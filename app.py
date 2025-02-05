import streamlit as st
import streamlit.components.v1 as components

# Streamlit UI Setup
st.set_page_config(page_title="Valentine Spin Wheel", layout="wide")

# Display large greeting message
st.markdown("<h1 style='text-align: center; color: #e60073;'>💖 Valentine's Spin & Win 💖</h1>", unsafe_allow_html=True)

# User Input Form
with st.form("spin_form"):
    name = st.text_input("Enter Your Name", placeholder="John Doe")
    phone = st.text_input("Enter Your Phone Number", placeholder="123-456-7890")
    submitted = st.form_submit_button("Proceed to Spin")

if submitted:
    if not name or not phone:
        st.error("Please enter both your name and phone number.")
    else:
        st.session_state["player_name"] = name
        st.session_state["player_phone"] = phone
        st.session_state["can_spin"] = True
        st.success(f"🎉 Welcome {name}! Click below to spin the wheel.")

        # Display large greeting for spin action
        st.markdown(f"<h2 style='text-align: center; color: #ff4081;'>Good Luck, {name}!</h2>", unsafe_allow_html=True)

# HTML & JavaScript for Spin Wheel and Winners Table
html_code = """
<!DOCTYPE html>
<html>
<head>
    <script>
        function sendPrizeToStreamlit(name, phone, prize) {
            window.parent.postMessage({ "name": name, "phone": phone, "prize": prize }, "*");
            addToTable(name, phone, prize);
        }

        function addToTable(name, phone, prize) {
            let table = document.getElementById("winnersTable");
            let row = table.insertRow(-1);
            let cell1 = row.insertCell(0);
            let cell2 = row.insertCell(1);
            let cell3 = row.insertCell(2);
            cell1.innerHTML = name;
            cell2.innerHTML = phone;
            cell3.innerHTML = prize;
        }

        window.addEventListener("message", (event) => {
            if (event.data.prize) {
                document.getElementById("result").innerText = `🎉 Congratulations! You won: ${event.data.prize}`;
                sendPrizeToStreamlit(event.data.name, event.data.phone, event.data.prize);
            }
        });
    </script>
    <style>
        body { text-align: center; font-family: Arial, sans-serif; }
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
            margin-top: 20px;
            border-collapse: collapse;
            width: 80%;
            margin-left: auto;
            margin-right: auto;
        }
        th, td {
            border: 1px solid black;
            padding: 8px;
            text-align: center;
        }
        th {
            background-color: #ff4081;
            color: white;
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

    <h2>Winners List</h2>
    <table id="winnersTable">
        <tr>
            <th>Name</th>
            <th>Phone</th>
            <th>Prize</th>
        </tr>
    </table>
</body>
</html>
"""

# Embed Spin Wheel
components.html(html_code, height=600)
