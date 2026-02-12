"""
Custom CSS theme for the Corrosion Rate Prediction app.
Provides a modern, polished look with gradient accents, card-based layouts,
and smooth animations.
"""

CUSTOM_CSS = """
<style>
/* ── Google Font ── */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

/* ── Global ── */
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* ── Hero Header ── */
.hero-title {
    text-align: center;
    font-size: 2.4rem;
    font-weight: 700;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 0.2rem;
    line-height: 1.3;
}
.hero-subtitle {
    text-align: center;
    font-size: 1.05rem;
    color: #8892a4;
    margin-bottom: 2rem;
    font-weight: 400;
}

/* ── Card containers ── */
.card {
    background: linear-gradient(145deg, rgba(30,34,47,0.6), rgba(22,25,35,0.8));
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 16px;
    padding: 1.8rem;
    margin-bottom: 1.2rem;
    backdrop-filter: blur(10px);
}
.card-header {
    font-size: 0.85rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 1.2px;
    color: #667eea;
    margin-bottom: 1rem;
}

/* ── Prediction Result Badge ── */
.result-badge {
    text-align: center;
    padding: 1.6rem 1.2rem;
    border-radius: 16px;
    background: linear-gradient(135deg, rgba(102,126,234,0.15), rgba(118,75,162,0.15));
    border: 1px solid rgba(102,126,234,0.3);
    margin: 1rem 0 1.5rem 0;
}
.result-badge .label {
    font-size: 0.85rem;
    color: #8892a4;
    text-transform: uppercase;
    letter-spacing: 1px;
    font-weight: 600;
    margin-bottom: 0.4rem;
}
.result-badge .value {
    font-size: 1.8rem;
    font-weight: 700;
    background: linear-gradient(135deg, #667eea, #764ba2);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

/* ── Input Summary Chips ── */
.chip-row {
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
    margin: 0.8rem 0;
}
.chip {
    display: inline-flex;
    align-items: center;
    gap: 0.35rem;
    background: rgba(102,126,234,0.1);
    border: 1px solid rgba(102,126,234,0.2);
    border-radius: 20px;
    padding: 0.35rem 0.85rem;
    font-size: 0.82rem;
    color: #c0c8dc;
    font-weight: 500;
}
.chip .chip-label {
    color: #667eea;
    font-weight: 600;
}

/* ── Recommendation Box ── */
.rec-box {
    background: linear-gradient(145deg, rgba(30,34,47,0.5), rgba(22,25,35,0.7));
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 14px;
    padding: 1.5rem 1.8rem;
    margin: 1rem 0;
    line-height: 1.7;
    color: #d0d5e0;
}
.rec-box ul {
    margin-left: 0.5rem;
}

/* ── Section dividers ── */
.section-divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(102,126,234,0.3), transparent);
    margin: 2rem 0;
    border: none;
}

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #141722 0%, #1a1e2e 100%);
}
section[data-testid="stSidebar"] .stMarkdown h2 {
    background: linear-gradient(135deg, #667eea, #764ba2);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    font-size: 1.3rem;
}

/* ── Sidebar Badges ── */
.sidebar-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.3rem;
    background: rgba(102,126,234,0.12);
    border: 1px solid rgba(102,126,234,0.2);
    border-radius: 8px;
    padding: 0.3rem 0.6rem;
    font-size: 0.75rem;
    color: #8892a4;
    font-weight: 500;
    margin-right: 0.3rem;
    margin-bottom: 0.3rem;
}

/* ── Form Styling ── */
[data-testid="stForm"] {
    border: 1px solid rgba(255,255,255,0.06) !important;
    border-radius: 16px !important;
    padding: 1.5rem !important;
    background: linear-gradient(145deg, rgba(30,34,47,0.4), rgba(22,25,35,0.6)) !important;
}

/* ── Submit Button ── */
[data-testid="stFormSubmitButton"] button {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 0.6rem 2rem !important;
    font-weight: 600 !important;
    font-size: 0.95rem !important;
    letter-spacing: 0.3px;
    transition: all 0.3s ease !important;
    width: 100% !important;
}
[data-testid="stFormSubmitButton"] button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 20px rgba(102,126,234,0.35) !important;
}

/* ── Download Buttons ── */
[data-testid="stDownloadButton"] button {
    background: rgba(102,126,234,0.1) !important;
    border: 1px solid rgba(102,126,234,0.25) !important;
    border-radius: 10px !important;
    color: #667eea !important;
    font-weight: 500 !important;
    transition: all 0.3s ease !important;
}
[data-testid="stDownloadButton"] button:hover {
    background: rgba(102,126,234,0.2) !important;
    border-color: rgba(102,126,234,0.5) !important;
}

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
    gap: 0.5rem;
}
.stTabs [data-baseweb="tab"] {
    border-radius: 10px;
    padding: 0.5rem 1.2rem;
    font-weight: 500;
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, rgba(102,126,234,0.2), rgba(118,75,162,0.2)) !important;
}

/* ── Footer ── */
.footer {
    text-align: center;
    padding: 1.5rem 0 0.5rem 0;
    color: #4a5068;
    font-size: 0.8rem;
    border-top: 1px solid rgba(255,255,255,0.04);
    margin-top: 3rem;
}
.footer a {
    color: #667eea;
    text-decoration: none;
}

/* ── Spinner ── */
.stSpinner > div {
    border-top-color: #667eea !important;
}
</style>
"""
