import streamlit as st
import streamlit.components.v1 as components
import pandas as pd

# Set page title
st.set_page_config(page_title="Valentine Spin Wheel", layout="wide")

# Initialize session state
if "results" not in st.session_state:
    st.session_state["results"] = []

# Display header
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

# JavaScript + HTML for Spin Wheel
html_code = """
<!DOCTYPE html>
<html>
<head>
    <script>
        function sendPrizeToStreamlit(name, phone, prize) {
            const message = { name: name, phone: phone, prize: prize };
            fetch('/_st_prize', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(message)
            }).then(response => response.json()).then(data => {
                console.log("Sent to Streamlit:", data);
            });
        }

        function spinWheel() {
            const prizes = ["Get 20% Off", "Mystery Box", "Buy 1 Get 1", "Thank You", "Lipstick", "Voucher"];
            const selectedPrize = prizes[Math.floor(Math.random() * prizes.length)];
            
            document.getElementById("result").innerText = `🎉 You won: ${selectedPrize}`;
            
            sendPrizeToStreamlit('""" + st.session_state.get("player_name", "Unknown") + """', 
                                 '""" + st.session_state.get("player_phone", "Unknown") + """', 
                                 selectedPrize);
        }
    </script>
    <style>
        body { text-align: center; font-family: Arial, sans-serif; }
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
    <button onclick="spinWheel()">🎰 Spin the Wheel</button>
    <p id="result"></p>
</body>
</html>
"""

# Embed the spin wheel
components.html(html_code, height=300)

# Function to capture data from JavaScript
def capture_prize():
    import json
    from streamlit.web.server.websocket_headers import get_websocket_headers
    
    headers = get_websocket_headers()
    data = json.loads(headers.get("st-prize", "{}"))
    
    if data:
        st.session_state["results"].append(data)

# Store prize results
capture_prize()

# Display Spin Results
st.markdown("## 🎉 Spin Results")
df = pd.DataFrame(st.session_state["results"], columns=["Name", "Phone", "Prize"])
st.dataframe(df)
