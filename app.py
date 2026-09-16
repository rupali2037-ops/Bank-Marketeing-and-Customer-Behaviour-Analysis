

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="Bank Marketing & Customer Behaviour Analysis",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------
# Page styling
# -----------------------------
st.markdown("""
<style>
.main {background-color: #f7f9fc;}
[data-testid="stMetric"] {
    background: white;
    border: 1px solid #e6eaf0;
    padding: 16px;
    border-radius: 12px;
}
.block-container {padding-top: 1.5rem;}
</style>
""", unsafe_allow_html=True)

st.title("🏦 Bank Marketing & Customer Behaviour Analysis")
st.caption("Interactive Streamlit dashboard based on the analysis and graphs in the supplied Jupyter Notebook.")

# -----------------------------
# Data loading
# -----------------------------
@st.cache_data
def load_data(uploaded_file):
    df = pd.read_csv(uploaded_file)
    return df

def standardize_columns(df):
    # The notebook uses V1...V16 and Class.
    rename_map = {
        "V1":"Age",
        "V2":"Job",
        "V3":"Marital Status",
        "V4":"Education",
        "V5":"Default",
        "V6":"Average balance",
        "V7":"Housing loan",
        "V8":"Personal loan",
        "V9":"Contact",
        "V10":"Contact day",
        "V11":"Contact month",
        "V12":"Contact duration",
        "V13":"Campaign contacts",
        "V14":"Previous contact days",
        "V15":"Previous contacts",
        "V16":"Previous result"
    }
    existing = {k:v for k,v in rename_map.items() if k in df.columns}
    df = df.rename(columns=existing)

    # Support common target names if present.
    for target in ["Class", "class", "y", "Y", "Target", "target", "Subscribed", "subscription"]:
        if target in df.columns and "Class" not in df.columns:
            df = df.rename(columns={target:"Class"})
            break

    # Convert expected numeric columns where possible.
    numeric_cols = [
        "Age", "Average balance", "Contact day", "Contact duration",
        "Campaign contacts", "Previous contact days", "Previous contacts", "Class"
    ]
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    # Notebook's cleaning logic: replace unknown with missing, then fill categorical
    # values sensibly instead of overwriting every row.
    df = df.replace("unknown", np.nan)
    for col in df.select_dtypes(include="object").columns:
        if df[col].isna().any():
            mode = df[col].mode()
            df[col] = df[col].fillna(mode.iloc[0] if len(mode) else "Unknown")
    for col in df.select_dtypes(include=np.number).columns:
        df[col] = df[col].fillna(df[col].median())

    df = df.drop_duplicates().copy()

    if "Class" in df.columns:
        df["Subscription Status"] = df["Class"].map({
            1: "Subscribed",
            2: "Not Subscribed"
        }).fillna(df["Class"].astype(str))
    return df

uploaded = st.sidebar.file_uploader(
    "Upload Bank_Marketing.csv",
    type=["csv"],
    help="Upload the CSV used in the notebook."
)

if uploaded is None:
    st.info("Please upload the Bank_Marketing.csv file to open the dashboard.")
    st.markdown("""
### Expected dataset
The supplied notebook analyzes the Bank Marketing dataset with fields such as:
`Age`, `Job`, `Marital Status`, `Education`, `Default`, `Average balance`,
`Housing loan`, `Personal loan`, `Contact`, `Contact day`, `Contact month`,
`Contact duration`, `Campaign contacts`, `Previous contact days`,
`Previous contacts`, `Previous result`, and `Class`.
""")
    st.stop()

df = standardize_columns(load_data(uploaded))

required = ["Class", "Age", "Job", "Marital Status", "Education",
            "Average balance", "Housing loan", "Personal loan", "Contact",
            "Contact day", "Contact duration", "Campaign contacts",
            "Previous contacts", "Previous result"]
missing = [c for c in required if c not in df.columns]

if missing:
    st.error("The uploaded CSV is missing these columns: " + ", ".join(missing))
    st.write("Available columns:", list(df.columns))
    st.stop()

