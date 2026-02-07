import json
from openai import OpenAI
import streamlit as st

@st.cache_data
def load_json(path: str):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def build_prompt(language: str, scenario_title: str, grounding_text: str) -> str:
    return f"""
You are a safety-focused assistant helping users understand their rights in immigration-related scenarios.
This is EDUCATIONAL information, NOT legal advice.
Do NOT ask for personal info. Do NOT ask about immigration status.
Be calm, clear, and actionable. Avoid legal jargon.

User language: {language}
Scenario: {scenario_title}

Use ONLY the following grounding text as the source of truth:
\"\"\"{grounding_text}\"\"\"

Return ONLY valid JSON in this exact schema:

{{
  "rights_bullets": ["... (max 5)"],
  "do": ["... (6-10)"],
  "dont": ["... (6-10)"],
  "scripts": {{
    "calm": "... (1-3 sentences)",
    "assert": "... (1-3 sentences)"
  }},
  "disclaimer": "Educational info, not legal advice."
}}
""".strip()

def generate_snapshot(language: str, scenario_title: str, grounding_text: str) -> dict:
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
    prompt = build_prompt(language, scenario_title, grounding_text)

    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Return only JSON. No extra text."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.2,
    )

    content = resp.choices[0].message.content.strip()
    return json.loads(content)


ZIP_HOTLINES = {
    # MVP examples (replace with real numbers your team approves)
    "90001": {"label": "Local help line", "number": "1-800-555-0101"},
    "10001": {"label": "Local help line", "number": "1-800-555-0102"},
    "60601": {"label": "Local help line", "number": "1-800-555-0103"},
}

DEFAULT_HOTLINE = {"label": "National help line", "number": "1-800-555-0199"}  # replace with real

# Page configuration
st.set_page_config(layout="centered")

# Styling
st.markdown(
    """
    <style>
    /* Force a clean white page + dark readable text everywhere */
    .stApp {
        background: white !important;
        color: #111 !important;
    }

    /* Streamlit containers */
    section[data-testid="stSidebar"], 
    section.main, 
    div[data-testid="stAppViewContainer"],
    div[data-testid="stHeader"],
    div[data-testid="stToolbar"] {
        background: white !important;
        color: #111 !important;
    }

    /* Make ALL text readable */
    h1, h2, h3, h4, h5, h6, p, span, div, label, li {
        color: #111 !important;
    }

    /* Your title style */
    h1 {
        font-family: Impact, Charcoal, sans-serif;
        text-align: center;
        font-size: 60px;
        margin-bottom: 0px;
    }

    /* Buttons */
    .stButton > button {
        width: 100%;
        border-radius: 6px;
        height: 3em;
        border: 1px solid #d3d3d3;
        background: #f7f7f7 !important;
        color: #111 !important;
        font-weight: 600;
    }

    .stButton > button:hover {
        background: #efefef !important;
    }

    /* Inputs (if you add any later) */
    input, textarea {
        color: #111 !important;
        background: #fff !important;
    }

    /* Make alert text readable */
    div[data-testid="stAlert"] * {
        color: #111 !important;
    }
    /* Link buttons (st.link_button) */

    div[data-testid="stLinkButton"] a {
        width: 100% !important;
        display: block !important;
        text-align: center !important;
        border-radius: 6px !important;
        padding: 0.6em 1em !important;

        background: #f7f7f7 !important;  /* light background */
        color: #111 !important;         /* dark readable text */
        border: 1px solid #d3d3d3 !important;

        font-weight: 600 !important;
        text-decoration: none !important;
    }

    div[data-testid="stLinkButton"] a:hover {
        background: #efefef !important;
        color: #111 !important;
    }
    /* Hotline: use a dedicated class so it overrides global text color */
    .hotline {
        text-align: center !important;
        color: #d60000 !important;
        font-weight: 900 !important;
        font-size: 22px !important;
        margin: 6px 0 22px 0 !important;
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

# --- Hotline + ZIP lookup (privacy-first: user enters ZIP, nothing stored) ---
if "zip_code" not in st.session_state:
    st.session_state.zip_code = ""

hotline_cols = st.columns([0.9, 2, 1.1])
with hotline_cols[1]:
    # ZIP input
    st.session_state.zip_code = st.text_input(
        "Enter ZIP code (optional)",
        value=st.session_state.zip_code,
        max_chars=10,
        placeholder="e.g., 90210",
        label_visibility="collapsed"
    )

    zip_clean = st.session_state.zip_code.strip()

    is_local = zip_clean in ZIP_HOTLINES
    hotline = ZIP_HOTLINES.get(zip_clean, DEFAULT_HOTLINE)

    # Clear, explicit headline for what this is
    st.markdown(
        "<div class='hotline'>HOTLINE LOOKUP</div>",
        unsafe_allow_html=True
    )

    # Clear result text (local vs national)
    if zip_clean and not is_local:
        st.markdown(
            f"<div style='text-align:center; font-weight:700; margin-top:4px;'>"
            f"No local hotline found for <b>{zip_clean}</b> yet.</div>",
            unsafe_allow_html=True
        )

    st.markdown(
        f"<div class='hotline'>{'Local' if is_local else 'National'} hotline: {hotline['number']}</div>",
        unsafe_allow_html=True
    )

    # Helpful fallback
    if zip_clean and not is_local:
        st.caption("Use the directory link below to find local legal help by ZIP.")
        st.link_button(
            "Find local legal aid directory",
            f"https://www.immigrationadvocates.org/nonprofit/legaldirectory/?zip={zip_clean}"
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

scenarios = load_json("data/scenarios.json")
resources = load_json("data/resources.json")["resources"]


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
            scenario_keys = list(scenarios.keys())
            scenario_key = scenario_keys[i]
            scenario = scenarios[scenario_key]

            if st.session_state.language == "English":
                scenario_title = scenario["title_en"]
                grounding = scenario["grounding_en"]
                lang = "English"
            else:
                scenario_title = scenario["title_es"]
                grounding = scenario["grounding_es"]
                lang = "Español"

            try:
                with st.spinner("Generating your Rights Snapshot..."):
                    result = generate_snapshot(lang, scenario_title, grounding)

                st.session_state["result"] = result
                st.session_state["resources"] = resources
                st.session_state["scenario_title"] = scenario_title

            except Exception as e:
                st.error(f"OpenAI error: {e}")
                st.session_state["result"] = None



st.markdown("---")

if "result" in st.session_state and st.session_state["result"]:
    r = st.session_state["result"]

    st.subheader(st.session_state.get("scenario_title", "Your Rights Snapshot"))

    st.markdown("### Your Rights")
    for b in r.get("rights_bullets", []):
        st.write(f"• {b}")

    st.markdown("### Do")
    for d in r.get("do", []):
        st.write(f"✅ {d}")

    st.markdown("### Don’t")
    for d in r.get("dont", []):
        st.write(f"❌ {d}")

    st.markdown("### What to Say")
    st.markdown("**Calm script:**")
    st.write(r.get("scripts", {}).get("calm", ""))

    st.markdown("**Assert your rights:**")
    st.write(r.get("scripts", {}).get("assert", ""))

    st.markdown("### Resources")
    for res in st.session_state.get("resources", []):
        name = res["name_en"] if st.session_state.language == "English" else res["name_es"]
        st.link_button(name, res["url"])

    st.caption(r.get("disclaimer", "Educational info, not legal advice."))
