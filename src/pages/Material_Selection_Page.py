import streamlit as st
from chat.chat import invoke_llm
from utils.vars import environment
from config.config import PIPE_ICON, MATERIAL_SELECTION_IMAGE, SIDEBAR_IMAGE
from config.theme import CUSTOM_CSS
from utils.processors import remove_think_tags

st.set_page_config(
    page_title="Material Selector",
    layout="wide",
    page_icon=PIPE_ICON,
    initial_sidebar_state="expanded",
)
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# ═══════════════════ Sidebar ═══════════════════
with st.sidebar:
    st.image(MATERIAL_SELECTION_IMAGE, use_container_width=True)
    st.markdown("## 🏗️ Material Selector")
    st.caption(
        "Get AI-powered material suggestions based on your corrosion environment "
        "and operating conditions."
    )
    st.markdown(
        '<div style="margin-top:0.8rem;">'
        '<span class="sidebar-badge">💡 LLM-Powered</span>'
        '<span class="sidebar-badge">🔎 Smart Selection</span>'
        "</div>",
        unsafe_allow_html=True,
    )
    st.markdown("---")
    st.markdown(
        "**How it works:**\n"
        "1. Describe the operating environment\n"
        "2. Set design constraints\n"
        "3. Get top material recommendations"
    )

# ═══════════════════ Hero Header ═══════════════════
st.markdown(
    '<div class="hero-title">AI-Powered Material Selector</div>',
    unsafe_allow_html=True,
)
st.markdown(
    '<div class="hero-subtitle">'
    "Describe your corrosion environment and constraints — "
    "the AI will recommend optimal materials with rationale."
    "</div>",
    unsafe_allow_html=True,
)

# ═══════════════════ Input Form ═══════════════════
with st.form("llm_material_selector"):
    # ── Section 1: Environment ──
    st.markdown(
        '<div class="card-header">🏭 Environment & Operating Conditions</div>',
        unsafe_allow_html=True,
    )
    c1, c2, c3 = st.columns(3)

    with c1:
        env = st.selectbox(
            "Environment Type",
            options=environment,
            help="e.g., seawater, acidic, alkaline",
        )
        pH = st.number_input("pH Level", min_value=0.0, max_value=14.0, value=7.0)

    with c2:
        temperature = st.number_input("Operating Temperature (°C)", value=25)
        pressure = st.number_input("Operating Pressure (bar)", value=1.0)

    with c3:
        chloride = st.selectbox(
            "Chloride Presence", ["None", "Low", "Moderate", "High"]
        )
        flow = st.selectbox(
            "Flow Condition",
            ["Static", "Low velocity", "High velocity", "Turbulent"],
        )

    # ── Section 2: Design Constraints ──
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="card-header">🔧 Design & Budget Constraints</div>',
        unsafe_allow_html=True,
    )
    d1, d2, d3 = st.columns(3)

    with d1:
        contact = st.selectbox("Galvanic Contact?", ["No", "Yes"])

    with d2:
        design_life = st.number_input("Required Design Life (Years)", value=10, min_value=1)
        maintenance = st.selectbox("Maintenance Frequency", ["Low", "Moderate", "High"])

    with d3:
        budget = st.selectbox("Budget Constraint", ["None", "Low", "Medium", "High"])

    # ── Section 3: Notes ──
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="card-header">📋 Additional Context</div>',
        unsafe_allow_html=True,
    )
    custom_notes = st.text_area(
        "Additional notes (optional)",
        height=90,
        placeholder="Any extra details about the environment, design requirements, "
        "prior failures, or preferred alloy families...",
        label_visibility="collapsed",
    )

    submitted = st.form_submit_button(
        "⚡  Suggest Materials", use_container_width=True
    )

# ═══════════════════ LLM Processing ═══════════════════
if submitted:
    user_prompt = f"""
You are a corrosion engineering assistant helping select optimal materials for corrosion resistance in industrial settings.

Based on the following operating and environmental conditions, recommend the **top 2–3 materials**:

- Environment: {env}
- pH Level: {pH}
- Chloride Presence: {chloride}
- Temperature: {temperature}°C
- Pressure: {pressure} bar
- Flow Condition: {flow}
- Galvanic Contact: {contact}
- Required Design Life: {design_life} years
- Maintenance Requirements: {maintenance}
- Budget Constraints: {budget}
- Additional Notes: {custom_notes}

Please provide your output in the following format:

1. **Material Name (UNS Code)**
   - ✅ *Why it is suitable* (highlight corrosion resistance, mechanical properties, compatibility, etc.)
   - ⚠️ *Limitations* or special handling considerations
   - Suggestions: Suggested surface treatments or enhancements (if needed)

Conclude with:
- 🎯 A final recommendation if one material clearly stands out for the given case.
- 🧠 Reminders or caveats (e.g., importance of site-specific testing, monitoring methods, etc.)

Use a **professional and concise tone**. Structure your response clearly with bullet points or short paragraphs to enhance readability for engineers in the field.
"""

    with st.spinner("💭 Generating material recommendations..."):
        response = remove_think_tags(invoke_llm(user_prompt))

    st.session_state.material_response = response
    st.session_state.material_inputs = {
        "Environment": env,
        "pH Level": pH,
        "Chloride": chloride,
        "Temperature": f"{temperature}°C",
        "Pressure": f"{pressure} bar",
        "Flow": flow,
        "Galvanic Contact": contact,
        "Design Life": f"{design_life} yrs",
        "Maintenance": maintenance,
        "Budget": budget,
        "Notes": custom_notes,
    }

# ═══════════════════ Results Display ═══════════════════
if "material_response" in st.session_state:
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

    # ── Input summary chips ──
    inputs = st.session_state.material_inputs
    chips = "".join(
        f'<span class="chip"><span class="chip-label">{k}:</span> {v}</span>'
        for k, v in inputs.items()
        if v and k != "Notes"
    )
    st.markdown(f'<div class="chip-row">{chips}</div>', unsafe_allow_html=True)

    # ── Tabbed results ──
    tab_rec, tab_export = st.tabs(["🔬 Material Recommendations", "📦 Export"])

    with tab_rec:
        st.markdown(
            f'<div class="rec-box">{st.session_state.material_response}</div>',
            unsafe_allow_html=True,
        )

    with tab_export:
        txt_content = "Material Selection Report\n" + "=" * 40 + "\n\n"
        txt_content += "Input Parameters:\n"
        for k, v in inputs.items():
            txt_content += f"  • {k}: {v}\n"
        txt_content += "\nAI Recommendations:\n" + "-" * 40 + "\n"
        txt_content += st.session_state.material_response

        st.download_button(
            label="📝  Download Report as TXT",
            data=txt_content.encode("utf-8"),
            file_name="material_recommendations.txt",
            mime="text/plain",
            use_container_width=True,
            key="download_material_txt",
        )

# ═══════════════════ Footer ═══════════════════
st.markdown(
    '<div class="footer">'
    "Built with Streamlit · AI Material Selector · LLM-Powered"
    "</div>",
    unsafe_allow_html=True,
)
