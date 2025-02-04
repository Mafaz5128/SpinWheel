import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import time
import random
from io import BytesIO

# Define the prizes
prizes = ["Free Lipstick", "10% Off", "Free Eyeliner", "$5 Coupon", "Mystery Gift", "20% Off", "Buy 1 Get 1", "Free Compact"]
colors = ['#FF5733', '#33FF57', '#3357FF', '#FF33A1', '#A133FF', '#FFD700', '#FF8C00', '#00CED1']

# Function to draw the wheel
def draw_wheel(angle=0):
    fig, ax = plt.subplots(figsize=(6,6), subplot_kw={'aspect': 'equal'})
    wedges, _ = ax.pie([1]*len(prizes), colors=colors, startangle=angle, counterclock=False, wedgeprops={'edgecolor': 'white'})
    
    for i, wedge in enumerate(wedges):
        theta = (wedge.theta2 + wedge.theta1) / 2
        x = 0.65 * np.cos(np.radians(theta))
        y = 0.65 * np.sin(np.radians(theta))
        ax.text(x, y, prizes[i], ha='center', va='center', fontsize=10, weight='bold', color='white')
    
    # Draw center spin button
    ax.add_patch(plt.Circle((0, 0), 0.15, color='black', zorder=10))
    ax.text(0, 0, "SPIN", ha='center', va='center', fontsize=12, color='white', weight='bold', zorder=11)
    
    # Draw arrow
    ax.annotate('', xy=(0, 1.05), xytext=(0, 0.75), arrowprops=dict(facecolor='red', edgecolor='black', linewidth=2, headwidth=15, headlength=20))
    
    buf = BytesIO()
    plt.savefig(buf, format='png', transparent=True)
    plt.close(fig)
    return buf

# Streamlit UI
st.title("🎡 Spin & Win!")
st.write("Click the center button to spin the wheel and win a prize!")

# Display the initial wheel
angle = 0
wheel_image = draw_wheel(angle)
st.image(wheel_image, use_container_width=True)

# Spin Button
if st.button("Spin Now!"):
    with st.spinner("Spinning..."):
        spins = random.randint(5, 10)  # Number of rotations
        final_angle = random.randint(0, 360) + (spins * 360)
        steps = 30
        for i in range(steps):
            angle = (final_angle / steps) * (i+1)
            wheel_image = draw_wheel(angle)
            st.image(wheel_image, use_container_width=True)
            time.sleep(0.05)
        
        # Determine the prize
        winning_index = int(((360 - (final_angle % 360)) / 45) % len(prizes))
        st.success(f"🎉 Congratulations! You won {prizes[winning_index]}! 🎁")
