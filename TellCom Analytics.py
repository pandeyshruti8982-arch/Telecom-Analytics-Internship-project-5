
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


# Professional dashboard color palette
CHART_COLORS = [
    "#2F80ED",  # blue
    "#27AE60",  # green
    "#F2994A",  # orange
    "#9B51E0",  # purple
    "#EB5757",  # red
    "#00A8A8",  # teal
    "#F2C94C",  # yellow
    "#56CCF2",  # sky
    "#BB6BD9",  # violet
    "#6FCF97",  # light green
]

# ============================================================
# TELCO CUSTOMER ANALYTICS — PROJECT 5
# Single-page Streamlit dashboard
#
# IMPORTANT:
# All displayed analytical values below were taken from the
# submitted Task 1–4 Jupyter notebooks. No analytical values
# are fabricated in this dashboard.
# ============================================================

st.set_page_config(
    page_title="TellCo Customer Analytics",
    page_icon="📡",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ---------------------------
# Theme / CSS
# ---------------------------
st.markdown("""
<style>
    .stApp {
        background: #f5f8fc;
    }
    .block-container {
        max-width: 1450px;
        padding-top: 1.2rem;
        padding-bottom: 2rem;
    }
    .hero {
        background: linear-gradient(110deg, #102a43 0%, #174a7e 55%, #1e6aa8 100%);
        padding: 28px 34px;
        border-radius: 18px;
        color: white;
        margin-bottom: 22px;
        box-shadow: 0 8px 25px rgba(16,42,67,.14);
    }
    .hero h1 {
        margin: 0;
        font-size: 2.35rem;
        font-weight: 750;
        letter-spacing: .2px;
    }
    .hero p {
        margin: 7px 0 0;
        font-size: 1.02rem;
        opacity: .90;
    }
    .section-title {
        font-size: 1.55rem;
        font-weight: 750;
        color: #102a43;
        margin: 24px 0 10px;
    }
    .section-subtitle {
        color: #52606d;
        margin-bottom: 12px;
    }
    .kpi {
        background: white;
        border: 1px solid #e3eaf2;
        border-radius: 14px;
        padding: 17px 18px;
        min-height: 105px;
        overflow: visible;
        box-shadow: 0 4px 15px rgba(16,42,67,.06);
    }
    .kpi-label {
        color: #66788a;
        font-size: .83rem;
        font-weight: 650;
        text-transform: uppercase;
        letter-spacing: .35px;
    }
    .kpi-value {
        color: #102a43;
        font-size: 1.75rem;
        font-weight: 800;
        margin-top: 7px;
    }
    .note {
        background: #eef6ff;
        border-left: 5px solid #2b78c5;
        border-radius: 10px;
        padding: 12px 15px;
        color: #30475e;
        margin: 8px 0 18px;
    }
    .source {
        color: #6b7785;
        font-size: .78rem;
        margin-top: 4px;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------
# Display helpers
# ---------------------------
def format_bytes(value):
    if value >= 1e12:
        return f"{value / 1e12:.3f}T"
    if value >= 1e9:
        return f"{value / 1e9:.3f}G"
    if value >= 1e6:
        return f"{value / 1e6:.3f}M"
    if value >= 1e3:
        return f"{value / 1e3:.3f}K"
    return f"{value:,.0f}"


def apply_chart_layout(fig, height=410, right=95, bottom=55):
    fig.update_layout(
        height=height,
        margin=dict(l=20, r=right, t=60, b=bottom),
        paper_bgcolor="white",
        plot_bgcolor="white",
        hoverlabel=dict(namelength=-1),
    )
    fig.update_xaxes(automargin=True)
    fig.update_yaxes(automargin=True)
    return fig

# ---------------------------
# Exact notebook-derived data
# ---------------------------

# Task 1 — raw / cleaned overview
raw_records = 150_001
raw_variables = 55
usable_sessions = 148_935
customers = 106_856

# Task 1 — application totals from notebook
app_usage = pd.DataFrame({
    "Application": ["Gaming", "Other", "YouTube", "Netflix", "Google", "Email", "Social Media"],
    "Total_Data_Bytes": [
        6.408892e13, 6.395425e13, 3.372204e12, 3.370060e12,
        1.162853e12, 3.364677e11, 2.722655e11
    ]
})

# Task 1 — application correlation with total traffic
app_corr = pd.DataFrame({
    "Application": ["Gaming", "Netflix", "YouTube", "Google", "Social Media", "Email", "Other"],
    "Correlation": [0.998263, 0.034583, 0.034577, 0.013359, 0.005707, 0.003912, -0.002562]
})

# Task 1 — top handset manufacturers
manufacturers = pd.DataFrame({
    "Handset Manufacturer": ["Apple", "Samsung", "Huawei"],
    "Usage Count": [59464, 40579, 34366]
})

# Task 1 — top handsets
handsets = pd.DataFrame({
    "Handset Type": [
        "Huawei B528S-23A",
        "Apple iPhone 6S (A1688)",
        "Apple iPhone 6 (A1586)",
        "Apple iPhone 7 (A1778)",
        "Apple iPhone Se (A1723)",
        "Apple iPhone 8 (A1905)",
        "Apple iPhone Xr (A2105)",
        "Samsung Galaxy S8 (Sm-G950F)",
        "Apple iPhone X (A1901)",
        "Samsung Galaxy A5 Sm-A520F",
    ],
    "Usage Count": [19727, 9413, 9012, 6304, 5176, 4985, 4562, 4480, 3810, 3708]
})

# Task 1 — PCA explained variance
pca = pd.DataFrame({
    "Principal Component": ["PC1","PC2","PC3","PC4","PC5","PC6","PC7"],
    "Explained Variance (%)": [70.735526, 5.912166, 5.822164, 5.241703, 4.467555, 4.086381, 3.734504],
    "Cumulative Variance (%)": [70.735526, 76.647692, 82.469856, 87.711560, 92.179115, 96.265496, 100.000000]
})

# Task 2 — engagement clusters
engagement_clusters = pd.DataFrame({
    "Engagement Level": ["High Engagement", "Low Engagement", "Medium Engagement"],
    "Customers": [4409, 79971, 22476],
    "Mean Sessions": [4.182581, 1.029136, 2.144198],
    "Mean Duration (ms)": [447436.128002, 94069.198869, 194410.893921],
    "Mean Traffic (bytes)": [2.161402e9, 4.977669e8, 1.089901e9],
})

# Task 2 — elbow values
elbow = pd.DataFrame({
    "K": list(range(2, 11)),
    "Inertia": [
        159909.049419, 105612.856625, 90316.482919,
        75914.056411, 66443.472278, 56975.902779,
        49887.606215, 45263.407844, 41711.349084
    ]
})

# Task 2 — top three applications
top_apps = pd.DataFrame({
    "Application": ["Gaming", "Other", "YouTube"],
    "Total Data (bytes)": [6.408892e13, 6.395425e13, 3.372204e12]
})

# Task 3 — experience clusters
experience_clusters = pd.DataFrame({
    "Experience Cluster": ["Cluster 0", "Cluster 1", "Cluster 2"],
    "Customers": [43998, 35909, 26949],
    "Mean TCP Retransmission (bytes)": [2.037487e7, 3.895633e6, 2.023900e7],
    "Mean RTT (ms)": [21.611608, 41.075753, 64.133368],
    "Mean Throughput (kbps)": [778.722044, 9375.239526, 1264.824759],
})

# Task 4 — satisfaction profile
satisfaction_profile = {
    "Mean": 1.601100,
    "Median": 1.531538,
    "75th Percentile": 1.954544,
    "Minimum": 0.127244,
    "Maximum": 16.814416,
}

# Task 4 — top 10 satisfaction scores
top_satisfaction = pd.DataFrame({
    "Rank": list(range(1, 11)),
    "Customer": [
        "33626320676","33614892860","33625779332","33659725664","33675877202",
        "33760536639","33664712899","33659359429","33667163239","33760413819"
    ],
    "Satisfaction Score": [
        16.814416, 16.756578, 16.556933, 16.419202, 15.463114,
        14.901734, 12.834937, 12.581322, 12.549648, 12.545818
    ]
})

# Task 4 — satisfaction clusters
satisfaction_clusters = pd.DataFrame({
    "Satisfaction Cluster": ["Cluster 0", "Cluster 1"],
    "Customers": [37238, 69618],
    "Mean Satisfaction": [1.3549, 1.7328],
    "Mean Experience": [0.8731, 2.5482],
})

# ---------------------------
# Header
# ---------------------------
st.markdown("""
<div class="hero">
    <h1>📡 TELCO CUSTOMER ANALYTICS</h1>
    <p>End-to-End Telecom Analytics</p>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="note">
<b>Data integrity:</b> The dashboard reproduces analytical values reported in the submitted
Task 1–4 notebooks. Satisfaction is a project-derived analytical index, not a direct survey score.
</div>
""", unsafe_allow_html=True)

# ---------------------------
# Executive overview
# ---------------------------
st.markdown('<div class="section-title">Executive Overview</div>', unsafe_allow_html=True)

cols = st.columns(4)
kpis = [
    ("Raw Records", f"{raw_records:,}"),
    ("Raw Variables", f"{raw_variables:,}"),
    ("Usable Sessions", f"{usable_sessions:,}"),
    ("Customers", f"{customers:,}"),
]
for col, (label, value) in zip(cols, kpis):
    with col:
        st.markdown(f"""
        <div class="kpi">
            <div class="kpi-label">{label}</div>
            <div class="kpi-value">{value}</div>
        </div>
        """, unsafe_allow_html=True)

# ---------------------------
# TASK 1
# ---------------------------
st.markdown('<div class="section-title">Task 1 — User Overview & Data Quality</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="section-subtitle">Raw telecom xDR data, application usage, handset profile and PCA summary.</div>',
    unsafe_allow_html=True
)

c1, c2 = st.columns(2)

with c1:
    plot_df = app_usage.sort_values("Total_Data_Bytes").copy()
    plot_df["Display"] = plot_df["Total_Data_Bytes"].map(format_bytes)
    fig = px.bar(
        plot_df,
        x="Total_Data_Bytes",
        y="Application",
        orientation="h",
        title="Application-wise Total Data Usage",
        labels={"Total_Data_Bytes": "Total Data (bytes)", "Application": ""},
        text="Display",
        custom_data=["Total_Data_Bytes"],
    )
    fig.update_traces(
        textposition="outside", cliponaxis=False,
        marker_color=CHART_COLORS[:len(plot_df)],
        hovertemplate="%{y}: %{customdata[0]:,.0f} bytes<extra></extra>"
    )
    apply_chart_layout(fig, 410, 120)
    st.plotly_chart(fig, use_container_width=True)

with c2:
    fig = px.bar(
        manufacturers.sort_values("Usage Count"),
        x="Usage Count",
        y="Handset Manufacturer",
        orientation="h",
        title="Top Handset Manufacturers",
        text="Usage Count",
    )
    fig.update_traces(texttemplate="%{text:,}", textposition="outside", cliponaxis=False,
                      marker_color=CHART_COLORS[:len(manufacturers)])
    apply_chart_layout(fig, 410, 95)
    st.plotly_chart(fig, use_container_width=True)

c3, c4 = st.columns(2)

with c3:
    fig = px.bar(
        handsets.sort_values("Usage Count"),
        x="Usage Count",
        y="Handset Type",
        orientation="h",
        title="Top 10 Handset Types",
        text="Usage Count",
    )
    fig.update_traces(texttemplate="%{text:,}", textposition="outside", cliponaxis=False,
                      marker_color=CHART_COLORS[:len(handsets)])
    apply_chart_layout(fig, 470, 100)
    st.plotly_chart(fig, use_container_width=True)

with c4:
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=pca["Principal Component"],
        y=pca["Cumulative Variance (%)"],
        mode="lines+markers+text",
        text=[f"{v:.1f}%" for v in pca["Cumulative Variance (%)"]],
        textposition="top center",
        name="Cumulative variance",
        line=dict(color="#9B51E0", width=3),
        marker=dict(color="#2F80ED", size=8),
    ))
    fig.update_layout(
        title="PCA Cumulative Explained Variance",
        xaxis_title="Principal Component",
        yaxis_title="Cumulative Variance (%)",
        yaxis=dict(range=[0, 105]),
        height=470,
        margin=dict(l=20,r=35,t=60,b=55),
    )
    st.plotly_chart(fig, use_container_width=True)

# ---------------------------
# TASK 2
# ---------------------------
st.markdown('<div class="section-title">Task 2 — User Engagement</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="section-subtitle">Engagement is measured using session frequency, total session duration and total network traffic.</div>',
    unsafe_allow_html=True
)

c1, c2 = st.columns(2)

with c1:
    fig = px.bar(
        engagement_clusters.sort_values("Customers"),
        x="Customers",
        y="Engagement Level",
        orientation="h",
        title="Customer Count by Engagement Level",
        text="Customers",
    )
    fig.update_traces(texttemplate="%{text:,}", textposition="outside", cliponaxis=False,
                      marker_color=CHART_COLORS[:len(engagement_clusters)])
    apply_chart_layout(fig, 410, 100)
    st.plotly_chart(fig, use_container_width=True)

with c2:
    fig = px.line(
        elbow,
        x="K",
        y="Inertia",
        markers=True,
        title="Elbow Method — Engagement Clustering",
        labels={"K": "Number of Clusters (K)", "Inertia": "Inertia"},
    )
    fig.add_vline(x=3, line_dash="dash", annotation_text="Selected K = 3", annotation_position="top right")
    fig.update_traces(line=dict(color="#F2994A", width=3), marker=dict(color="#2F80ED", size=9))
    fig.update_layout(height=410, margin=dict(l=20,r=55,t=75,b=55))
    st.plotly_chart(fig, use_container_width=True)

c1, c2 = st.columns(2)

with c1:
    plot_df = top_apps.sort_values("Total Data (bytes)").copy()
    plot_df["Display"] = plot_df["Total Data (bytes)"].map(format_bytes)
    fig = px.bar(
        plot_df,
        x="Total Data (bytes)",
        y="Application",
        orientation="h",
        title="Top 3 Most Used Applications",
        text="Display",
        custom_data=["Total Data (bytes)"],
    )
    fig.update_traces(
        textposition="outside", cliponaxis=False,
        marker_color=CHART_COLORS[:len(plot_df)],
        hovertemplate="%{y}: %{customdata[0]:,.0f} bytes<extra></extra>"
    )
    apply_chart_layout(fig, 380, 120)
    st.plotly_chart(fig, use_container_width=True)

with c2:
    # Cluster mean sessions — one common unit so the chart is directly comparable
    fig = px.bar(
        engagement_clusters,
        x="Engagement Level",
        y="Mean Sessions",
        text="Mean Sessions",
        title="Mean Session Frequency by Engagement Cluster",
    )
    fig.update_traces(texttemplate="%{text:.2f}", textposition="outside", cliponaxis=False,
                      marker_color=CHART_COLORS[:len(engagement_clusters)])
    apply_chart_layout(fig, 380, 75)
    st.plotly_chart(fig, use_container_width=True)

# ---------------------------
# TASK 3
# ---------------------------
st.markdown('<div class="section-title">Task 3 — User Experience / Network Quality</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="section-subtitle">Customer-level experience clustering using TCP retransmission, RTT and throughput.</div>',
    unsafe_allow_html=True
)

c1, c2 = st.columns(2)

with c1:
    fig = px.bar(
        experience_clusters,
        x="Experience Cluster",
        y="Customers",
        text="Customers",
        title="Customers by Experience Cluster",
    )
    fig.update_traces(texttemplate="%{text:,}", textposition="outside", cliponaxis=False,
                      marker_color=CHART_COLORS[:len(experience_clusters)])
    apply_chart_layout(fig, 400, 95)
    st.plotly_chart(fig, use_container_width=True)

with c2:
    fig = px.bar(
        experience_clusters,
        x="Experience Cluster",
        y="Mean Throughput (kbps)",
        text="Mean Throughput (kbps)",
        title="Mean Throughput by Experience Cluster",
    )
    fig.update_traces(texttemplate="%{text:.1f}", textposition="outside", cliponaxis=False,
                      marker_color=CHART_COLORS[:len(experience_clusters)])
    apply_chart_layout(fig, 400, 95)
    st.plotly_chart(fig, use_container_width=True)

c1, c2 = st.columns(2)

with c1:
    fig = px.bar(
        experience_clusters,
        x="Experience Cluster",
        y="Mean RTT (ms)",
        text="Mean RTT (ms)",
        title="Mean RTT by Experience Cluster",
    )
    fig.update_traces(texttemplate="%{text:.2f}", textposition="outside", cliponaxis=False,
                      marker_color=CHART_COLORS[:len(experience_clusters)])
    apply_chart_layout(fig, 380, 90)
    st.plotly_chart(fig, use_container_width=True)

with c2:
    fig = px.bar(
        experience_clusters,
        x="Experience Cluster",
        y="Mean TCP Retransmission (bytes)",
        text="Mean TCP Retransmission (bytes)",
        title="Mean TCP Retransmission by Experience Cluster",
    )
    fig.update_traces(texttemplate="%{text:.3s}", textposition="outside", cliponaxis=False,
                      marker_color=CHART_COLORS[:len(experience_clusters)])
    apply_chart_layout(fig, 380, 100)
    st.plotly_chart(fig, use_container_width=True)

# ---------------------------
# TASK 4
# ---------------------------
st.markdown('<div class="section-title">Task 4 — Customer Satisfaction</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="section-subtitle">Satisfaction Score = (Engagement Score + Experience Score) / 2.</div>',
    unsafe_allow_html=True
)

cols = st.columns(5)
for col, (label, value) in zip(cols, satisfaction_profile.items()):
    with col:
        st.markdown(f"""
        <div class="kpi">
            <div class="kpi-label">{label}</div>
            <div class="kpi-value">{value:.3f}</div>
        </div>
        """, unsafe_allow_html=True)

c1, c2 = st.columns(2)

with c1:
    fig = px.bar(
        top_satisfaction.sort_values("Satisfaction Score"),
        x="Satisfaction Score",
        y="Rank",
        orientation="h",
        text="Satisfaction Score",
        hover_data=["Customer"],
        title="Top 10 Customers by Satisfaction Score",
    )
    fig.update_traces(texttemplate="%{text:.3f}", textposition="outside", cliponaxis=False,
                      marker_color=CHART_COLORS[:len(top_satisfaction)])
    fig.update_layout(height=470, margin=dict(l=20,r=100,t=60,b=55), yaxis=dict(dtick=1, autorange="reversed"))
    st.plotly_chart(fig, use_container_width=True)

with c2:
    fig = px.bar(
        satisfaction_clusters,
        x="Satisfaction Cluster",
        y="Customers",
        text="Customers",
        title="Customers by Satisfaction Cluster",
    )
    fig.update_traces(texttemplate="%{text:,}", textposition="outside", cliponaxis=False,
                      marker_color=CHART_COLORS[:len(satisfaction_clusters)])
    apply_chart_layout(fig, 470, 110)
    st.plotly_chart(fig, use_container_width=True)

st.markdown("""
<div class="note">
<b>Interpretation note:</b> Satisfaction is a derived analytical index based on Engagement Score
and Experience Score. It should not be described as a direct customer survey satisfaction measure.
The notebook regression reports MSE = 0.0 and R² = 1.0 because the target is mathematically derived
from the same two predictor scores.
</div>
""", unsafe_allow_html=True)

# ---------------------------
# Footer
# ---------------------------
st.markdown(
    '<div class="source">Source: Submitted Project 5 Jupyter notebooks — Tasks 1–4. '
    'Dashboard designed as a single-page Streamlit presentation of notebook-derived results.</div>',
    unsafe_allow_html=True
)