# -----------------------------
# Sidebar filters
# -----------------------------
st.sidebar.header("🔎 Dashboard Filters")

def options_for(col):
    return sorted(df[col].dropna().astype(str).unique().tolist())

age_min, age_max = int(df["Age"].min()), int(df["Age"].max())
age_range = st.sidebar.slider("Age", age_min, age_max, (age_min, age_max))

jobs = st.sidebar.multiselect("Job", options_for("Job"), default=options_for("Job"))
education = st.sidebar.multiselect("Education", options_for("Education"), default=options_for("Education"))
marital = st.sidebar.multiselect("Marital Status", options_for("Marital Status"), default=options_for("Marital Status"))
contact = st.sidebar.multiselect("Contact", options_for("Contact"), default=options_for("Contact"))
housing = st.sidebar.multiselect("Housing loan", options_for("Housing loan"), default=options_for("Housing loan"))
personal = st.sidebar.multiselect("Personal loan", options_for("Personal loan"), default=options_for("Personal loan"))
subscription = st.sidebar.multiselect(
    "Subscription Status",
    ["Subscribed", "Not Subscribed"],
    default=["Subscribed", "Not Subscribed"]
)

filtered = df[
    df["Age"].between(age_range[0], age_range[1]) &
    df["Job"].astype(str).isin(jobs) &
    df["Education"].astype(str).isin(education) &
    df["Marital Status"].astype(str).isin(marital) &
    df["Contact"].astype(str).isin(contact) &
    df["Housing loan"].astype(str).isin(housing) &
    df["Personal loan"].astype(str).isin(personal) &
    df["Subscription Status"].astype(str).isin(subscription)
].copy()

# -----------------------------
# Header KPIs
# -----------------------------
total = len(filtered)
subscribed = int((filtered["Class"] == 1).sum())
subscription_rate = (subscribed / total * 100) if total else 0
avg_age = filtered["Age"].mean() if total else 0
avg_balance = filtered["Average balance"].mean() if total else 0
avg_campaign = filtered["Campaign contacts"].mean() if total else 0
avg_duration = filtered["Contact duration"].mean() if total else 0

c1, c2, c3, c4, c5, c6 = st.columns(6)
c1.metric("Total Customers", f"{total:,}")
c2.metric("Subscribed", f"{subscribed:,}")
c3.metric("Subscription Rate", f"{subscription_rate:.2f}%")
c4.metric("Average Age", f"{avg_age:.1f}")
c5.metric("Avg. Balance", f"{avg_balance:,.0f}")
c6.metric("Avg. Call Duration", f"{avg_duration:,.0f}")

st.divider()

# -----------------------------
# Tabs
# -----------------------------
tabs = st.tabs([
    "📊 Overview",
    "👥 Customer Behaviour",
    "📞 Campaign Analysis",
    "💳 Loan & Default",
    "🎓 Demographics",
    "🔥 Correlation",
    "📋 Data"
])

dark_blue = "#0B3D91"
dark_red = "#8B0000"
dark_green = "#006400"
dark_pink = "#C2185B"

with tabs[0]:
    st.subheader("Conversion Overview")

    left, right = st.columns(2)

    with left:
        conv = filtered.groupby("Subscription Status").size().reset_index(name="Customer Count")
        fig = px.pie(
            conv, names="Subscription Status", values="Customer Count",
            hole=0.55, title="Conversion Rate Distribution",
            color="Subscription Status",
            color_discrete_map={"Subscribed":dark_blue, "Not Subscribed":dark_red}
        )
        fig.update_traces(textposition="inside", textinfo="percent+label")
        st.plotly_chart(fig, use_container_width=True)

    with right:
        kpi = pd.DataFrame({
            "Metric": ["Total Customers", "Average Age", "Average Balance", "Average Campaign Contacts"],
            "Value": [total, avg_age, avg_balance, avg_campaign]
        })
        fig = px.bar(kpi, x="Metric", y="Value", text="Value", title="Key Performance Indicators")
        fig.update_traces(texttemplate="%{text:.2f}", textposition="outside")
        st.plotly_chart(fig, use_container_width=True)

    st.subheader("Customer Age Distribution")
    fig = px.histogram(filtered, x="Age", nbins=30, title="Age Distribution of Customers")
    st.plotly_chart(fig, use_container_width=True)

