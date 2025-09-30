import streamlit as st
import random

# Mnemonica stack
MNEMONICA = [
    "4C","2H","7D","3C","4H","6D","AS","5H","9S","2S","QH","3D","QC",
    "8H","6S","5S","9H","KC","2D","JH","3S","8S","6H","10C","5D","KD",
    "2C","3H","8D","5C","KS","JD","8C","10S","KH","JC","7S","10H","AD",
    "4S","7H","4D","AC","9C","JS","QD","7C","QS","10D","6C","AH","9D"
]

# Map suits to symbols
SUIT_SYMBOLS = {"C":"♣","D":"♦","H":"♡","S":"♠"}

st.set_page_config(page_title="ACAAN Helper", layout="centered")

# Session state for card, number, and modes
if 'current_card' not in st.session_state:
    st.session_state.current_card = random.choice(MNEMONICA)
if 'current_number' not in st.session_state:
    st.session_state.current_number = random.randint(1,52)
if 'change_card_mode' not in st.session_state:
    st.session_state.change_card_mode = 'random'
if 'change_number_mode' not in st.session_state:
    st.session_state.change_number_mode = 'random'

st.title("ACAAN Helper")

# Function to render the card
def render_card(code):
    rank = code[:-1]
    suit = SUIT_SYMBOLS[code[-1]]
    color = "red" if suit in ["♡","♦"] else "black"

    # Magician-only subtle signal
    if MNEMONICA.index(st.session_state.current_card)+1 == st.session_state.current_number:
        border_color = "#a0ffa0"  # very subtle green border for magician
        shadow = "0 0 5px rgba(0,255,0,0.2)"
    else:
        border_color = "#333"
        shadow = "3px 3px 8px rgba(0,0,0,0.4)"

    card_html = f"""
    <div style="
        width:120px;
        height:180px;
        border-radius:12px;
        border:2px solid {border_color};
        background-color:white;
        color:{color};
        display:flex;
        flex-direction:column;
        justify-content:space-between;
        padding:10px;
        font-family:sans-serif;
        box-shadow:{shadow};
    ">
        <div style="font-size:24px;">{rank}{suit}</div>
        <div style="font-size:48px; display:flex; justify-content:center; align-items:center;">{suit}</div>
        <div style="font-size:24px; transform:rotate(180deg);">{rank}{suit}</div>
    </div>
    """
    st.markdown(card_html, unsafe_allow_html=True)

# Display card and number
col1, col2 = st.columns([2,1])
with col1:
    render_card(st.session_state.current_card)
with col2:
    st.markdown(f"### Position: {st.session_state.current_number}")

# Buttons with magic trick logic
col3, col4 = st.columns(2)
with col3:
    if st.button("Change Card"):
        if st.session_state.change_card_mode == 'random':
            new_card = random.choice(MNEMONICA)
            attempts = 0
            while new_card == st.session_state.current_card and attempts < 6:
                new_card = random.choice(MNEMONICA)
                attempts += 1
            st.session_state.current_card = new_card
            st.session_state.change_number_mode = 'force'
        else:
            st.session_state.current_card = MNEMONICA[st.session_state.current_number - 1]
            st.session_state.change_number_mode = 'random'
        st.session_state.change_card_mode = 'random'

with col4:
    if st.button("Change Number"):
        if st.session_state.change_number_mode == 'random':
            st.session_state.current_number = random.randint(1,52)
            st.session_state.change_card_mode = 'force'
        else:
            st.session_state.current_number = MNEMONICA.index(st.session_state.current_card) + 1
            st.session_state.change_card_mode = 'random'
        st.session_state.change_number_mode = 'random'
