import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import random
import time

# Define wheel segments
segments = ["Prize 1", "Prize 2", "Prize 3", "Prize 4", "Prize 5", "Prize 6", "Prize 7", "Prize 8"]
colors = ["#FF5733", "#33FF57", "#3357FF", "#F39C12", "#8E44AD", "#E74C3C", "#2ECC71", "#3498DB"]
num_segments = len(segments)

def draw_wheel(angle=0):
    fig, ax = plt.subplots(figsize=(5, 5), subplot_kw={'aspect': 'equal'})
    wedges, _ = ax.pie([1]*num_segments, colors=colors, startangle=angle, counterclock=False)
    
    # Add text labels
    for i, wedge in enumerate(wedges):
        ang = (wedge.theta2 + wedge.theta1) / 2
        x = 0.7 * np.cos(np.radians(ang))
        y = 0.7 * np.sin(np.radians(ang))
        ax.text(x, y, segments[i], ha='center', va='center', fontsize=10, color='white', fontweight='bold')
    
    ax.add_patch(plt.Circle((0, 0), 0.1, color='black'))  # Center circle
    return fig

def spin_wheel():
    total_rotation = random.randint(5, 10) * 360 + random.randint(0, 360)
    steps = 50
    angle_step = total_rotation / steps
    current_angle = 0
    wheel_placeholder = st.empty()
    
    for _ in range(steps):
        current_angle += angle_step
        with wheel_placeholder:
            st.pyplot(draw_wheel(current_angle))
        time.sleep(0.05)
    
    # Determine the winning segment
    final_angle = current_angle % 360
    winning_index = int(final_angle // (360 / num_segments))
    st.success(f"🎉 Congratulations! You won {segments[winning_index]}!")

# Streamlit UI
st.title("🎡 Advanced Spin Wheel Game")
st.pyplot(draw_wheel())
if st.button("Spin the Wheel! 🎰"):
    spin_wheel()