with tabs[1]:
    st.subheader("Customer Behaviour Analysis")

    left, right = st.columns(2)
    with left:
        fig = px.histogram(
            filtered, x="Job", color="Subscription Status", barmode="group",
            title="Job Category vs Subscription",
            color_discrete_map={"Subscribed":dark_green, "Not Subscribed":dark_pink}
        )
        fig.update_layout(xaxis_tickangle=-35)
        st.plotly_chart(fig, use_container_width=True)

    with right:
        marital_subscription = filtered.groupby(
            ["Marital Status", "Subscription Status"]
        ).size().reset_index(name="Count")
        fig = px.bar(
            marital_subscription, x="Marital Status", y="Count",
            color="Subscription Status", barmode="group", text="Count",
            title="Marital Status vs Subscription",
            color_discrete_map={"Subscribed":dark_blue, "Not Subscribed":dark_red}
        )
        st.plotly_chart(fig, use_container_width=True)

    left, right = st.columns(2)
    with left:
        fig = px.box(
            filtered, x="Subscription Status", y="Age", color="Subscription Status",
            title="Age Distribution by Subscription Status",
            color_discrete_map={"Subscribed":dark_blue, "Not Subscribed":dark_red}
        )
        st.plotly_chart(fig, use_container_width=True)

    with right:
        fig = px.violin(
            filtered, x="Subscription Status", y="Age", color="Subscription Status",
            box=True, points="all", title="Age Distribution by Subscription Status",
            color_discrete_map={"Subscribed":dark_blue, "Not Subscribed":dark_red}
        )
        st.plotly_chart(fig, use_container_width=True)

    education_count = filtered.groupby("Education").size().reset_index(name="Count")
    fig = px.pie(
        education_count, names="Education", values="Count",
        hole=0.5, title="Customer Distribution by Education Level"
    )
    fig.update_traces(textposition="inside", textinfo="percent+label")
    st.plotly_chart(fig, use_container_width=True)

with tabs[2]:
    st.subheader("Marketing Campaign Analysis")

    left, right = st.columns(2)
    with left:
        fig = px.histogram(
            filtered, x="Contact duration", nbins=30,
            title="Contact Duration Distribution"
        )
        fig.update_layout(xaxis_title="Call Duration (Seconds)", yaxis_title="Number of Customers")
        st.plotly_chart(fig, use_container_width=True)

    with right:
        fig = px.box(
            filtered, x="Subscription Status", y="Contact duration",
            color="Subscription Status", title="Contact Duration vs Subscription",
            color_discrete_map={"Subscribed":dark_blue, "Not Subscribed":dark_red}
        )
        st.plotly_chart(fig, use_container_width=True)

    day_rate = (
        filtered.groupby("Contact day")["Class"]
        .apply(lambda x: (x == 1).mean() * 100)
        .reset_index(name="Subscription Rate")
        .sort_values("Contact day")
    )
    fig = px.line(
        day_rate, x="Contact day", y="Subscription Rate", markers=True,
        title="Subscription Rate by Day of Month"
    )
    st.plotly_chart(fig, use_container_width=True)

    month_rate = (
        filtered.groupby("Contact month")["Class"]
        .apply(lambda x: (x == 1).mean() * 100)
        .reset_index(name="Subscription Rate")
    )
    month_order = ["jan","feb","mar","apr","may","jun","jul","aug","sep","oct","nov","dec"]
    month_rate["order"] = month_rate["Contact month"].astype(str).str.lower().map(
        {m:i for i,m in enumerate(month_order)}
    )
    month_rate = month_rate.sort_values("order")
    fig = px.bar(
        month_rate, x="Contact month", y="Subscription Rate",
        text="Subscription Rate", title="Subscription Rate by Contact Month"
    )
    fig.update_traces(texttemplate="%{text:.2f}%", textposition="outside")
    st.plotly_chart(fig, use_container_width=True)

