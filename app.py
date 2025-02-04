import streamlit as st
import random

# List of prizes
prizes = ["10% Off", "Free Lipstick", "20% Off", "Buy 1 Get 1", "Free Shipping", "Gift Hamper"]

# Streamlit UI
st.title("💖 Valentine's Day Spin & Win! 💖")

# Spin button
if st.button("🎡 Spin the Wheel!"):
    result = random.choice(prizes)
    st.success(f"🎉 Congratulations! You won: {result} 🎁")

# (Optional) Collect user details
user_name = st.text_input("Enter your name (Optional)")
user_email = st.text_input("Enter your email to receive the prize (Optional)")
if st.button("Submit Details"):
    st.write("Your prize will be sent to your email soon! 💌")
