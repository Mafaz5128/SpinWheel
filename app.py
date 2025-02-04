import streamlit as st
import random
import numpy as np
import matplotlib.pyplot as plt
import time

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

# Function to create a spinning wheel using Matplotlib
def draw_wheel(rotation_angle=0):
    fig, ax = plt.subplots(figsize=(5, 5), subplot_kw=dict(aspect="equal"))
    wedges, _ = ax.pie([1] * len(prizes), labels=prizes, colors=colors, startangle=rotation_angle)

    # Add arrow
    ax.annotate('▼', xy=(0, 0.8), xytext=(0, 1.2),
                arrowprops=dict(facecolor='red', shrink=0.05),
                ha='center', fontsize=20, color='black')

    return fig

# UI
st.title("💖 Valentine's Day Spin & Win! 💖")
st.markdown("🎁 Spin the wheel and win exciting prizes! Spread the love this Valentine's Day! 💕")

rotation_angle = 0
wheel_chart = st.empty()  # Placeholder for updating chart
fig = draw_wheel(rotation_angle)
wheel_chart.pyplot(fig)  # ✅ Fix: Use `pyplot()` instead of `plotly_chart()`

if st.button("🎡 Spin the Wheel!"):
    with st.spinner("Spinning... 🎠"):
        total_time = 15  
        steps = 50  
        for i in range(steps):
            rotation_angle += random.randint(15, 30)  
            rotation_angle %= 360  
            fig = draw_wheel(rotation_angle=rotation_angle)
            wheel_chart.pyplot(fig, clear=True)  # ✅ Fix: No duplicate error with `pyplot()`
            time.sleep(total_time / steps)

    sector_size = 360 / len(prizes)
    winning_index = int((rotation_angle % 360) / sector_size)
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
        st.warning("⚠️ Please enter a valid email to receive the prize.")
