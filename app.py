import streamlit as st
import pandas as pd
import json
import requests
import plotly.graph_objects as go
from PIL import Image
from io import BytesIO

# -----------------------------------------------
# Page config (MUST be first Streamlit call)
# -----------------------------------------------
st.set_page_config(layout="wide", page_title="OB Lineouts", page_icon="🏉")

# -----------------------------------------------
# Google Sheet URL — replace SHEET_ID with yours.
# In Google Sheets: File → Share → Publish to web
# → Sheet1 → CSV → Publish, then paste the URL.
# -----------------------------------------------
SHEET_URL = "https://docs.google.com/spreadsheets/d/19f9aFK5Ovdlu2L17Bj_cyOFQi4Gcs8072iXQnzYPL8c/edit?usp=sharing"

@st.cache_data(ttl=300)
def load_data():
    try:
        df = pd.read_csv(SHEET_URL)
    except Exception:
        df = pd.read_excel("OBLineouts.xlsx", engine="openpyxl")
    df["Timestamp"] = df["Timestamp"].astype(str)
    df["Personnel"] = pd.to_numeric(df["Personnel"], errors="coerce").fillna(0).astype(int)
    return df

@st.cache_data(show_spinner=False)
def load_logo(url, size=(48, 48)):
    if not url:
        return None
    try:
        resp = requests.get(url, timeout=6)
        resp.raise_for_status()
        img = Image.open(BytesIO(resp.content)).convert("RGBA")
        img.thumbnail(size, Image.LANCZOS)
        return img
    except Exception:
        return None

with open("team_formats.json") as f:
    stylers = json.load(f)

def get_cfg(team):
    cfg = stylers.get(str(team), {})
    return cfg.get("logo", ""), cfg.get("header_color", "#333333")

# -----------------------------------------------
# Stats helpers
# -----------------------------------------------
def mode_call(sub):
    m = sub["Call"].mode()
    return m[0] if not m.empty else "N/A"

def success_rate(sub):
    return (sub["Outcome"].eq("Won").sum() / len(sub)) * 100 if len(sub) else 0

def defended_rate(sub):
    return (sub["Defended"].eq("Y").sum() / len(sub)) * 100 if len(sub) else 0

# -----------------------------------------------
# HTML helpers
# -----------------------------------------------
def hex_to_rgba(hex_color, alpha=0.12):
    h = hex_color.lstrip("#")
    r, g, b = int(h[0:2],16), int(h[2:4],16), int(h[4:6],16)
    return f"rgba({r},{g},{b},{alpha})"

def styled_table(df_view, color, team_name, logo_url):
    light = hex_to_rgba(color, 0.10)
    mid   = hex_to_rgba(color, 0.25)
    rows_html = ""
    for i, row in df_view.iterrows():
        bg = "#ffffff" if i % 2 == 0 else "#fafafa"
        cells = ""
        for col in df_view.columns:
            val = row[col]
            if col == "Outcome":
                c = "#2a7a2a" if val == "Won" else "#c0392b"
                cell = f'<td style="padding:5px 10px;border-bottom:1px solid #f0f0f0;white-space:nowrap;color:{c};font-weight:bold">{val}</td>'
            else:
                cell = f'<td style="padding:5px 10px;border-bottom:1px solid #f0f0f0;white-space:nowrap">{val}</td>'
            cells += cell
        rows_html += f'<tr style="background:{bg}">{cells}</tr>'

    headers = "".join(
        f'<th style="background:{light};color:{color};padding:7px 10px;text-align:left;'
        f'white-space:nowrap;font-size:13px;letter-spacing:0.04em;border-bottom:2px solid {mid}">{c}</th>'
        for c in df_view.columns
    )

    logo_tag = f'<img src="{logo_url}" style="height:36px;width:36px;object-fit:contain;border-radius:4px">' if logo_url else ""

    return f"""
    <div style="border-radius:10px;overflow:hidden;box-shadow:0 2px 10px rgba(0,0,0,0.10);
                background:#fff;margin-bottom:4px">
      <div style="display:flex;align-items:center;gap:10px;padding:10px 14px;background:{color}">
        {logo_tag}
        <span style="font-family:'Bebas Neue',sans-serif;font-size:20px;color:white;
                     letter-spacing:0.05em">{team_name}</span>
      </div>
      <div style="overflow-x:auto">
        <table style="width:100%;border-collapse:collapse;font-family:'Bebas Neue',sans-serif;font-size:13px">
          <thead><tr>{headers}</tr></thead>
          <tbody>{rows_html}</tbody>
        </table>
      </div>
    </div>
    """

