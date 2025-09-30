import streamlit as st
import random
import requests
from PIL import Image
from io import BytesIO

# Mnemonica stack
MNEMONICA = [
    "4C","2H","7D","3C","4H","6D","AS","5H","9S","2S","QH","3D","QC",
    "8H","6S","5S","9H","KC","2D","JH","3S","8S","6H","10C","5D","KD",
    "2C","3H","8D","5C","KS","JD","8C","10S","KH","JC","7S","10H","AD",
    "4S","7H","4D","AC","9C","JS","QD","7C","QS","10D","6C","AH","9D"
]

CARD_URL = "https://deckofcardsapi.com/static/img/{code}.png"

# Cache each card individually for reliability
@st.cache_data(show_spinner=False)
def load_card(code):
    url = CARD_URL.format(code=code)
    try:
        resp = requests.get(url, timeout=5)
        resp.raise_for_status()  # Raise error if not 200
        img = Image.open(BytesIO(resp.content))
        return img
    except Exception as e:
        # If a card fails, return a blank placeholder
        st.warning(f"Failed to load card {code}, showing placeholder")
        return Image.new("RGB", (180, 260), color=(50,50,50))

st.set_page_config(page_title="ACAAN Helper", layout="centered")
st.title("ACAAN Helper")

# Session state
if 'current_card' not in st.session_state:
    st.session_state.current_card = random.choice(MNEMONICA)
if 'current_number' not in st.session_state:
    st.session_state.current_number = random.randint(1, 52)

# Display
col1, col2 = st.columns([2,1])
with col1:
    st.image(load_card(st.session_state.current_card), width=180)
with col2:
    st.markdown(f"### Position: {st.session_state.current_number}")
    if MNEMONICA.index(st.session_state.current_card)+1 == st.session_state.current_number:
        st.markdown("<div style='width:6px;height:6px;background:white;border-radius:50%;'></div>", unsafe_allow_html=True)

# Buttons
col3, col4 = st.columns(2)
with col3:
    if st.button("Change Card"):
        new_card = random.choice(MNEMONICA)
        attempts = 0
        while new_card == st.session_state.current_card and attempts < 6:
            new_card = random.choice(MNEMONICA)
            attempts +=1
        st.session_state.current_card = new_card
with col4:
    if st.button("Change Number"):
        st.session_state.current_number = random.randint(1,52)
