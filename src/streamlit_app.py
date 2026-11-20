"""UFO Cred — Mission Control. Dashboard-first, real inventory, honest ML placeholders."""
from __future__ import annotations

import base64
from pathlib import Path

import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from src.data_loader import DATA_DIR, load_files

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets"
VIOLET = "#b37af5"
TEAL = "#35d8cf"
SKY = "#86ceff"
BG = "#08101f"

st.set_page_config(page_title="UFO Cred | Mission Control", page_icon="🛸", layout="wide", initial_sidebar_state="expanded")


def asset_uri(filename: str) -> str:
    path = ASSETS / filename
    if not path.is_file():
        return ""
    return "data:image/png;base64," + base64.b64encode(path.read_bytes()).decode("ascii")


brand = asset_uri("ufo_cred_brand.png")
observatory = asset_uri("observatory.png")
nebula = asset_uri("nebula_ufo.png")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;600&family=Inter:wght@400;500;600;700&display=swap');
html, body, [class*="css"], [data-testid="stAppViewContainer"] {font-family:Inter,Arial,sans-serif;}
.stApp {background:radial-gradient(ellipse at 78% -18%,#29345c 0%,#101a32 34%,#080e1c 80%);color:#edf1ff;}
.block-container {max-width:1550px;padding-top:1.5rem;padding-bottom:3rem;}
[data-testid="stSidebar"] {background:linear-gradient(180deg,#0b1223,#10122b 60%,#090f20);border-right:1px solid #3d355e;}
[data-testid="stSidebar"] .block-container {padding-top:1rem;}
[data-testid="stSidebar"] .stRadio label {font-size:.92rem;}
[data-testid="stSidebar"] [role="radiogroup"] label {border-radius:9px;padding:8px 10px;margin:2px 0;}
[data-testid="stSidebar"] [role="radiogroup"] label:has(input:checked) {background:linear-gradient(90deg,#593d7c,#262243);border:1px solid #7f5ba7;}
h1,h2,h3 {font-family:Cinzel,Georgia,serif;color:#f4f0ff;letter-spacing:.012em;}
h1 {font-size:2.6rem !important;margin-bottom:0 !important;}
h3 {font-size:1.17rem !important;}
[data-testid="stMetric"] {background:linear-gradient(145deg,rgba(19,32,57,.95),rgba(14,20,40,.95));border:1px solid #60528e;border-radius:14px;padding:17px 20px;box-shadow:0 0 22px #603b8b18;min-height:145px;}
[data-testid="stMetricLabel"] {color:#e0e1f3;}
[data-testid="stMetricValue"] {color:#faf8ff;font-family:Georgia,serif;font-size:2.4rem;}
[data-testid="stVerticalBlockBorderWrapper"] > div {border-color:#465377 !important;}
[data-testid="stDataFrame"], [data-testid="stPlotlyChart"] {border-radius:12px;overflow:hidden;}
.stButton button, .stDownloadButton button {border:1px solid #7d5da5;background:#26213f;color:#f0eaff;border-radius:9px;}
.stButton button:hover, .stDownloadButton button:hover {border-color:#ba89fc;color:#fff;}
[data-testid="stAlert"] {border-radius:12px;}
.ufo-eyebrow {font-size:.75rem;letter-spacing:.32em;color:#c3b6df;margin:0 0 7px;}
.ufo-sub {color:#c4cbdf;margin-top:-5px;margin-bottom:20px;}
.ufo-panel {border:1px solid #45567b;border-radius:13px;padding:17px 19px;background:linear-gradient(140deg,#101c32ed,#0c1727f2);margin-bottom:14px;min-height:100px;}
.ufo-panel h3 {margin:0 0 8px;}
.ufo-muted {color:#aab6d0;font-size:.88rem;}
.ufo-pill {display:inline-block;background:#302249;color:#d6b1ff;border:1px solid #674783;padding:4px 10px;border-radius:25px;font-size:.75rem;}
.ufo-ready {color:#69edbe;}
.ufo-brand {width:100%;max-width:250px;display:block;margin:0 auto 14px;}
.ufo-obs {width:100%;border-radius:12px;opacity:.8;margin-top:28px;}
.ufo-hero {background:linear-gradient(90deg,#0b1426 0%,#12142d88 54%,#09152544 100%);border:1px solid #35476c;border-radius:15px;padding:20px 24px;margin-bottom:22px;min-height:165px;display:flex;align-items:center;justify-content:space-between;gap:20px;}
.ufo-hero-art {width:290px;max-width:40%;height:125px;object-fit:cover;border-radius:10px;opacity:.9;mix-blend-mode:screen;}
.ufo-evidence {background:#111a2c;border:1px solid #415275;border-radius:12px;padding:12px;margin:5px 0 10px;}
.ufo-evidence img {width:100%;height:145px;object-fit:cover;border-radius:8px;}
.ufo-evidence-name {overflow-wrap:anywhere;font-size:.82rem;color:#d9dff5;margin-top:9px;}
.ufo-map {height:265px;border-radius:11px;background:radial-gradient(ellipse at center,#23335a 0%,#101d34 55%,#0b1629 100%);border:1px solid #35486d;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;padding:25px;}
.ufo-map .globe {font-size:5rem;filter:drop-shadow(0 0 15px #ae7eff55);}
.ufo-model {display:flex;justify-content:space-between;align-items:center;border-bottom:1px solid #36445e;padding:12px 0;gap:12px;font-size:.88rem;}
.ufo-model:last-child {border-bottom:none;}
.ufo-status {border:1px solid #53627b;color:#c1cce1;border-radius:20px;padding:4px 9px;font-size:.75rem;white-space:nowrap;}
.ufo-footer {margin-top:26px;color:#8998b8;font-size:.77rem;}
</style>
""", unsafe_allow_html=True)


@st.cache_data(show_spinner=False, ttl=60)
def inventory() -> pd.DataFrame:
    return load_files()


def panel(title: str, body: str, pill: str = "") -> None:
    pill_html = f'<span class="ufo-pill">{pill}</span>' if pill else ""
    st.markdown(f'<div class="ufo-panel"><h3>{title} {pill_html}</h3><div class="ufo-muted">{body}</div></div>', unsafe_allow_html=True)


def safe_preview(row: pd.Series, *, full: bool = False) -> None:
    path = Path(str(row["filepath"]))
    if not path.is_file():
        st.warning("This file is no longer at its indexed location. Refresh the inventory.")
        return
    if row["file_type"] == "image":
        st.image(str(path), use_container_width=True)
    elif row["file_type"] == "video":
        if full:
            st.video(str(path))
        else:
            st.markdown('<div class="ufo-map"><span class="globe">🎞️</span>Video evidence</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="ufo-map"><span class="globe">📄</span>PDF report</div>', unsafe_allow_html=True)
        if full:
            st.caption("PDF preview is not enabled yet; use the filename to locate the original.")


with st.sidebar:
    if brand:
        st.markdown(f'<img class="ufo-brand" src="{brand}" alt="UFO Cred"/>', unsafe_allow_html=True)
    else:
        st.markdown("## 🛸 UFO CRED")
    navigation = {
        "🏠  Mission Control": "Mission Control",
        "📁  Evidence Explorer": "Evidence Explorer",
        "🧠  Analysis & Models": "Analysis & Models",
        "📊  Visualizations": "Visualizations",
        "↗  Forecasting": "Forecasting",
        "📄  Reports": "Reports",
        "⚙️  Settings": "Settings",
    }
    selected = st.radio("Navigate", list(navigation), label_visibility="collapsed")
    page = navigation[selected]
    st.caption("EVIDENCE OBSERVATORY  •  V1.0")
    if st.button("↻ Refresh evidence", use_container_width=True):
        inventory.clear()
        st.rerun()
    if observatory:
        st.markdown(f'<img class="ufo-obs" src="{observatory}" alt="Observatory at night"/>', unsafe_allow_html=True)

files = inventory()
counts = files.file_type.value_counts() if not files.empty else pd.Series(dtype=int)
num = lambda kind: int(counts.get(kind, 0))

if page == "Mission Control":
    hero_art = f'<img class="ufo-hero-art" src="{nebula}" alt="Nebula and UFO"/>' if nebula else ""
    st.markdown(f'''<div class="ufo-hero"><div><div class="ufo-eyebrow">ANOMALY  •  PATTERN  •  CREDIBILITY  •  FORECAST</div><h1>Mission Control</h1><div class="ufo-sub">A central dashboard for UFO report analysis, evidence exploration, and model insights.</div><span class="ufo-ready">● Inventory system online</span></div>{hero_art}</div>''', unsafe_allow_html=True)
    if not DATA_DIR.is_dir():
        st.warning(f"No data directory found at {DATA_DIR}. Create it and add JPG, PNG, PDF, or MP4 files.")
    elif files.empty:
        st.info("No supported evidence files yet. Add media under data/ and refresh the inventory.")
    k1, k2, k3, k4 = st.columns(4)
    k1.metric("◈  Total Reports / Files", f"{len(files):,}", help="One inventory record per media file, not necessarily one unique sighting")
    k2.metric("▧  Image Files", f"{num('image'):,}")
    k3.metric("▤  PDF Files", f"{num('pdf'):,}")
    k4.metric("▷  Video Files", f"{num('video'):,}")

    left, right = st.columns([1, 1.3], gap="medium")
    with left:
        st.subheader("✧ Report Media Types")
        if not files.empty:
            values = [num("image"), num("video"), num("pdf")]
            fig = go.Figure(go.Pie(labels=["Images", "Videos", "PDFs"], values=values, hole=.65,
                                   marker=dict(colors=[VIOLET, TEAL, SKY]), textinfo="none", sort=False))
            fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                              font=dict(color="#e7e8fa", family="Arial"), height=290,
                              margin=dict(l=8,r=8,t=5,b=5),
                              legend=dict(orientation="v", x=1, y=.8))
            fig.add_annotation(text=f"<b>{len(files):,}</b><br><span style='font-size:12px'>Total Files</span>",
                               x=.37,y=.5,showarrow=False,font=dict(size=23,color="#f5f1ff"))
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar":False})
        else:
            panel("Awaiting evidence", "Media composition will populate when files are added.")
    with right:
        st.subheader("▣ Recent Evidence")
        st.caption("Inventory sample • dates are not inferred from filenames")
        if not files.empty:
            sample = files.tail(3).iloc[::-1]
            cards = st.columns(3)
            for card, (_, item) in zip(cards, sample.iterrows()):
                with card:
                    if item.file_type == "image":
                        try:
                            st.image(str(item.filepath), use_container_width=True)
                        except Exception:
                            st.caption("Image preview unavailable")
                    else:
                        icon = "📄" if item.file_type == "pdf" else "🎞️"
                        st.markdown(f'<div class="ufo-evidence"><div style="font-size:3rem;text-align:center;padding:35px 0">{icon}</div></div>', unsafe_allow_html=True)
                    st.caption(f"{item.filename[:35]}{'…' if len(item.filename)>35 else ''}")
                    st.caption(item.file_type.upper())
        else:
            panel("Evidence explorer", "Your image, PDF, and video previews will appear here.")

    mapcol, mlcol = st.columns([1.1, 1], gap="medium")
    with mapcol:
        st.subheader("◎ Global Sightings Map")
        st.markdown('<div class="ufo-map"><div class="globe">🌐</div><div class="ufo-pill">FUTURE FEATURE</div><p class="ufo-muted">Verified geographic coordinates needed before plotting real sighting locations.</p></div>', unsafe_allow_html=True)
    with mlcol:
        st.subheader("♧ ML Laboratory")
        st.caption("Model status, performance, and insights")
        st.markdown('''<div class="ufo-panel">
        <div class="ufo-model"><span>♢ &nbsp; Credibility Models</span><span class="ufo-status">Not trained</span></div>
        <div class="ufo-model"><span>⌁ &nbsp; Anomaly Detection</span><span class="ufo-status">Not trained</span></div>
        <div class="ufo-model"><span>◌ &nbsp; Clustering (HDBSCAN)</span><span class="ufo-status">Not trained</span></div>
        <div class="ufo-model"><span>↗ &nbsp; Forecast Model</span><span class="ufo-status">Phase 2</span></div>
        </div>''', unsafe_allow_html=True)

elif page == "Evidence Explorer":
    st.title("Evidence Explorer")
    st.caption("Search and inspect local UFO media without modifying source files.")
    a, b = st.columns([1, 2])
    with a:
        kind = st.selectbox("Media type", ["All", "image", "pdf", "video"])
    with b:
        query = st.text_input("Search filename", placeholder="UAP, 2024, report...")
    view = files.copy()
    if kind != "All":
        view = view[view.file_type == kind]
    if query:
        view = view[view.filename.str.contains(query, case=False, regex=False, na=False)]
    st.caption(f"{len(view)} matching files")
    if not view.empty:
        st.dataframe(view[["report_id", "filename", "file_type", "size_mb"]], use_container_width=True, hide_index=True)
        chosen = st.selectbox("Inspect evidence", view.report_id.tolist(),
                              format_func=lambda rid: view.loc[view.report_id.eq(rid), "filename"].iloc[0])
        item = view.loc[view.report_id.eq(chosen)].iloc[0]
        st.subheader(item.filename)
        st.caption(f"{item.file_type.upper()} • {item.size_mb} MB • {item.report_id}")
        safe_preview(item, full=True)
    else:
        st.info("No matching evidence files. Try a different filter or add files under data/.")

elif page == "Analysis & Models":
    st.title("ML Laboratory")
    st.caption("Seven planned models • No training is run when the dashboard opens.")
    for title, description in [
        ("Credibility classification", "Random Forest • Logistic Regression • Gradient Boosting. Requires defensible labeled credibility data."),
        ("Anomaly detection", "Isolation Forest. Requires a validated, numeric feature matrix."),
        ("Unsupervised clustering", "KMeans • Gaussian Mixture • HDBSCAN. Requires preprocessing and feature scaling decisions."),
    ]:
        panel(title, description, "Not trained")
    st.info("The original train.py is preserved for debugging. Its models are not connected to this UI yet.")

elif page == "Visualizations":
    st.title("Visualizations")
    st.caption("Real inventory statistics today; geographic and time-series plots later.")
    if files.empty:
        st.info("Add evidence files to populate the charts.")
    else:
        totals = files.groupby("file_type", as_index=False).agg(files=("filename", "count"), megabytes=("size_mb", "sum"))
        fig = go.Figure(go.Bar(x=totals.file_type, y=totals.files, marker_color=[VIOLET, TEAL, SKY][:len(totals)]))
        fig.update_layout(title="Evidence count by type", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font_color="#e6e8fb")
        st.plotly_chart(fig, use_container_width=True)
        st.dataframe(totals, hide_index=True, use_container_width=True)
    panel("Global sightings map", "Requires verified coordinates. No locations are invented.", "Planned")
    panel("Sighting timeline", "Requires actual sighting dates rather than file creation times.", "Planned")

elif page == "Forecasting":
    st.title("Forecasting")
    panel("Temporal observatory", "Forecasting models need dated sightings, an explicit prediction target, and a time-aware validation strategy.", "Phase 2")

elif page == "Reports":
    st.title("Reports")
    st.caption("Export a current evidence inventory as CSV.")
    st.download_button("Download evidence inventory", files.to_csv(index=False).encode("utf-8"),
                       "ufo_cred_inventory.csv", "text/csv", disabled=files.empty)
    st.dataframe(files, use_container_width=True, hide_index=True)

else:
    st.title("Settings")
    st.write("**Evidence directory:**", str(DATA_DIR))
    st.write("**Discovered files:**", len(files))
    st.caption("Supported formats: JPG, JPEG, PNG, PDF, MP4")
    if st.button("Refresh file inventory"):
        inventory.clear()
        st.rerun()

st.markdown('<div class="ufo-footer">UFO CRED • Evidence Observatory • Exploration is not a determination of authenticity or extraterrestrial origin. • Visual assets adapted from the approved concept mockup.</div>', unsafe_allow_html=True)
