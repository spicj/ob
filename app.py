import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from datetime import datetime, timedelta

df = pd.read_excel("OBLineouts.xlsx")
df['Timestamp'] =df['Timestamp'].astype(str)
df['Personnel'] = df['Personnel'].round(0).astype(int)
st.set_page_config(layout="wide")

st.markdown("""
<style>
    h1 {
        font-family: 'Bebas Neue', sans-serif;
        font-size: 60px;
        color: #000000;
        text-align: center; /* Centers the title */
    }
</style>
""", unsafe_allow_html=True)

st.title("Old Belvedere Juniors - Lineouts")



st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&display=swap');

    /* Apply Bebas Neue globally */
    html, body, [class*="css"] {
        font-family: 'Bebas Neue', sans-serif !important;
    }

    /* Optional: Adjust default paragraph size */
    p {
        font-size: 18px;
    }

    /* Headings */
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Bebas Neue', sans-serif !important;
    }
</style>
""", unsafe_allow_html=True)



st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&display=swap');

        /* Apply font to all Streamlit widgets */
        div[data-baseweb="select"], div[data-baseweb="slider"], div[data-baseweb="input"] label {
            font-family: 'Bebas Neue', sans-serif;
            font-size: 18px;
            color: #000000; /* Black text */
        }

        /* Dropdown options */
        div[data-baseweb="select"] span {
            font-family: 'Bebas Neue', sans-serif;
            font-size: 16px;
        }

        /* Slider value */
        div[data-baseweb="slider"] span {
            font-family: 'Bebas Neue', sans-serif;
            font-size: 16px;
            color: #FF0000; /* Red for emphasis */
        }

        /* Buttons */
        button[kind="primary"] {
            font-family: 'Bebas Neue', sans-serif;
            background-color: #000000;
            color: white;
            font-size: 18px;
            border-radius: 6px;
        }
    </style>
""", unsafe_allow_html=True)

def mode(df):
    return df["Call"].mode()[0] if not df["Call"].mode().empty else "N/A"

def success(df):
    return (df["Outcome"].eq("Won").sum() / len(df["Outcome"])) * 100 if len(df) > 0 else 0

def defended(df):
    return (df["Defended"].eq("Y").sum() / len(df["Defended"])) * 100 if len(df) > 0 else 0


# Create two columns
col1, col2 = st.columns(2)

with col1: 
    # Create two columns: logo on the left, slicer on the right
    logo_col, slicer_col = st.columns([1, 7])  # Adjust ratio for spacing

    with logo_col:
        st.image("https://www.thefrontrowunion.com/wp-content/uploads/2020/09/Old-Belvedere-Crest.png", use_column_width=True)

    with slicer_col:
        selected_team = st.selectbox("Select Team", df["Team"].unique())




with col2:
    # Create two columns: logo on the left, slicer on the right
    logo_col, slicer_col = st.columns([1, 7])  # Adjust ratio for spacing

    with logo_col:
        st.image("https://www.oldwesley.ie/wp-content/uploads/2019/11/Old-Wesley-Crest.png", use_column_width=True)

    with slicer_col:
        selected_team = st.selectbox("Select Opponent", df["Opponent"].unique())

filtered_df = df[df["Opponent"] == selected_team]


your_team_df = filtered_df[filtered_df["Throw In"] == "Old Belvedere"]

opposition_df = filtered_df[filtered_df["Throw In"] != "Old Belvedere"]

your_team_df_view = your_team_df[['Call', 'Movement', 'Outcome', 'Clean','Play', 'Receiver', 'Defended', 'Defender', 'Personnel']]
opposition_df_view = opposition_df[['Call', 'Movement', 'Outcome', 'Clean','Play', 'Receiver', 'Defended', 'Defender', 'Personnel']]
# Table 1 (Black header)



styled_html_1 = f"""
<div class="table1" style="width: 100%; overflow-x: auto;">
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&display=swap');

        .table1 table {{
            font-family: 'Bebas Neue', sans-serif;
            font-size: 18px;
            padding: 4px 8px !important;
            line-height: 1.2;
            white-space: nowrap;
            border-collapse: collapse;
        }}
        .table1 th {{
            background-color: #000000;
            color: white;
            font-size: 18px;
        }}
        .table1 .logo-container {{
            display: flex;
            align-items: center;
            margin-bottom: 8px;
        }}
        .table1 .logo-container img {{
            height: 40px;
            margin-right: 10px;
        }}
        .table1 .logo-container span {{
            font-family: 'Bebas Neue', sans-serif;
            font-size: 24px;
            color: #000000;
        }}
    </style>
    <div class="logo-container">
        <img src = "https://www.thefrontrowunion.com/wp-content/uploads/2020/09/Old-Belvedere-Crest.png" >
        <span>Old Belvedere</span>
    </div>
    <div class="custom-table">
        {your_team_df_view.style.hide(axis="index").to_html()}
"""








