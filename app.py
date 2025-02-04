import streamlit as st
import random
import numpy as np
import plotly.graph_objects as go

# List of prizes
prizes = ["10% Off", "Free Lipstick", "20% Off", "Buy 1 Get 1", "Free Shipping", "Gift Hamper"]
colors = ["#FF9999", "#66B3FF", "#99FF99", "#FFCC99", "#FFD700", "#FF69B4"]  # Different colors for sections

# Function to create the spin wheel
def draw_wheel(selected_prize=None):
    fig = go.Figure()

    # Angles for each prize
    angles = np.linspace(0, 360, len(prizes) + 1)
    
    # Create pie chart for wheel
    fig.add_trace(go.Pie(
        labels=prizes,
        values=[1] * len(prizes),  # Equal distribution
        textinfo="label",
        marker=dict(colors=colors, line=dict(color="black", width=1)),
        hole=0.3
    ))

    # Highlight selected prize
    if selected_prize:
        index = prizes.index(selected_prize)
        rotation_angle = angles[index]  # Angle to rotate to selected prize
        fig.update_layout(annotations=[
            dict(text=f"🎉 {selected_prize} 🎁", x=0.5, y=0.5, font_size=20, showarrow=False)
        ])
    else:
        rotation_angle = 0

    # Rotate wheel
    fig.update_layout(
        showlegend=False,
        margin=dict(l=10, r=10, t=10, b=10),
        height=400,
        width=400
    )

    return fig

# Streamlit UI
st.title("💖 Valentine's Day Spin & Win! 💖")

# Draw the initial wheel
selected_prize = None
chart = draw_wheel()
wheel_chart = st.plotly_chart(chart)

# Spin button
if st.button("🎡 Spin the Wheel!"):
    selected_prize = random.choice(prizes)
    updated_chart = draw_wheel(selected_prize)
    wheel_chart = st.plotly_chart(updated_chart)  # Update the chart
    st.success(f"🎉 Congratulations! You won: {selected_prize} 🎁")

# Collect user details
user_name = st.text_input("Enter your name (Optional)")
user_email = st.text_input("Enter your email to receive the prize (Optional)")

if st.button("Submit Details"):
    if user_email:
        st.write("Your prize will be sent to your email soon! 💌")
    else:
        st.warning("Please enter a valid email to receive the prize.")