with tabs[3]:
    st.subheader("Loan & Default Analysis")

    left, right = st.columns(2)
    with left:
        housing_subscription = filtered.groupby(
            ["Housing loan", "Subscription Status"]
        ).size().reset_index(name="Count")
        fig = px.funnel(
            housing_subscription, x="Count", y="Housing loan",
            color="Subscription Status", title="Housing Loan vs Subscription",
            color_discrete_map={"Subscribed":dark_blue, "Not Subscribed":dark_red}
        )
        st.plotly_chart(fig, use_container_width=True)

    with right:
        personal_subscription = filtered.groupby(
            ["Personal loan", "Subscription Status"]
        ).size().reset_index(name="Count")
        fig = px.bar(
            personal_subscription, x="Personal loan", y="Count",
            color="Subscription Status", barmode="group",
            title="Personal Loan vs Subscription",
            color_discrete_map={"Subscribed":dark_green, "Not Subscribed":dark_red}
        )
        st.plotly_chart(fig, use_container_width=True)

    heatmap_data = pd.crosstab(filtered["Default"], filtered["Subscription Status"])
    fig = px.imshow(
        heatmap_data, text_auto=True, color_continuous_scale="Blues",
        title="Default Status vs Subscription Heatmap"
    )
    fig.update_layout(xaxis_title="Subscription Status", yaxis_title="Default Status")
    st.plotly_chart(fig, use_container_width=True)

with tabs[4]:
    st.subheader("Demographic & Previous Campaign Behaviour")

    left, right = st.columns(2)
    with left:
        pie_data = filtered.groupby("Previous result").size().reset_index(name="Count")
        fig = px.pie(
            pie_data, names="Previous result", values="Count",
            title="Customer Distribution by Previous Campaign Outcome",
            hole=0.45
        )
        fig.update_traces(textposition="inside", textinfo="percent+label")
        st.plotly_chart(fig, use_container_width=True)

    with right:
        heatmap_data = (
            filtered.groupby(["Subscription Status", "Previous contacts"])
            .size().reset_index(name="Count")
        )
        fig = px.density_heatmap(
            heatmap_data, x="Subscription Status", y="Previous contacts",
            z="Count", color_continuous_scale="Reds",
            title="Previous Contacts by Subscription Status"
        )
        st.plotly_chart(fig, use_container_width=True)

    # Contact method donut charts, matching the notebook's intent in a cleaner layout.
    contacts = filtered["Contact"].dropna().unique()
    cols = st.columns(max(1, min(len(contacts), 3)))
    for i, method in enumerate(contacts):
        data = filtered[filtered["Contact"] == method].groupby("Subscription Status").size().reset_index(name="Count")
        fig = px.pie(
            data, names="Subscription Status", values="Count", hole=0.55,
            title=f"{method} Contact",
            color="Subscription Status",
            color_discrete_map={"Subscribed":dark_blue, "Not Subscribed":dark_red}
        )
        fig.update_traces(textposition="inside", textinfo="percent+label")
        cols[i % len(cols)].plotly_chart(fig, use_container_width=True)

with tabs[5]:
    st.subheader("Correlation Heatmap")

    num_df = filtered.select_dtypes(include=["int64", "float64", "int32", "float32"])
    corr = num_df.corr()
    fig = px.imshow(
        corr, text_auto=".3f", color_continuous_scale="Blues",
        title="Correlation Heatmap of Numerical Features"
    )
    fig.update_layout(height=700)
    st.plotly_chart(fig, use_container_width=True)

with tabs[6]:
    st.subheader("Filtered Dataset")
    st.write(f"Showing **{len(filtered):,}** of **{len(df):,}** customers.")
    st.dataframe(filtered, use_container_width=True, height=500)

    csv = filtered.to_csv(index=False).encode("utf-8")
    st.download_button(
        "⬇️ Download Filtered CSV",
        data=csv,
        file_name="filtered_bank_marketing.csv",
        mime="text/csv"
    )

st.divider()
st.caption("Bank Marketing & Customer Behaviour Analysis • Streamlit dashboard")