def metric_card(label, value, color):
    return f"""
    <div style="background:#fff;border-radius:10px;padding:12px 8px;text-align:center;
                box-shadow:0 2px 6px rgba(0,0,0,0.08);flex:1;border-top:3px solid {color}">
      <div style="font-family:'Bebas Neue',sans-serif;font-size:11px;color:#888;
                  letter-spacing:0.06em;text-transform:uppercase;margin-bottom:4px">{label}</div>
      <div style="font-family:'Bebas Neue',sans-serif;font-size:26px;color:#111">{value}</div>
    </div>
    """

def metrics_row(sub, color):
    cards = (
        metric_card("Top Call",     mode_call(sub), color) +
        metric_card("Success Rate", f"{success_rate(sub):.1f}%", color) +
        metric_card("Defended",     f"{defended_rate(sub):.1f}%", color)
    )
    return f'<div style="display:flex;gap:10px;margin-top:10px">{cards}</div>'

# -----------------------------------------------
# Global CSS
# -----------------------------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&display=swap');
html, body, [class*="css"]  { font-family: 'Bebas Neue', sans-serif !important; }
h1, h2, h3, h4, h5, h6     { font-family: 'Bebas Neue', sans-serif !important; }
h1  { font-size: 52px; text-align: center; color: #111; margin-bottom: 0; }
p   { font-size: 16px; }
div[data-baseweb="select"] span,
div[data-baseweb="select"] label { font-family: 'Bebas Neue', sans-serif !important; font-size: 16px; }
hr  { border: none; border-top: 2px solid #e0e0e0; margin: 16px 0; }
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------
# Load data
# -----------------------------------------------
df = load_data()
valid_teams     = sorted(set(df["Team"]).intersection(stylers))
valid_opponents = sorted(set(df["Opponent"]).intersection(stylers))

# -----------------------------------------------
# Header
# -----------------------------------------------
st.markdown("<h1>🏉 Old Belvedere Juniors — Lineouts</h1>", unsafe_allow_html=True)
st.markdown("<hr>", unsafe_allow_html=True)

# -----------------------------------------------
# Selectors
# -----------------------------------------------
sel_col1, sel_col2 = st.columns(2)

with sel_col1:
    selected_team = st.selectbox("Select Team", valid_teams, key="selected_team")

with sel_col2:
    selected_opponent = st.selectbox("Select Opponent", valid_opponents, key="selected_opponent")

team_logo_url, team_color = get_cfg(selected_team)
opp_logo_url,  opp_color  = get_cfg(selected_opponent)

# Selector cards with logo + colour bar
def selector_card(logo_url, name, color):
    logo_tag = f'<img src="{logo_url}" style="height:40px;width:40px;object-fit:contain;border-radius:4px">' if logo_url else ""
    return f"""
    <div style="background:white;border-radius:10px;padding:10px 14px;
                box-shadow:0 1px 5px rgba(0,0,0,0.09);border-left:4px solid {color};
                display:flex;align-items:center;gap:10px;margin-top:-8px;margin-bottom:12px">
      {logo_tag}
      <span style="font-family:'Bebas Neue',sans-serif;font-size:20px;color:{color}">{name}</span>
    </div>
    """

with sel_col1:
    st.markdown(selector_card(team_logo_url, selected_team, team_color), unsafe_allow_html=True)
with sel_col2:
    st.markdown(selector_card(opp_logo_url, selected_opponent, opp_color), unsafe_allow_html=True)

# -----------------------------------------------
# Filter
# -----------------------------------------------
fixture_df    = df[(df["Team"] == selected_team) & (df["Opponent"] == selected_opponent)].copy()
your_team_df  = fixture_df[fixture_df["Throw In"] == "Old Belvedere"].reset_index(drop=True)
opposition_df = fixture_df[fixture_df["Throw In"] == selected_opponent].reset_index(drop=True)

VIEW_COLS = ["Call", "Movement", "Outcome", "Clean", "Play", "Receiver", "Defended", "Defender", "Personnel"]

# -----------------------------------------------
# Tables + Metrics
# -----------------------------------------------
st.markdown("<hr>", unsafe_allow_html=True)
tcol, ocol = st.columns(2)

with tcol:
    st.markdown(styled_table(your_team_df[VIEW_COLS],  team_color, selected_team,     team_logo_url), unsafe_allow_html=True)
    st.markdown(metrics_row(your_team_df,  team_color), unsafe_allow_html=True)

with ocol:
    st.markdown(styled_table(opposition_df[VIEW_COLS], opp_color,  selected_opponent, opp_logo_url),  unsafe_allow_html=True)
    st.markdown(metrics_row(opposition_df, opp_color),  unsafe_allow_html=True)

# -----------------------------------------------
# Pitch visualisation
# -----------------------------------------------
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("<h2 style='text-align:center;letter-spacing:0.05em'>Lineout Positions</h2>", unsafe_allow_html=True)

PITCH_LEN, PITCH_WID = 100, 70
fig = go.Figure()

# Pitch background + in-goal shading
fig.add_shape(type="rect", x0=0, y0=0, x1=PITCH_LEN, y1=PITCH_WID, fillcolor="#3a8a3a", line=dict(width=0))
for x0, x1 in [(0, 5), (95, 100)]:
    fig.add_shape(type="rect", x0=x0, y0=0, x1=x1, y1=PITCH_WID, fillcolor="#2d7030", line=dict(width=0))

# Pitch lines
for x in [5, 22, 50, 78, 95]:
    fig.add_shape(type="line", x0=x, y0=0, x1=x, y1=PITCH_WID,
                  line=dict(color="rgba(255,255,255,0.45)", width=1.5, dash="dash"))
    fig.add_annotation(x=x, y=PITCH_WID + 1.5, text=f"{x}m", showarrow=False,
                       font=dict(color="white", size=11, family="Bebas Neue"), xanchor="center")

for x in [0, 100]:
    fig.add_shape(type="line", x0=x, y0=0, x1=x, y1=PITCH_WID, line=dict(color="white", width=2.5))

# Scatter traces — won (circle) and lost (x) for each team
for sub, color, name in [
    (your_team_df,  team_color, selected_team),
    (opposition_df, opp_color,  selected_opponent),
]:
    for outcome, symbol in [("Won", "circle"), ("Lost", "x")]:
        mask = sub["Outcome"] == outcome
        s = sub[mask]
        if len(s):
            fig.add_trace(go.Scatter(
                x=s["Distance to Opponent Tryline"],
                y=s["Side"],
                mode="markers",
                marker=dict(size=14, color=color, symbol=symbol,
                            opacity=0.9, line=dict(color="white", width=1.8)),
                name=f"{name} — {outcome}",
                customdata=s[["Call", "Play", "Receiver"]].fillna("—").values,
                hovertemplate=(
                    "<b>%{customdata[0]}</b><br>"
                    "Distance: %{x}m<br>"
                    "Play: %{customdata[1]}<br>"
                    "Receiver: %{customdata[2]}<extra></extra>"
                ),
            ))

fig.update_layout(
    font=dict(family="Bebas Neue, sans-serif"),
    paper_bgcolor="#1a1a1a",
    plot_bgcolor="#3a8a3a",
    legend=dict(orientation="h", yanchor="top", y=-0.08, xanchor="center", x=0.5,
                bgcolor="rgba(0,0,0,0)", font=dict(color="white", size=13)),
    xaxis=dict(range=[-2, 102], showgrid=False, zeroline=False,
               title=dict(text="Distance to Opponent Try Line (m)",
                          font=dict(color="white", size=13)),
               tickfont=dict(color="white")),
    yaxis=dict(range=[-5, 75], showgrid=False, zeroline=False,
               tickvals=[0, 70], ticktext=["Near", "Far"],
               tickfont=dict(color="white", size=12)),
    margin=dict(t=50, b=70, l=60, r=20),
    height=420,
)

st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False, "scrollZoom": False})
