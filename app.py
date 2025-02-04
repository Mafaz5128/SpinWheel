import streamlit as st
import random
import time

# Set the title for the app
st.title("Spin the Wheel! 🎉")

# Create a container for the wheel
st.markdown("""
    <div style="display: flex; justify-content: center;">
        <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/1/1d/Color_wheel_10.svg/500px-Color_wheel_10.svg.png" width="300" height="300">
    </div>
    """, unsafe_allow_html=True)

# Text below the wheel
st.subheader("Wheel of Fortune")

# Placeholder for result message
result_message = st.empty()

# Define spin values and color list
spin_values = [
    {"min_degree": 61, "max_degree": 90, "value": 100},
    {"min_degree": 31, "max_degree": 60, "value": 200},
    {"min_degree": 0, "max_degree": 30, "value": 300},
    {"min_degree": 331, "max_degree": 360, "value": 400},
    {"min_degree": 301, "max_degree": 330, "value": 500},
    {"min_degree": 271, "max_degree": 300, "value": 600},
    {"min_degree": 241, "max_degree": 270, "value": 700},
    {"min_degree": 211, "max_degree": 240, "value": 800},
    {"min_degree": 181, "max_degree": 210, "value": 900},
    {"min_degree": 151, "max_degree": 180, "value": 1000},
    {"min_degree": 121, "max_degree": 150, "value": 1100},
    {"min_degree": 91, "max_degree": 120, "value": 1200},
]

# Spin button
if st.button('Spin'):
    result_message.text("Best of Luck! 🍀")
    
    # Simulate a random degree
    random_degree = random.randint(0, 359)
    
    # Simulate wheel spin
    for i in range(15):
        time.sleep(0.1)  # Slow down the spin
        degree_offset = random.randint(0, 10)
        random_degree += degree_offset
        if random_degree >= 360:
            random_degree = random_degree - 360
    
    # Find the value corresponding to the spin degree
    for spin in spin_values:
        if spin["min_degree"] <= random_degree <= spin["max_degree"]:
            value = spin["value"]
            break
    
    result_message.text(f"Congratulations, You Have Won ${value} 🎉")
