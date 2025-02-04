import streamlit as st
import random
import numpy as np
import plotly.graph_objects as go
import time

# Valentine Theme Colors
background_color = "#FFE6E6"  # Light pink background
button_color = "#FF4C4C"  # Red button
text_color = "#D63384"  # Dark pink text
prizes = ["10% Off", "Free Lipstick", "20% Off", "Buy 1 Get 1", "Free Shipping", "Gift Hamper"]
colors = ["#FF9999", "#FF6666", "#FF4C4C", "#FFB6C1", "#FF69B4", "#FF1493"]  # Stylish Valentine colors

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

# Function to create a stylish spin wheel
def draw_wheel(selected_prize=None, rotation_angle=0):
    fig = go.Figure()

    fig.add_trace(go.Pie(
        labels=prizes,
        values=[1] * len(prizes),
        textinfo="label",
        marker=dict(colors=colors, line=dict(color="black", width=1.5)),
        hole=0.2
    ))

    # Rotate the wheel dynamically
    fig.update_traces(rotation=rotation_angle)  # Corrected line for rotation

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

# Valentine's Day UI
st.title("💖 Valentine's Day Spin & Win! 💖")
st.markdown("🎁 Spin the wheel and win exciting prizes! Spread the love this Valentine's Day! 💕")

# Draw the initial wheel
rotation_angle = 0
selected_prize = None
chart = draw_wheel()
wheel_chart = st.plotly_chart(chart)

# Spin button with animation
if st.button("🎡 Spin the Wheel!"):
    with st.spinner("Spinning... 🎠"):
        for _ in range(30):  # Simulate spinning effect
            rotation_angle += random.randint(30, 60)
            rotation_angle %= 360  # Keep it within 360 degrees
            chart = draw_wheel(rotation_angle=rotation_angle)
            wheel_chart = st.plotly_chart(chart)
            time.sleep(0.1)  # Small delay to create animation effect

    # Final result
    selected_prize = random.choice(prizes)
    st.success(f"🎉 Congratulations! You won: {selected_prize} 🎁")
    final_chart = draw_wheel(selected_prize=selected_prize, rotation_angle=rotation_angle)
    wheel_chart = st.plotly_chart(final_chart)  # Update with final position

# Collect user details
st.subheader("💌 Claim Your Prize!")
user_name = st.text_input("Enter your name (Optional)")
user_email = st.text_input("Enter your email to receive the prize (Optional)")

if st.button("Submit Details"):
    if user_email:
        st.success("✅ Your prize will be sent to your email soon! 💌")
    else:
        st.warning("⚠️ Please enter a valid email to receive the prize.")
