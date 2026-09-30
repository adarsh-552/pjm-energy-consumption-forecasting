"""
PJM Energy Consumption Forecasting - Production Dashboard

Presents the pre-generated 30-day (720 hour) XGBoost forecast stored in
PJM_30_Day_Forecast_XGBoost.xlsx. No model is trained or loaded here.

Run with:
    python -m streamlit run streamlit_app.py

Requires: streamlit, pandas, plotly, openpyxl
"""

import io
import math
from dataclasses import dataclass
from pathlib import Path

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
FORECAST_FILE = "PJM_30_Day_Forecast_XGBoost.xlsx"
REQUIRED_COLUMNS = ["Datetime", "Forecast_MW"]
MODEL_NAME = "XGBoost"

# Final test-set performance of the selected production model (from the notebook)
MODEL_METRICS = [
    ("MAE", "57.12", "MW", "Mean Absolute Error"),
    ("RMSE", "77.09", "MW", "Root Mean Squared Error"),
    ("MAPE", "0.99", "%", "Mean Absolute Percentage Error"),
]

FEATURE_GROUPS = {
    "Temporal Features": [
        "Hour", "Day", "Month", "Year", "Day of Week", "Holiday Indicator",
    ],
    "Cyclical Features": [
        "Hour Sin/Cos", "Month Sin/Cos", "Day-of-Week Sin/Cos",
    ],
    "Lag Features": ["Lag 1", "Lag 24", "Lag 168"],
    "Rolling Features": [
        "24-hour rolling mean", "168-hour rolling mean", "24-hour rolling std",
    ],
}

PAGES = ["Overview", "Forecast Analysis", "Forecast Data", "Model Information"]

# Palette (mirrored in the CSS variables below)
BG = "#0A1628"
PANEL = "#0F1F3A"
PANEL_2 = "#13274A"
BORDER = "#1F3560"
TEXT_PRIMARY = "#E6EDF7"
TEXT_MUTED = "#8FA3C0"
ACCENT = "#38BDF8"
AMBER = "#FBBF24"
MINT = "#34D399"
GRID = "rgba(143, 163, 192, 0.14)"
FONT = "Inter, -apple-system, 'Segoe UI', Roboto, sans-serif"
PLOT_CONFIG = {"displaylogo": False}