# Table 2 (Red header)
styled_html_2 = f"""
<div class="table2" style="width: 100%; overflow-x: auto;">
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&display=swap');

        .table2 table {{
            font-family: 'Bebas Neue', sans-serif;
            font-size: 18px;
            padding: 4px 8px !important;
            line-height: 1.2;
            white-space: nowrap;
            border-collapse: collapse;
        }}
        .table2 th {{
            background-color: #FF0000;
            color: white;
            font-size: 18px;
        }}
        .table2 .logo-container {{
            display: flex;
            align-items: center;
            margin-bottom: 8px;
        }}
        .table2 .logo-container img {{
            height: 40px;
            margin-right: 10px;
        }}
        .table2 .logo-container span {{
            font-family: 'Bebas Neue', sans-serif;
            font-size: 24px;
            color: #FF0000;
        }}
        <img src="https://www.thefrontrowunion.com/wp-content/uploads/2020/09/Old-Belvedere-Crest.png">
        <span>Old Belvedere</span>
           </style>
    </div>
    <div class="custom-table">
        {opposition_df_view.style.hide(axis="index").to_html()}
"""

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&display=swap');
    /* Apply Bebas Neue font to metrics */
    div[data-testid="stMetric"] {
        font-family: 'Bebas Neue', sans-serif;
        color: #000000; /* Black text */
    }
    div[data-testid="stMetric"] > label {
        font-size: 18px;
    }
    div[data-testid="stMetric"] > div {
        font-size: 24px; /* Bigger for metric value */
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<style>
.metric-card {
    background-color: #f9f9f9; /* Light background */
    border-radius: 12px;       /* Soft rounded corners */
    padding: 16px;
    margin: 8px;
    box-shadow: 0 4px 8px rgba(0,0,0,0.1); /* Subtle shadow */
    text-align: center;
    font-family: 'Bebas Neue', sans-serif;
}
.metric-card h3 {
    font-size: 18px;
    color: #333;
    margin-bottom: 8px;
}
.metric-card p {
    font-size: 24px;
    font-weight: bold;
    color: #000;
}
</style>
""", unsafe_allow_html=True)



with col1:  
    st.markdown(styled_html_1, unsafe_allow_html=True)
    m1, m2, m3 = st.columns(3)
    m1.metric("Most Common Call", mode(your_team_df))
    m2.metric("Success Rate (%)", f"""{success(your_team_df):.1f}%""")
    m3.metric("Defended (%)", f"""{defended(your_team_df):.1f}%""")


with col2:
    st.markdown(styled_html_2, unsafe_allow_html=True)
    m4, m5, m6 = st.columns(3)
    m4.metric("Most Common Call", mode(opposition_df))
    m5.metric("Success Rate (%)", f"""{success(opposition_df):.1f}%""")
    m6.metric("Defended (%)", f"""{defended(opposition_df):.1f}%""")



import plotly.graph_objects as go

# Assume your positional columns are 'X' and 'Y' (scaled to pitch dimensions)
pitch_length = 100  # meters
pitch_width = 70    # meters

fig = go.Figure()

# Scatter lineouts
fig.add_trace(go.Scatter(
    x=your_team_df["Distance to Opponent Tryline"], y=your_team_df["Side"],
    mode="markers",
    marker=dict(size=20, color="#000000", opacity=0.7),
    name="Old Belvedere",
    text=your_team_df["Call"]
))

fig.add_trace(go.Scatter(
    x=opposition_df["Distance to Opponent Tryline"], y=opposition_df["Side"],
    mode="markers",
    marker=dict(size=20, color="#FF0000", opacity=0.7),
    name="Old Wesley",
    text=opposition_df["Call"]
))
# Draw pitch background
fig.add_shape(type="rect",
              x0=0, y0=0, x1=pitch_length, y1=pitch_width,
              line=dict(color="green", width=3),
              fillcolor="lightgreen")

# Add key pitch lines
for x in [0, 5, 22, 40, 50, 60, 78, 95, 100]:  # try lines, 22m, halfway
    fig.add_shape(type="line",
                  x0=x, y0=0, x1=x, y1=pitch_width,
                  line=dict(color="white", width=2, dash="dash"))


fig.update_layout(
    
title={
        'text': "Lineout Positions on Pitch",
        'font': {
            'family': 'Bebas Neue, sans-serif',  # Custom font
            'size': 32,                          # Font size
            'color': 'black'                     # Font color
        },
        'x': 0.5,  # Center the title
        'xanchor': 'center'
    },
    legend= dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5, bgcolor="rgba(0,0,0,0)"),# Transparent background,
    xaxis=dict(range=[0, pitch_length], showgrid=False, zeroline=False),
    yaxis=dict(range=[0, pitch_width], showgrid=False, zeroline=False),
    plot_bgcolor="green",
    width=500, height=500
)


fig.update_layout(
    autosize=True,
    xaxis=dict(autorange=True),
    yaxis=dict(autorange=True)
)


st.plotly_chart(fig, use_container_width=True, config={
    'displayModeBar': False,  # Hide toolbar
    'scrollZoom': False       # Disable scroll zoom
})



