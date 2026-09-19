import streamlit as st
import pandas as pd
import plotly.express as px

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Bank Marketing Intelligence",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown("""
<style>

/* ---------- MAIN BACKGROUND ---------- */

.stApp {
    background:
        radial-gradient(circle at 80% 10%, rgba(0, 119, 255, 0.10), transparent 25%),
        radial-gradient(circle at 10% 90%, rgba(0, 220, 255, 0.06), transparent 25%),
        #050B16;
    color: white;
}

/* ---------- SIDEBAR ---------- */

section[data-testid="stSidebar"] {
    background:
        linear-gradient(180deg, #030711 0%, #071322 100%);
    border-right: 1px solid #16395D;
}

section[data-testid="stSidebar"] > div {
    padding-top: 25px;
}

/* ---------- SIDEBAR TITLE ---------- */

.sidebar-title {
    font-size: 22px;
    font-weight: 800;
    color: #E8F7FF;
    padding: 5px 5px 18px 5px;
    border-bottom: 1px solid #17344F;
    margin-bottom: 22px;
}

.sidebar-title span {
    color: #38BDF8;
}

/* ---------- FILTER CARD ---------- */

.filter-card {
    background: linear-gradient(
        145deg,
        rgba(14, 38, 63, 0.85),
        rgba(7, 19, 33, 0.90)
    );

    border: 1px solid #174B70;
    border-radius: 14px;

    padding: 13px 14px;
    margin-top: 10px;
    margin-bottom: 15px;

    box-shadow:
        0 8px 25px rgba(0,0,0,0.25),
        inset 0 0 15px rgba(56,189,248,0.025);
}

.filter-title {
    color: #8BD9FF;
    font-size: 13px;
    font-weight: 700;
    margin-bottom: 5px;
}

.filter-icon {
    color: #38BDF8;
    font-size: 16px;
}

/* ---------- RADIO MENU ---------- */

div[role="radiogroup"] label {
    background: rgba(11, 28, 47, 0.75);
    border: 1px solid #173B59;
    border-radius: 10px;
    padding: 10px 12px;
    margin-bottom: 7px;
    transition: 0.2s;
}

div[role="radiogroup"] label:hover {
    border-color: #38BDF8;
    background: rgba(20, 55, 82, 0.9);
}

/* ---------- SELECT BOX ---------- */

div[data-baseweb="select"] > div {
    background: #071525 !important;
    border: 1px solid #24577A !important;
    border-radius: 9px !important;
    color: white !important;
}

div[data-baseweb="select"]:hover > div {
    border-color: #38BDF8 !important;
}

/* ---------- REMOVE RED MULTISELECT LOOK ---------- */

span[data-baseweb="tag"] {
    background: #123B5A !important;
    border: 1px solid #2B7AA5 !important;
    color: #DDF6FF !important;
    border-radius: 7px !important;
}

span[data-baseweb="tag"] svg {
    color: #7DD3FC !important;
}

/* ---------- SLIDER ---------- */

div[data-testid="stSlider"] div[role="slider"] {
    background: #38BDF8 !important;
}

div[data-testid="stSlider"] [data-testid="stThumbValue"] {
    color: #7DD3FC !important;
}

/* ---------- KPI CARDS ---------- */

[data-testid="stMetric"] {
    background:
        linear-gradient(
            145deg,
            rgba(14, 43, 70, 0.95),
            rgba(7, 24, 41, 0.95)
        );

    border: 1px solid #1C5A85;
    border-radius: 16px;
    padding: 18px;

    box-shadow:
        0 10px 30px rgba(0,0,0,0.25);
}

[data-testid="stMetricValue"] {
    color: #6DD5FA;
    font-weight: 800;
}

[data-testid="stMetricLabel"] {
    color: #B8D4E6;
}

/* ---------- HEADINGS ---------- */

h1 {
    color: #F1F9FF;
    font-weight: 850;
}

h2 {
    color: #E4F4FF;
}

h3 {
    color: #BFEAFF;
}

/* ---------- CHART CONTAINER ---------- */

.chart-box {
    background:
        linear-gradient(
            145deg,
            rgba(8, 25, 43, 0.85),
            rgba(4, 14, 26, 0.9)
        );

    border: 1px solid #173D5B;
    border-radius: 16px;
    padding: 8px;
}

/* ---------- DIVIDER ---------- */

hr {
    border-color: #17344F !important;
}

/* ---------- BUTTON ---------- */

.stButton button {
    background: linear-gradient(90deg, #075985, #0284C7);
    color: white;
    border: none;
    border-radius: 9px;
    font-weight: 700;
}

.stButton button:hover {
    background: linear-gradient(90deg, #0284C7, #38BDF8);
}

/* ---------- DATAFRAME ---------- */

[data-testid="stDataFrame"] {
    border: 1px solid #173D5B;
    border-radius: 12px;
}

/* ---------- FOOTER ---------- */

.footer {
    text-align: center;
    color: #6F91A8;
    font-size: 13px;
    padding: 25px;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# LOAD DATA
# =========================================================

@st.cache_data
def load_data():

    df = pd.read_csv("Bank_Marketing.csv")

    rename_map = {
        "V1": "Age",
        "V2": "Job",
        "V3": "Marital Status",
        "V4": "Education",
        "V5": "Default",
        "V6": "Average balance",
        "V7": "Housing loan",
        "V8": "Personal loan",
        "V9": "Contact",
        "V10": "Contact day",
        "V11": "Contact month",
        "V12": "Contact duration",
        "V13": "Campaign contacts",
        "V14": "Previous contacts",
        "V15": "Previous days",
        "V16": "Previous result"
    }

    df = df.rename(columns=rename_map)

    if "Class" in df.columns:
        df["Subscription Status"] = df["Class"].map({
            1: "Subscribed",
            2: "Not Subscribed"
        })

    return df.drop_duplicates()


df = load_data()


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.markdown(
        '<div class="sidebar-title">🏦 BANK <span>ANALYTICS</span></div>',
        unsafe_allow_html=True
    )

    st.markdown("### 📊 Select Dashboard")

    menu = st.radio(
        "Dashboard",
        [
            "🏠 Executive Dashboard",
            "👥 Customer Insights",
            "📢 Campaign Analytics",
            "🔎 Data Explorer"
        ],
        label_visibility="collapsed"
    )

    st.markdown("---")

    st.markdown("### 🎛️ Smart Filters")

    # =====================================================
    # JOB FILTER
    # =====================================================

    st.markdown("""
    <div class="filter-card">
        <div class="filter-title">
            💼 JOB CATEGORY
        </div>
    </div>
    """, unsafe_allow_html=True)

    job_options = ["All Jobs"] + sorted(
        df["Job"].dropna().unique().tolist()
    )

    selected_job = st.selectbox(
        "Job",
        job_options,
        label_visibility="collapsed"
    )

    # =====================================================
    # EDUCATION FILTER
    # =====================================================

    st.markdown("""
    <div class="filter-card">
        <div class="filter-title">
            🎓 EDUCATION LEVEL
        </div>
    </div>
    """, unsafe_allow_html=True)

    education_options = ["All Education"] + sorted(
        df["Education"].dropna().unique().tolist()
    )

    selected_education = st.selectbox(
        "Education",
        education_options,
        label_visibility="collapsed"
    )

    # =====================================================
    # MARITAL FILTER
    # =====================================================

    st.markdown("""
    <div class="filter-card">
        <div class="filter-title">
            👥 MARITAL STATUS
        </div>
    </div>
    """, unsafe_allow_html=True)

    marital_options = ["All Status"] + sorted(
        df["Marital Status"].dropna().unique().tolist()
    )

    selected_marital = st.selectbox(
        "Marital",
        marital_options,
        label_visibility="collapsed"
    )

    # =====================================================
    # AGE FILTER
    # =====================================================

    st.markdown("""
    <div class="filter-card">
        <div class="filter-title">
            🎂 AGE RANGE
        </div>
    </div>
    """, unsafe_allow_html=True)

    min_age = int(df["Age"].min())
    max_age = int(df["Age"].max())

    age_range = st.slider(
        "Age",
        min_value=min_age,
        max_value=max_age,
        value=(min_age, max_age),
        label_visibility="collapsed"
    )

    st.markdown("---")

    st.caption("✨ Smart filtering • Interactive analytics")


# =========================================================
# APPLY FILTERS
# =========================================================

filtered_df = df.copy()

if selected_job != "All Jobs":
    filtered_df = filtered_df[
        filtered_df["Job"] == selected_job
    ]

if selected_education != "All Education":
    filtered_df = filtered_df[
        filtered_df["Education"] == selected_education
    ]

if selected_marital != "All Status":
    filtered_df = filtered_df[
        filtered_df["Marital Status"] == selected_marital
    ]

filtered_df = filtered_df[
    filtered_df["Age"].between(
        age_range[0],
        age_range[1]
    )
]


# =========================================================
# HEADER
# =========================================================

st.markdown(
    "# 🏦 Bank Marketing Intelligence Dashboard"
)

st.markdown(
    "### Customer Behaviour  •  Campaign Performance  •  Subscription Analytics"
)

st.markdown("---")


# =========================================================
# COMMON METRICS
# =========================================================

total_customers = len(filtered_df)

subscribed = (
    filtered_df["Subscription Status"]
    .eq("Subscribed")
    .sum()
)

not_subscribed = (
    filtered_df["Subscription Status"]
    .eq("Not Subscribed")
    .sum()
)

conversion_rate = (
    subscribed / total_customers * 100
    if total_customers > 0 else 0
)

avg_balance = (
    filtered_df["Average balance"].mean()
    if total_customers > 0 else 0
)


# =========================================================
# EXECUTIVE DASHBOARD
# =========================================================

if menu == "🏠 Executive Dashboard":

    st.markdown("## 📊 Executive Overview")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "👥 Total Customers",
        f"{total_customers:,}"
    )

    c2.metric(
        "✅ Subscribed",
        f"{subscribed:,}"
    )

    c3.metric(
        "🎯 Conversion Rate",
        f"{conversion_rate:.2f}%"
    )

    c4.metric(
        "💰 Avg. Balance",
        f"{avg_balance:,.0f}"
    )

    st.markdown("---")

    # =====================================================
    # DONUT
    # =====================================================

    col1, col2 = st.columns(2)

    with col1:

        st.markdown("### 🍩 Subscription Distribution")

        sub_data = (
            filtered_df["Subscription Status"]
            .value_counts()
            .reset_index()
        )

        sub_data.columns = ["Status", "Count"]

        fig = px.pie(
            sub_data,
            names="Status",
            values="Count",
            hole=0.68,
            color="Status",
            color_discrete_map={
                "Subscribed": "#087EA4",
                "Not Subscribed": "#C026D3"
            }
        )

        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font_color="white",
            legend_title=""
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    # =====================================================
    # JOB
    # =====================================================

    with col2:

        st.markdown("### 💼 Subscription Rate by Job")

        job_rate = (
            filtered_df
            .groupby("Job")["Class"]
            .apply(
                lambda x: (x == 1).mean() * 100
            )
            .reset_index(
                name="Subscription Rate"
            )
            .sort_values(
                "Subscription Rate"
            )
        )

        fig = px.bar(
            job_rate,
            x="Subscription Rate",
            y="Job",
            orientation="h",
            text_auto=".1f"
        )

        fig.update_traces(
            marker_color="#38BDF8"
        )

        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font_color="white",
            xaxis_title="Subscription Rate (%)",
            yaxis_title="",
            showlegend=False
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    # =====================================================
    # AGE
    # =====================================================

    st.markdown("### 👤 Customer Age Distribution")

    fig = px.histogram(
        filtered_df,
        x="Age",
        color="Subscription Status",
        nbins=30,
        barmode="overlay",
        opacity=0.75,
        color_discrete_map={
            "Subscribed": "#0EA5E9",
            "Not Subscribed": "#C026D3"
        }
    )

    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color="white",
        xaxis_title="Age",
        yaxis_title="Customers"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# =========================================================
# CUSTOMER INSIGHTS
# =========================================================

elif menu == "👥 Customer Insights":

    st.markdown("## 👥 Customer Behaviour Insights")

    col1, col2 = st.columns(2)

    with col1:

        marital = (
            filtered_df
            .groupby(
                ["Marital Status", "Subscription Status"]
            )
            .size()
            .reset_index(
                name="Customers"
            )
        )

        fig = px.bar(
            marital,
            x="Marital Status",
            y="Customers",
            color="Subscription Status",
            barmode="group",
            title="Marital Status vs Subscription",
            color_discrete_map={
                "Subscribed": "#0EA5E9",
                "Not Subscribed": "#C026D3"
            }
        )

        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font_color="white"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    with col2:

        education_rate = (
            filtered_df
            .groupby("Education")["Class"]
            .apply(
                lambda x: (x == 1).mean() * 100
            )
            .reset_index(
                name="Subscription Rate"
            )
        )

        fig = px.bar(
            education_rate,
            x="Education",
            y="Subscription Rate",
            text_auto=".1f",
            title="Education vs Subscription"
        )

        fig.update_traces(
            marker_color="#8B5CF6"
        )

        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font_color="white"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    # =====================================================
    # LOAN ANALYSIS
    # =====================================================

    st.markdown("## 💳 Loan Behaviour")

    col1, col2 = st.columns(2)

    with col1:

        housing = (
            filtered_df
            .groupby(
                ["Housing loan", "Subscription Status"]
            )
            .size()
            .reset_index(
                name="Customers"
            )
        )

        fig = px.bar(
            housing,
            x="Housing loan",
            y="Customers",
            color="Subscription Status",
            barmode="group",
            title="Housing Loan vs Subscription"
        )

        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font_color="white"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    with col2:

        personal = (
            filtered_df
            .groupby(
                ["Personal loan", "Subscription Status"]
            )
            .size()
            .reset_index(
                name="Customers"
            )
        )

        fig = px.bar(
            personal,
            x="Personal loan",
            y="Customers",
            color="Subscription Status",
            barmode="group",
            title="Personal Loan vs Subscription"
        )

        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font_color="white"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    # BALANCE

    fig = px.box(
        filtered_df,
        x="Subscription Status",
        y="Average balance",
        color="Subscription Status",
        title="Balance Distribution by Subscription",
        color_discrete_map={
            "Subscribed": "#0EA5E9",
            "Not Subscribed": "#C026D3"
        }
    )

    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color="white"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# =========================================================
# CAMPAIGN ANALYTICS
# =========================================================

elif menu == "📢 Campaign Analytics":

    st.markdown("## 📢 Campaign Performance")

    col1, col2 = st.columns(2)

    # CONTACT
    with col1:

        contact_rate = (
            filtered_df
            .groupby("Contact")["Class"]
            .apply(
                lambda x: (x == 1).mean() * 100
            )
            .reset_index(
                name="Conversion Rate"
            )
        )

        fig = px.bar(
            contact_rate,
            x="Contact",
            y="Conversion Rate",
            text_auto=".1f",
            title="Conversion Rate by Contact"
        )

        fig.update_traces(
            marker_color="#06B6D4"
        )

        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font_color="white"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    # MONTH
    with col2:

        month_order = [
            "jan", "feb", "mar", "apr",
            "may", "jun", "jul", "aug",
            "sep", "oct", "nov", "dec"
        ]

        month_rate = (
            filtered_df
            .groupby("Contact month")["Class"]
            .apply(
                lambda x: (x == 1).mean() * 100
            )
            .reindex(month_order)
            .reset_index(
                name="Subscription Rate"
            )
        )

        fig = px.line(
            month_rate,
            x="Contact month",
            y="Subscription Rate",
            markers=True,
            title="Monthly Subscription Rate"
        )

        fig.update_traces(
            line_color="#A855F7",
            marker_color="#38BDF8"
        )

        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font_color="white"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    # CAMPAIGN CONTACTS

    st.markdown("### 📞 Campaign Contact vs Conversion")

    campaign = (
        filtered_df
        .groupby("Campaign contacts")["Class"]
        .agg(
            Customers="count",
            Subscribed=lambda x: (x == 1).sum()
        )
        .reset_index()
    )

    campaign["Conversion Rate"] = (
        campaign["Subscribed"]
        / campaign["Customers"]
        * 100
    )

    fig = px.scatter(
        campaign,
        x="Campaign contacts",
        y="Conversion Rate",
        size="Customers",
        hover_data=[
            "Customers",
            "Subscribed"
        ],
        title="Campaign Contacts vs Conversion Rate"
    )

    fig.update_traces(
        marker_color="#38BDF8"
    )

    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color="white"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# =========================================================
# DATA EXPLORER
# =========================================================

elif menu == "🔎 Data Explorer":

    st.markdown("## 🔎 Interactive Data Explorer")

    selected_columns = st.multiselect(
        "Select columns",
        df.columns.tolist(),
        default=df.columns.tolist()
    )

    if selected_columns:

        st.dataframe(
            filtered_df[selected_columns],
            use_container_width=True,
            height=500
        )

    st.markdown("### 📋 Dataset Information")

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Rows",
        f"{len(filtered_df):,}"
    )

    c2.metric(
        "Columns",
        len(filtered_df.columns)
    )

    c3.metric(
        "Missing Values",
        int(filtered_df.isnull().sum().sum())
    )

    csv = filtered_df.to_csv(index=False)

    st.download_button(
        "⬇️ Download Filtered Data",
        csv,
        "bank_marketing_filtered.csv",
        "text/csv"
    )


# =========================================================
# FOOTER
# =========================================================

st.markdown(
    """
    <div class="footer">
        🏦 Bank Marketing & Customer Behaviour Analysis
        <br>
        Interactive Business Intelligence Dashboard
    </div>
    """,
    unsafe_allow_html=True
)