st.set_page_config(
    page_title="PJM Energy Forecast",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------------------------------------------------------------------
# Styling
# ---------------------------------------------------------------------------
CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

:root {
    --bg: #0A1628;
    --side: #0B1B33;
    --panel: #0F1F3A;
    --panel-2: #13274A;
    --border: #1F3560;
    --text: #E6EDF7;
    --muted: #8FA3C0;
    --accent: #38BDF8;
    --amber: #FBBF24;
    --mint: #34D399;
}

html, body, .stApp {
    font-family: 'Inter', -apple-system, 'Segoe UI', Roboto, sans-serif;
}
.stApp { background: var(--bg); color: var(--text); }
header[data-testid="stHeader"] { background: transparent; }
#MainMenu, footer { visibility: hidden; }
.block-container { padding-top: 2rem; padding-bottom: 2rem; max-width: 1400px; }

/* ---------- Sidebar ---------- */
section[data-testid="stSidebar"] {
    background: var(--side);
    border-right: 1px solid var(--border);
}
.side-brand {
    color: var(--text);
    font-size: 1.05rem;
    font-weight: 700;
    letter-spacing: 0.02em;
    padding-bottom: 1rem;
    margin-bottom: 0.75rem;
    border-bottom: 1px solid var(--border);
}
.side-brand-sub { color: var(--muted); font-size: 0.78rem; font-weight: 400; margin-top: 0.2rem; letter-spacing: 0; }

section[data-testid="stSidebar"] div[role="radiogroup"] { gap: 0.2rem; }
section[data-testid="stSidebar"] div[role="radiogroup"] > label {
    width: 100%;
    padding: 0.6rem 0.85rem;
    border-radius: 8px;
    border: 1px solid transparent;
    cursor: pointer;
}
section[data-testid="stSidebar"] div[role="radiogroup"] > label > div:first-child { display: none; }
section[data-testid="stSidebar"] div[role="radiogroup"] > label p {
    color: var(--muted);
    font-size: 0.95rem;
    font-weight: 500;
    margin: 0;
}
section[data-testid="stSidebar"] div[role="radiogroup"] > label:hover { background: rgba(56, 189, 248, 0.08); }
section[data-testid="stSidebar"] div[role="radiogroup"] > label:has(input:checked) {
    background: rgba(56, 189, 248, 0.14);
    border-color: rgba(56, 189, 248, 0.35);
}
section[data-testid="stSidebar"] div[role="radiogroup"] > label:has(input:checked) p { color: var(--text); font-weight: 600; }

.side-status { margin-top: 2.5rem; padding-top: 1rem; border-top: 1px solid var(--border); }
.side-label { color: var(--muted); font-size: 0.75rem; font-weight: 500; margin-top: 0.9rem; }
.side-value { color: var(--text); font-size: 0.98rem; font-weight: 600; }
.status-dot {
    display: inline-block; width: 8px; height: 8px; border-radius: 50%;
    background: var(--mint); margin-right: 0.45rem;
}

/* ---------- Hero ---------- */
.hero {
    background: linear-gradient(135deg, #0E2444 0%, #0B3A66 60%, #0C4F7D 100%);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 2.25rem 2.5rem;
    margin-bottom: 1.5rem;
}
.hero-title { color: #FFFFFF; font-size: 2rem; font-weight: 700; letter-spacing: 0.01em; line-height: 1.2; }
.hero-sub { color: #9FD8F5; font-size: 1.15rem; font-weight: 500; margin-top: 0.45rem; }
.badge-row { margin-top: 1.1rem; }
.badge {
    display: inline-block; margin: 0 0.5rem 0.4rem 0; padding: 0.28rem 0.8rem;
    font-size: 0.8rem; font-weight: 500; color: #E6F4FC;
    border: 1px solid rgba(159, 216, 245, 0.45); border-radius: 999px;
    background: rgba(255, 255, 255, 0.06);
}
.hero-desc { color: #C3D5E8; font-size: 0.98rem; line-height: 1.6; max-width: 70ch; margin-top: 0.9rem; }

/* ---------- Page + section headings ---------- */
.page-title { color: var(--text); font-size: 1.7rem; font-weight: 700; line-height: 1.25; }
.page-sub { color: var(--muted); font-size: 0.98rem; margin-top: 0.3rem; margin-bottom: 1.25rem; }
.section-title { color: var(--text); font-size: 1.2rem; font-weight: 600; margin: 2rem 0 0.25rem 0; }
.section-sub { color: var(--muted); font-size: 0.9rem; margin-bottom: 0.9rem; }

/* ---------- Cards ---------- */
.card {
    background: var(--panel);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 1.1rem 1.25rem;
    min-height: 92px;
}
.card-tall { min-height: 358px; }
.card-title { color: var(--text); font-size: 1rem; font-weight: 600; margin-bottom: 0.6rem; }
.card-text { color: var(--muted); font-size: 0.93rem; line-height: 1.65; }

.kpi { min-height: 108px; border-top: 3px solid var(--border); }
.kpi-accent { border-top-color: var(--accent); }
.kpi-amber { border-top-color: var(--amber); }
.kpi-mint { border-top-color: var(--mint); }
.kpi-label { color: var(--muted); font-size: 0.8rem; font-weight: 500; margin-bottom: 0.4rem; }
.kpi-value { color: var(--text); font-size: 1.7rem; font-weight: 700; line-height: 1.2; }
.kpi-unit { color: var(--muted); font-size: 0.9rem; font-weight: 500; margin-left: 0.3rem; }

.info-label { color: var(--muted); font-size: 0.8rem; font-weight: 500; margin-bottom: 0.3rem; }
.info-value { color: var(--text); font-size: 1.15rem; font-weight: 600; }
.info-note { color: var(--muted); font-size: 0.82rem; margin-top: 0.3rem; }

.tag {
    display: inline-block; margin: 0.2rem 0.35rem 0.2rem 0; padding: 0.28rem 0.65rem;
    font-size: 0.82rem; color: #BFE6FA; border-radius: 6px;
    background: rgba(56, 189, 248, 0.10); border: 1px solid rgba(56, 189, 248, 0.28);
}

ul.obs { list-style: none; margin: 0; padding: 0; }
ul.obs li { color: var(--muted); font-size: 0.93rem; line-height: 1.55; padding: 0.7rem 0; border-bottom: 1px solid var(--border); }
ul.obs li:last-child { border-bottom: none; }
ul.obs li b { color: var(--text); font-weight: 600; }

/* ---------- Plotly containers ---------- */
div[data-testid="stPlotlyChart"] {
    background: var(--panel);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 0.5rem;
}

/* ---------- Expander ---------- */
div[data-testid="stExpander"] {
    background: var(--panel);
    border: 1px solid var(--border);
    border-radius: 12px;
}
div[data-testid="stExpander"] details { border: none; }
div[data-testid="stExpander"] summary,
div[data-testid="stExpander"] summary p { color: var(--text); font-weight: 600; }

/* ---------- Inputs ---------- */
[data-testid="stWidgetLabel"] p, [data-testid="stWidgetLabel"] label { color: var(--muted) !important; font-size: 0.82rem; }
div[data-baseweb="input"], div[data-baseweb="input"] > div, div[data-baseweb="base-input"] {
    background: var(--panel-2) !important;
    border-color: var(--border) !important;
}
div[data-baseweb="input"] input { color: var(--text) !important; }
div[data-baseweb="select"] > div { background: var(--panel-2) !important; border-color: var(--border) !important; }
div[data-baseweb="select"] div, div[data-baseweb="select"] span { color: var(--text); }
div[data-baseweb="select"] svg { fill: var(--muted); }
div[data-baseweb="popover"] ul, div[data-baseweb="popover"] li { background: var(--panel-2); color: var(--text); }

/* ---------- Data table ---------- */
.table-wrap {
    max-height: 430px; overflow-y: auto;
    border: 1px solid var(--border); border-radius: 10px; margin-top: 0.5rem;
}
table.fc-table { width: 100%; border-collapse: collapse; font-size: 0.9rem; }
table.fc-table th {
    position: sticky; top: 0; background: var(--panel-2); color: var(--muted);
    font-weight: 600; text-align: left; padding: 0.65rem 1rem; border-bottom: 1px solid var(--border);
}
table.fc-table td { color: var(--text); padding: 0.55rem 1rem; border-bottom: 1px solid rgba(31, 53, 96, 0.6); }
table.fc-table th:last-child, table.fc-table td:last-child { text-align: right; font-variant-numeric: tabular-nums; }
table.fc-table tr:hover td { background: rgba(56, 189, 248, 0.06); }
.table-caption { color: var(--muted); font-size: 0.82rem; margin-top: 0.5rem; }

/* ---------- Download buttons ---------- */
div[data-testid="stDownloadButton"] button {
    background: var(--accent);
    border: none;
    border-radius: 8px;
    padding: 0.6rem 1.4rem;
    font-weight: 600;
    width: 100%;
}
div[data-testid="stDownloadButton"] button, div[data-testid="stDownloadButton"] button p { color: #04121F !important; }
div[data-testid="stDownloadButton"] button:hover { background: #7DD3FC; }

/* ---------- Footer ---------- */
.site-footer {
    text-align: center; color: var(--muted); font-size: 0.85rem;
    border-top: 1px solid var(--border); margin-top: 3rem; padding-top: 1.25rem;
}
.site-footer b { color: var(--text); font-weight: 600; }
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# Data loading
# ---------------------------------------------------------------------------
def find_forecast_file():
    """Look next to this script first, then in the current working directory."""
    for candidate in (Path(__file__).resolve().parent / FORECAST_FILE, Path.cwd() / FORECAST_FILE):
        if candidate.exists():
            return candidate
    return None


@st.cache_data(show_spinner=False)
def load_forecast(path: str) -> pd.DataFrame:
    """Read the forecast workbook and normalise column types."""
    df = pd.read_excel(path)
    missing = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    if missing:
        raise ValueError(f"Missing column(s): {', '.join(missing)}")
    df = df[REQUIRED_COLUMNS].copy()
    df["Datetime"] = pd.to_datetime(df["Datetime"])
    df["Forecast_MW"] = pd.to_numeric(df["Forecast_MW"], errors="coerce")
    return df.dropna().sort_values("Datetime").reset_index(drop=True)


@st.cache_data(show_spinner=False)
def to_csv_bytes(df: pd.DataFrame) -> bytes:
    export = df.assign(Forecast_MW=df["Forecast_MW"].round(2))
    return export.to_csv(index=False).encode("utf-8")


@st.cache_data(show_spinner=False)
def to_excel_bytes(df: pd.DataFrame) -> bytes:
    export = df.assign(Forecast_MW=df["Forecast_MW"].round(2))
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
        export.to_excel(writer, index=False, sheet_name="Forecast")
        sheet = writer.sheets["Forecast"]
        sheet.column_dimensions["A"].width = 22
        sheet.column_dimensions["B"].width = 16
    return buffer.getvalue()


# ---------------------------------------------------------------------------
# Statistics (all calculated from the dataframe)
# ---------------------------------------------------------------------------
@dataclass(frozen=True)
class ForecastStats:
    n: int
    days: int
    avg: float
    peak: float
    peak_time: pd.Timestamp
    low: float
    low_time: pd.Timestamp
    spread: float
    start: pd.Timestamp
    end: pd.Timestamp
    frequency: str


def infer_frequency(timestamps: pd.Series) -> str:
    step = timestamps.diff().median()
    if pd.isna(step):
        return "Unknown"
    if step == pd.Timedelta(hours=1):
        return "Hourly"
    if step == pd.Timedelta(minutes=30):
        return "Half-hourly"
    if step == pd.Timedelta(days=1):
        return "Daily"
    return str(step)


def compute_stats(df: pd.DataFrame) -> ForecastStats:
    peak_idx = df["Forecast_MW"].idxmax()
    low_idx = df["Forecast_MW"].idxmin()
    peak = float(df.loc[peak_idx, "Forecast_MW"])
    low = float(df.loc[low_idx, "Forecast_MW"])
    n = len(df)
    return ForecastStats(
        n=n,
        days=max(1, round(n / 24)),
        avg=float(df["Forecast_MW"].mean()),
        peak=peak,
        peak_time=df.loc[peak_idx, "Datetime"],
        low=low,
        low_time=df.loc[low_idx, "Datetime"],
        spread=peak - low,
        start=df["Datetime"].iloc[0],
        end=df["Datetime"].iloc[-1],
        frequency=infer_frequency(df["Datetime"]),
    )


def fmt_dt(ts: pd.Timestamp) -> str:
    return ts.strftime("%d %b %Y, %H:%M")


# ---------------------------------------------------------------------------
# HTML building blocks
# ---------------------------------------------------------------------------
def html(markup: str) -> None:
    st.markdown(markup, unsafe_allow_html=True)


def section(title: str, sub: str = "") -> None:
    sub_html = f'<div class="section-sub">{sub}</div>' if sub else ""
    html(f'<div class="section-title">{title}</div>{sub_html}')


def page_header(title: str, sub: str) -> None:
    html(f'<div class="page-title">{title}</div><div class="page-sub">{sub}</div>')


def kpi_card(label: str, value: str, unit: str = "", accent: str = "") -> str:
    unit_html = f'<span class="kpi-unit">{unit}</span>' if unit else ""
    cls = f"card kpi kpi-{accent}" if accent else "card kpi"
    return (
        f'<div class="{cls}"><div class="kpi-label">{label}</div>'
        f'<div class="kpi-value">{value}{unit_html}</div></div>'
    )


def info_card(label: str, value: str, note: str = "") -> str:
    note_html = f'<div class="info-note">{note}</div>' if note else ""
    return (
        f'<div class="card"><div class="info-label">{label}</div>'
        f'<div class="info-value">{value}</div>{note_html}</div>'
    )


def tag_group_card(title: str, items) -> str:
    tags = "".join(f'<span class="tag">{item}</span>' for item in items)
    return f'<div class="card"><div class="card-title">{title}</div>{tags}</div>'


# ---------------------------------------------------------------------------
# Chart helpers
# ---------------------------------------------------------------------------
def style_figure(fig: go.Figure, title: str, height: int, x_title: str, y_title: str) -> go.Figure:
    fig.update_layout(
        title=dict(text=title, x=0.02, xanchor="left", font=dict(size=16, color=TEXT_PRIMARY)),
        height=height,
        margin=dict(l=24, r=24, t=64, b=24),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family=FONT, color=TEXT_MUTED, size=12),
        hoverlabel=dict(
            bgcolor=PANEL_2,
            bordercolor=BORDER,
            font=dict(family=FONT, color=TEXT_PRIMARY, size=13),
        ),
        showlegend=False,
    )
    fig.update_xaxes(
        title_text=x_title, showgrid=True, gridcolor=GRID, zeroline=False,
        linecolor=BORDER, ticks="outside", tickcolor=BORDER,
    )
    fig.update_yaxes(
        title_text=y_title, showgrid=True, gridcolor=GRID, zeroline=False,
        linecolor=BORDER, tickformat=",",
    )
    return fig


def main_forecast_chart(df: pd.DataFrame, s: ForecastStats) -> go.Figure:
    pad = max((s.peak - s.low) * 0.08, 1.0)
    floor = s.low - pad
    custom = pd.DataFrame(
        {"d": df["Datetime"].dt.strftime("%d %b %Y"), "t": df["Datetime"].dt.strftime("%H:%M")}
    ).values

    fig = go.Figure()
    # Invisible baseline so the area fill starts at the axis floor, not at zero
    fig.add_trace(go.Scatter(
        x=df["Datetime"], y=[floor] * len(df), mode="lines",
        line=dict(width=0), hoverinfo="skip", showlegend=False,
    ))
    fig.add_trace(go.Scatter(
        x=df["Datetime"], y=df["Forecast_MW"], mode="lines", name="Forecast",
        line=dict(color=ACCENT, width=2.2, shape="spline", smoothing=0.5),
        fill="tonexty", fillcolor="rgba(56, 189, 248, 0.09)",
        customdata=custom,
        hovertemplate=(
            "<b>Date:</b> %{customdata[0]}<br>"
            "<b>Time:</b> %{customdata[1]}<br>"
            "<b>Forecast Demand:</b> %{y:,.0f} MW<extra></extra>"
        ),
    ))
    fig.add_trace(go.Scatter(
        x=[s.peak_time], y=[s.peak], mode="markers", name="Peak",
        marker=dict(color=AMBER, size=10, line=dict(color=PANEL, width=2)),
        hovertemplate=f"<b>Peak demand</b><br>{fmt_dt(s.peak_time)}<br>{s.peak:,.0f} MW<extra></extra>",
    ))
    fig.add_trace(go.Scatter(
        x=[s.low_time], y=[s.low], mode="markers", name="Minimum",
        marker=dict(color=MINT, size=10, line=dict(color=PANEL, width=2)),
        hovertemplate=f"<b>Minimum demand</b><br>{fmt_dt(s.low_time)}<br>{s.low:,.0f} MW<extra></extra>",
    ))
    style_figure(fig, "30-Day Hourly Electricity Demand Forecast", 560, "Datetime", "Electricity Demand (MW)")
    fig.update_layout(
        hovermode="x",
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    )
    fig.update_xaxes(showgrid=False, showspikes=True, spikecolor=BORDER, spikethickness=1, spikedash="dot")
    fig.update_yaxes(range=[floor, s.peak + pad])
    return fig


def hourly_chart(hourly: pd.DataFrame) -> go.Figure:
    labels = [f"{h:02d}:00" for h in hourly["hour"]]
    fig = go.Figure(go.Scatter(
        x=hourly["hour"], y=hourly["avg"], mode="lines+markers",
        line=dict(color=ACCENT, width=2.4, shape="spline", smoothing=0.6),
        marker=dict(size=6, color=ACCENT, line=dict(color=PANEL, width=1.5)),
        customdata=labels,
        hovertemplate="<b>%{customdata}</b><br>Avg forecast: %{y:,.0f} MW<extra></extra>",
    ))
    style_figure(fig, "Hourly Demand Pattern", 340, "Hour of Day", "Average Demand (MW)")
    fig.update_xaxes(tickmode="array", tickvals=list(range(0, 24, 3)),
                     ticktext=[f"{h:02d}:00" for h in range(0, 24, 3)])
    return fig


def daily_chart(daily: pd.DataFrame) -> go.Figure:
    fig = go.Figure(go.Scatter(
        x=daily["day"], y=daily["avg"], mode="lines+markers",
        line=dict(color=ACCENT, width=2.4),
        marker=dict(size=6, color=ACCENT, line=dict(color=PANEL, width=1.5)),
        hovertemplate="<b>%{x|%a, %d %b %Y}</b><br>Avg forecast: %{y:,.0f} MW<extra></extra>",
    ))
    style_figure(fig, "Daily Demand Pattern", 340, "Date", "Average Demand (MW)")
    fig.update_xaxes(tickformat="%d %b")
    return fig


def distribution_chart(df: pd.DataFrame, s: ForecastStats) -> go.Figure:
    fig = go.Figure(go.Histogram(
        x=df["Forecast_MW"], nbinsx=30,
        marker=dict(color=ACCENT, line=dict(color=PANEL, width=1)), opacity=0.9,
        hovertemplate="Demand: %{x:,.0f} MW<br>Hours: %{y}<extra></extra>",
    ))
    fig.add_vline(
        x=s.avg, line_dash="dash", line_color=AMBER, line_width=1.5,
        annotation_text=f"Mean {s.avg:,.0f} MW", annotation_position="top right",
        annotation_font=dict(color=AMBER, size=12),
    )
    style_figure(fig, "Forecast Distribution", 340, "Forecast Demand (MW)", "Number of Hours")
    fig.update_layout(bargap=0.04)
    return fig


# ---------------------------------------------------------------------------
# Pages
# ---------------------------------------------------------------------------
def render_overview(df: pd.DataFrame, s: ForecastStats) -> None:
    badges = "".join(
        f'<span class="badge">{b}</span>'
        for b in (MODEL_NAME, f"{s.n} Hour Forecast", "Production Model")
    )
    html(
        '<div class="hero">'
        '<div class="hero-title">⚡ PJM ENERGY CONSUMPTION FORECASTING</div>'
        '<div class="hero-sub">30-Day Hourly Electricity Demand Forecast</div>'
        f'<div class="badge-row">{badges}</div>'
        '<div class="hero-desc">Machine learning based forecasting of hourly electricity demand '
        'using historical consumption patterns and engineered temporal features.</div>'
        "</div>"
    )

    cols = st.columns(5, gap="medium")
    cards = [
        kpi_card("Average Demand", f"{s.avg:,.0f}", "MW", "accent"),
        kpi_card("Peak Demand", f"{s.peak:,.0f}", "MW", "amber"),
        kpi_card("Minimum Demand", f"{s.low:,.0f}", "MW", "mint"),
        kpi_card("Forecast Horizon", f"{s.days}", "Days"),
        kpi_card("Total Predictions", f"{s.n:,}", "Hours"),
    ]
    for col, card in zip(cols, cards):
        col.markdown(card, unsafe_allow_html=True)

    html('<div style="height:1.25rem"></div>')
    st.plotly_chart(main_forecast_chart(df, s), config=PLOT_CONFIG)

    section("Forecast Period")
    cols = st.columns(4, gap="medium")
    period_cards = [
        info_card("Forecast Start", fmt_dt(s.start)),
        info_card("Forecast End", fmt_dt(s.end)),
        info_card("Forecast Frequency", s.frequency),
        info_card("Total Forecast Points", f"{s.n:,}"),
    ]
    for col, card in zip(cols, period_cards):
        col.markdown(card, unsafe_allow_html=True)


def render_analysis(df: pd.DataFrame, s: ForecastStats) -> None:
    page_header(
        "Forecast Analysis",
        "How predicted demand varies across hours, days and demand levels.",
    )

    hourly = (
        df.groupby(df["Datetime"].dt.hour)["Forecast_MW"].mean()
        .rename("avg").rename_axis("hour").reset_index()
    )
    # Hour-ending convention: a 00:00 reading closes the previous day, so the
    # forecast window splits into complete 24-hour days.
    day_key = (df["Datetime"] - pd.Timedelta(hours=1)).dt.normalize()
    daily = (
        df.groupby(day_key)["Forecast_MW"].mean()
        .rename("avg").rename_axis("day").reset_index()
    )

    section("Demand Pattern Analysis")
    c1, c2 = st.columns(2, gap="medium")
    c1.plotly_chart(hourly_chart(hourly), config=PLOT_CONFIG)
    c2.plotly_chart(daily_chart(daily), config=PLOT_CONFIG)

    html('<div style="height:1rem"></div>')
    c3, c4 = st.columns(2, gap="medium")
    c3.plotly_chart(distribution_chart(df, s), config=PLOT_CONFIG)

    busy_h = hourly.loc[hourly["avg"].idxmax()]
    quiet_h = hourly.loc[hourly["avg"].idxmin()]
    busy_d = daily.loc[daily["avg"].idxmax()]
    quiet_d = daily.loc[daily["avg"].idxmin()]
    observations = [
        f"Demand is highest around <b>{int(busy_h['hour']):02d}:00</b>, averaging {busy_h['avg']:,.0f} MW.",
        f"Demand is lowest around <b>{int(quiet_h['hour']):02d}:00</b>, averaging {quiet_h['avg']:,.0f} MW.",
        f"The busiest day is <b>{busy_d['day']:%d %b}</b> at {busy_d['avg']:,.0f} MW on average.",
        f"The quietest day is <b>{quiet_d['day']:%d %b}</b> at {quiet_d['avg']:,.0f} MW on average.",
    ]
    items = "".join(f"<li>{o}</li>" for o in observations)
    c4.markdown(
        f'<div class="card card-tall"><div class="card-title">Key observations</div>'
        f'<ul class="obs">{items}</ul></div>',
        unsafe_allow_html=True,
    )

    section("Peak Demand Analysis")
    cols = st.columns(5, gap="medium")
    peak_cards = [
        kpi_card("Peak Demand", f"{s.peak:,.0f}", "MW", "amber"),
        info_card("Peak Date & Time", fmt_dt(s.peak_time)),
        kpi_card("Minimum Demand", f"{s.low:,.0f}", "MW", "mint"),
        info_card("Minimum Date & Time", fmt_dt(s.low_time)),
        kpi_card("Demand Range", f"{s.spread:,.0f}", "MW", "accent"),
    ]
    for col, card in zip(cols, peak_cards):
        col.markdown(card, unsafe_allow_html=True)


def render_data(df: pd.DataFrame, s: ForecastStats) -> None:
    page_header(
        "Forecast Data",
        f"All {s.n:,} hourly predictions from {fmt_dt(s.start)} to {fmt_dt(s.end)}.",
    )

    labels = df["Datetime"].dt.strftime("%d %b %Y, %H:%M")
    mw_text = df["Forecast_MW"].map("{:,.2f}".format)

    with st.expander(f"View {s.n}-Hour Forecast", expanded=True):
        c1, c2, c3 = st.columns([2.2, 1, 1], gap="medium")
        query = c1.text_input("Search", placeholder="Filter by date, time or MW value, e.g. 10 Aug or 14:00")
        page_size = c2.selectbox("Rows per page", [24, 48, 120], index=0)

        if query.strip():
            q = query.strip()
            mask = labels.str.contains(q, case=False, regex=False) | mw_text.str.contains(q, regex=False)
        else:
            mask = pd.Series(True, index=df.index)

        matches = int(mask.sum())
        if matches == 0:
            st.info("No forecast rows match this search.")
        else:
            pages = math.ceil(matches / page_size)
            page = c3.selectbox("Page", list(range(1, pages + 1)), format_func=lambda p: f"{p} of {pages}")
            first = (page - 1) * page_size
            view_labels = labels[mask].iloc[first:first + page_size]
            view_mw = mw_text[mask].iloc[first:first + page_size]

            rows = "".join(f"<tr><td>{d}</td><td>{m}</td></tr>" for d, m in zip(view_labels, view_mw))
            html(
                '<div class="table-wrap"><table class="fc-table">'
                "<thead><tr><th>Datetime</th><th>Forecast (MW)</th></tr></thead>"
                f"<tbody>{rows}</tbody></table></div>"
                f'<div class="table-caption">Showing rows {first + 1}-{first + len(view_labels)} '
                f"of {matches:,}</div>"
            )

    section("Download Forecast", "Files contain the Datetime and Forecast_MW columns for all predictions.")
    d1, d2, _ = st.columns([1, 1, 2], gap="medium")
    d1.download_button(
        "Download CSV", data=to_csv_bytes(df),
        file_name="PJM_30_Day_Forecast_XGBoost.csv", mime="text/csv",
    )
    d2.download_button(
        "Download Excel", data=to_excel_bytes(df),
        file_name="PJM_30_Day_Forecast_XGBoost.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )


def render_model_info() -> None:
    page_header("Model Information", "The production model behind the forecast and the features it uses.")

    section("Final Model Performance", "Selected production model: XGBoost")
    cols = st.columns(3, gap="medium")
    for col, (name, value, unit, note) in zip(cols, MODEL_METRICS):
        col.markdown(
            f'<div class="card kpi kpi-accent"><div class="kpi-label">{name}</div>'
            f'<div class="kpi-value">{value}<span class="kpi-unit">{unit}</span></div>'
            f'<div class="info-note">{note}</div></div>',
            unsafe_allow_html=True,
        )
    html('<div style="height:0.9rem"></div>')
    html(
        '<div class="card"><div class="card-text">XGBoost was selected as the final forecasting model '
        "after evaluating the engineered time-series features on a chronological test set.</div></div>"
    )

    section("Forecasting Features")
    cols = st.columns(4, gap="medium")
    for col, (title, items) in zip(cols, FEATURE_GROUPS.items()):
        col.markdown(tag_group_card(title, items), unsafe_allow_html=True)

    section("About This Project")
    about_tags = "".join(
        f'<span class="tag">{t}</span>'
        for t in (
            "Historical hourly consumption", "Time-based feature engineering", "Lag features",
            "Rolling statistics", "XGBoost", "30-day recursive forecasting",
        )
    )
    html(
        '<div class="card"><div class="card-text">This project forecasts hourly PJM electricity demand '
        "using machine learning and historical temporal patterns. Engineered calendar, lag and rolling "
        "features feed an XGBoost model, and the 30-day forecast is produced recursively, one hour at a "
        f'time.</div><div style="margin-top:0.8rem">{about_tags}</div></div>'
    )


def render_footer() -> None:
    html(
        '<div class="site-footer"><b>PJM Energy Consumption Forecasting</b><br>'
        "Built with: Python • Pandas • XGBoost • Plotly • Streamlit</div>"
    )


# ---------------------------------------------------------------------------
# App
# ---------------------------------------------------------------------------
forecast_path = find_forecast_file()
if forecast_path is None:
    st.error(
        f"**Forecast file not found:** `{FORECAST_FILE}`\n\n"
        "Place this file in the same folder as `streamlit_app.py` and restart the app."
    )
    st.stop()

try:
    forecast_df = load_forecast(str(forecast_path))
except ValueError as exc:
    st.error(
        f"**Unexpected file format in `{FORECAST_FILE}`.** "
        f"The file must contain the columns `Datetime` and `Forecast_MW`. {exc}"
    )
    st.stop()
except Exception as exc:
    st.error(f"**Could not read `{FORECAST_FILE}`.** Details: {exc}")
    st.stop()

if forecast_df.empty:
    st.error(f"`{FORECAST_FILE}` does not contain any forecast rows.")
    st.stop()

stats = compute_stats(forecast_df)

with st.sidebar:
    html(
        '<div class="side-brand">⚡ PJM ENERGY FORECAST'
        '<div class="side-brand-sub">Electricity demand analytics</div></div>'
    )
    page = st.radio("Navigation", PAGES, label_visibility="collapsed")
    status_rows = [
        ("Model", MODEL_NAME),
        ("Forecast Horizon", f"{stats.days} Days"),
        ("Predictions", f"{stats.n:,} Hours"),
        ("Status", '<span class="status-dot"></span>Production Forecast'),
    ]
    rows_html = "".join(
        f'<div class="side-label">{label}</div><div class="side-value">{value}</div>'
        for label, value in status_rows
    )
    html(f'<div class="side-status">{rows_html}</div>')

if page == "Overview":
    render_overview(forecast_df, stats)
elif page == "Forecast Analysis":
    render_analysis(forecast_df, stats)
elif page == "Forecast Data":
    render_data(forecast_df, stats)
else:
    render_model_info()

render_footer()