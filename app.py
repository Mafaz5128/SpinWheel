import streamlit as st
import numpy as np
import plotly.graph_objects as go
import time
import random

# List of prizes
prizes = ["10% Off", "Free Lipstick", "20% Off", "Buy 1 Get 1", "Free Shipping", "Gift Hamper"]
colors = ["#FF0000", "#FF69B4", "#FFD700", "#32CD32", "#1E90FF", "#8A2BE2"]  # Valentine theme colors

# Function to draw the spinning wheel
def draw_wheel(rotation_angle=0):
    fig = go.Figure()
    
    num_slices = len(prizes)
    angles = np.linspace(0, 360, num_slices + 1)
    
    for i in range(num_slices):
        fig.add_shape(
            type="path",
            path=f"M 0 0 L {np.cos(np.radians(angles[i]))} {np.sin(np.radians(angles[i]))} A 1 1 0 0 1 {np.cos(np.radians(angles[i+1]))} {np.sin(np.radians(angles[i+1]))} Z",
            fillcolor=colors[i],
            line=dict(width=2, color='black')
        )
        fig.add_annotation(
            x=0.7 * np.cos(np.radians((angles[i] + angles[i + 1]) / 2)),
            y=0.7 * np.sin(np.radians((angles[i] + angles[i + 1]) / 2)),
            text=prizes[i],
            showarrow=False,
            font=dict(size=16, color='white')
        )
    
    fig.add_shape(type="line", x0=0, y0=1.1, x1=0, y1=1.2, line=dict(color="red", width=4))  # Arrow
    
    fig.update_layout(
        showlegend=False,
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
        width=500,
        height=500,
        plot_bgcolor='white',
        shapes=[]
    )
    
    return fig

# Streamlit UI
st.title("💖 Valentine's Day Spin & Win! 💖")
st.markdown("🎡 Spin the wheel and win exciting prizes! 🎁")

# Wheel display
wheel_chart = st.plotly_chart(draw_wheel(), use_container_width=False)

# Spin button
if st.button("🎡 Spin the Wheel!"):
    winning_index = random.randint(0, len(prizes) - 1)
    final_angle = 360 - (winning_index * (360 / len(prizes)))
    
    for angle in np.linspace(0, final_angle + 1440, 100):  # Smooth spinning effect
        wheel_chart.plotly_chart(draw_wheel(rotation_angle=angle), use_container_width=False)
        time.sleep(0.15)
    
    st.success(f"🎉 Congratulations! You won: {prizes[winning_index]} 🎁")

# Collect user details
user_name = st.text_input("Enter your name (Optional)")
user_email = st.text_input("Enter your email to receive the prize (Optional)")
if st.button("Submit Details"):
    st.write("Your prize will be sent to your email soon! 💌")
