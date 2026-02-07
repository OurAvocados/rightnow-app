import streamlit as st

# Page configuration
st.set_page_config(layout="centered")

# Styling
st.markdown(
    """
    <style>
    .stApp {
        background-color: white;
    }
    h1 {
        font-family: Impact, Charcoal, sans-serif;
        text-align: center;
        color: black;
        font-size: 60px;
        margin-bottom: 0px; 
    }
    .stButton > button {
        width: 100%;
        border-radius: 5px;
        height: 3em;
        border: 1px solid #d3d3d3;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Title 
st.markdown("<h1>RIGHTNOW</h1>", unsafe_allow_html=True)

# Initialize language state
if "language" not in st.session_state:
    st.session_state.language = "English"

# Initialize hotline number
hotline_cols = st.columns([0.9, 2, 1.1])
with hotline_cols[1]:
    st.markdown(
        "<p style='text-align: center; color: red; font-weight: bold; font-size: 20px; margin-bottom: 20px;'>HOTLINE NUMBER</p>", 
        unsafe_allow_html=True
    )

# Language Button(s)
lang_cols = st.columns([2.8, 1.5, 0.2, 1.5, 3.2])
with lang_cols[1]:
    if st.button("English", use_container_width=True):
        st.session_state.language = "English"
with lang_cols[3]:
    if st.button("Español", use_container_width=True):
        st.session_state.language = "Español"

# Language Selected Text 
text_cols = st.columns([0.9, 2, 1.1])
with text_cols[1]:
    st.markdown(
        f"<p style='text-align: center; color: gray; font-size: 14px; margin-top: -10px;'>Language selected: {st.session_state.language}</p>", 
        unsafe_allow_html=True
    )

# Separator Line 
st.markdown("---")

# Scenario Buttons 
buttons_text = {
    "English": ["ICE at my door", "Traffic stop", "Workplace questioning", "Public questioning by law enforcement"],
    "Español": ["ICE en mi puerta", "Parada de tráfico", "Interrogatorio en el trabajo", "Interrogatorio público por parte de la policía"]
}

scen_cols = st.columns([0.9, 2, 1.1])

with scen_cols[1]:
    for i, btn_text in enumerate(buttons_text[st.session_state.language]):
        if st.button(btn_text, key=f"scenario_{i}", use_container_width=True):
            # -----------------------------------------
            # TODO: 
            # This is where the team can:
            # 1) Call the OpenAI API with the selected scenario
            # 2) Retrieve the structured Rights / Do/Don't / Scripts
            # 3) Load any pre-written JSON/Markdown guidance for this scenario
            # 4) Display results (bullets, checklists, scripts) in the app
            # -----------------------------------------
            st.write(f"You clicked: {btn_text}")
