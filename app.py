import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

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

.stApp {
    background: linear-gradient(135deg, #050816 0%, #0B1220 50%, #071A2B 100%);
    color: white;
}

[data-testid="stSidebar"] {
    background: #050B16;
}

[data-testid="stMetric"] {
    background: linear-gradient(135deg, #0B1B32, #102A43);
    border: 1px solid #1D4E89;
    padding: 18px;
    border-radius: 15px;
}

[data-testid="stMetricValue"] {
    color: #7DD3FC;
}

[data-testid="stMetricLabel"] {
    color: #CBD5E1;
}

h1 {
    color: #7DD3FC;
    font-weight: 800;
}

h2, h3 {
    color: #E2E8F0;
}

div[data-testid="stDataFrame"] {
    border-radius: 12px;
}

.stButton button {
    border-radius: 10px;
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# TITLE
# =========================================================

st.markdown(
    "<h1>🏦 Bank Marketing Intelligence Dashboard</h1>",
    unsafe_allow_html=True
)

st.markdown(
    "### Customer Behaviour • Campaign Performance • Subscription Analytics"
)

# =========================================================
# LOAD DATA
# =========================================================

@st.cache_data
def load_data():

    df = pd.read_csv("Bank_marketing.csv")

    # Rename columns according to the project notebook
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

    # Subscription labels
    if "Class" in df.columns:
        df["Subscription Status"] = df["Class"].map({
            1: "Subscribed",
            2: "Not Subscribed"
        })

    # Clean missing values
    df = df.drop_duplicates()

    return df


df = load_data()

# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.markdown("## 🏦 BANK ANALYTICS")

st.sidebar.markdown("---")

menu = st.sidebar.radio(
    "Select Dashboard",
    [
        "🏠 Executive Dashboard",
        "👥 Customer Insights",
        "📢 Campaign Analytics",
        "🔎 Data Explorer"
    ]
)

st.sidebar.markdown("---")

st.sidebar.markdown("### 🎛️ Filters")

# =========================================================
# FILTERS
# =========================================================

filtered_df = df.copy()

# Job filter
if "Job" in df.columns:

    jobs = st.sidebar.multiselect(
        "Job",
        sorted(df["Job"].dropna().unique()),
        default=sorted(df["Job"].dropna().unique())
    )

    if jobs:
        filtered_df = filtered_df[
            filtered_df["Job"].isin(jobs)
        ]

# Education filter
if "Education" in df.columns:

    education = st.sidebar.multiselect(
        "Education",
        sorted(df["Education"].dropna().unique()),
        default=sorted(df["Education"].dropna().unique())
    )

    if education:
        filtered_df = filtered_df[
            filtered_df["Education"].isin(education)
        ]

# Age filter
if "Age" in df.columns:

    min_age = int(df["Age"].min())
    max_age = int(df["Age"].max())

    age_range = st.sidebar.slider(
        "Age Range",
        min_age,
        max_age,
        (min_age, max_age)
    )

    filtered_df = filtered_df[
        filtered_df["Age"].between(
            age_range[0],
            age_range[1]
        )
    ]

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
# 1. EXECUTIVE DASHBOARD
# =========================================================

if menu == "🏠 Executive Dashboard":

    st.markdown("## 📊 Executive Overview")

    # KPI ROW
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
    # SUBSCRIPTION DONUT
    # =====================================================

    col1, col2 = st.columns(2)

    with col1:

        subscription_count = (
            filtered_df["Subscription Status"]
            .value_counts()
            .reset_index()
        )

        subscription_count.columns = [
            "Status",
            "Count"
        ]

        fig = px.pie(
            subscription_count,
            names="Status",
            values="Count",
            hole=0.65,
            title="Subscription Distribution",
            color="Status",
            color_discrete_map={
                "Subscribed": "#0B3D91",
                "Not Subscribed": "#8B0000"
            }
        )

        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font_color="white",
            legend_title="Status"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    # =====================================================
    # JOB PERFORMANCE
    # =====================================================

    with col2:

        job_rate = (
            filtered_df
            .groupby("Job")["Class"]
            .apply(lambda x: (x == 1).mean() * 100)
            .reset_index(name="Subscription Rate")
            .sort_values(
                "Subscription Rate",
                ascending=False
            )
        )

        fig = px.bar(
            job_rate,
            x="Subscription Rate",
            y="Job",
            orientation="h",
            title="Subscription Rate by Job",
            text_auto=".1f"
        )

        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font_color="white",
            xaxis_title="Subscription Rate (%)",
            yaxis_title=""
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    # =====================================================
    # AGE DISTRIBUTION
    # =====================================================

    st.markdown("## 👤 Customer Age Analysis")

    fig = px.histogram(
        filtered_df,
        x="Age",
        color="Subscription Status",
        nbins=30,
        title="Age Distribution by Subscription Status",
        barmode="overlay",
        opacity=0.75,
        color_discrete_map={
            "Subscribed": "#0B3D91",
            "Not Subscribed": "#8B0000"
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
# 2. CUSTOMER INSIGHTS
# =========================================================

elif menu == "👥 Customer Insights":

    st.markdown("## 👥 Customer Behaviour Analysis")

    # =====================================================
    # MARITAL STATUS
    # =====================================================

    col1, col2 = st.columns(2)

    with col1:

        marital = (
            filtered_df
            .groupby(
                ["Marital Status", "Subscription Status"]
            )
            .size()
            .reset_index(name="Customers")
        )

        fig = px.bar(
            marital,
            x="Marital Status",
            y="Customers",
            color="Subscription Status",
            barmode="group",
            title="Marital Status vs Subscription",
            color_discrete_map={
                "Subscribed": "#0B3D91",
                "Not Subscribed": "#8B0000"
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

    # =====================================================
    # EDUCATION
    # =====================================================

    with col2:

        education_rate = (
            filtered_df
            .groupby("Education")["Class"]
            .apply(lambda x: (x == 1).mean() * 100)
            .reset_index(name="Subscription Rate")
        )

        fig = px.bar(
            education_rate,
            x="Education",
            y="Subscription Rate",
            title="Education vs Subscription Rate",
            text_auto=".1f"
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
    # LOANS
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
            .reset_index(name="Customers")
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
            .reset_index(name="Customers")
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

    # =====================================================
    # BALANCE VS SUBSCRIPTION
    # =====================================================

    fig = px.box(
        filtered_df,
        x="Subscription Status",
        y="Average balance",
        color="Subscription Status",
        title="Balance Distribution by Subscription Status",
        color_discrete_map={
            "Subscribed": "#0B3D91",
            "Not Subscribed": "#8B0000"
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
# 3. CAMPAIGN ANALYTICS
# =========================================================

elif menu == "📢 Campaign Analytics":

    st.markdown("## 📢 Marketing Campaign Analytics")

    # =====================================================
    # CONTACT METHOD
    # =====================================================

    col1, col2 = st.columns(2)

    with col1:

        contact_rate = (
            filtered_df
            .groupby("Contact")["Class"]
            .apply(lambda x: (x == 1).mean() * 100)
            .reset_index(name="Conversion Rate")
        )

        fig = px.bar(
            contact_rate,
            x="Contact",
            y="Conversion Rate",
            title="Conversion Rate by Contact Method",
            text_auto=".1f"
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
    # MONTHLY PERFORMANCE
    # =====================================================

    with col2:

        month_order = [
            "jan", "feb", "mar", "apr",
            "may", "jun", "jul", "aug",
            "sep", "oct", "nov", "dec"
        ]

        month_rate = (
            filtered_df
            .groupby("Contact month")["Class"]
            .apply(lambda x: (x == 1).mean() * 100)
            .reindex(month_order)
            .reset_index(name="Subscription Rate")
        )

        fig = px.line(
            month_rate,
            x="Contact month",
            y="Subscription Rate",
            markers=True,
            title="Monthly Subscription Rate"
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
    # CAMPAIGN CONTACTS
    # =====================================================

    st.markdown("## 📞 Campaign Contact Analysis")

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
        title="Campaign Contacts vs Conversion Rate",
        hover_data=["Customers", "Subscribed"]
    )

    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color="white",
        xaxis_title="Number of Campaign Contacts",
        yaxis_title="Conversion Rate (%)"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # =====================================================
    # PREVIOUS CAMPAIGN RESULT
    # =====================================================

    previous_rate = (
        filtered_df
        .groupby("Previous result")["Class"]
        .apply(lambda x: (x == 1).mean() * 100)
        .reset_index(name="Subscription Rate")
        .sort_values(
            "Subscription Rate",
            ascending=False
        )
    )

    fig = px.bar(
        previous_rate,
        x="Previous result",
        y="Subscription Rate",
        title="Previous Campaign Outcome vs Current Subscription",
        text_auto=".1f"
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
# 4. DATA EXPLORER
# =========================================================

elif menu == "🔎 Data Explorer":

    st.markdown("## 🔎 Interactive Data Explorer")

    st.write(
        "Use the controls below to explore the bank marketing dataset."
    )

    # =====================================================
    # COLUMN SELECTOR
    # =====================================================

    columns = st.multiselect(
        "Select columns to display",
        df.columns.tolist(),
        default=df.columns.tolist()
    )

    if columns:

        st.dataframe(
            filtered_df[columns],
            use_container_width=True,
            height=500
        )

    # =====================================================
    # DOWNLOAD
    # =====================================================

    csv = filtered_df.to_csv(index=False)

    st.download_button(
        label="⬇️ Download Filtered Dataset",
        data=csv,
        file_name="bank_marketing_filtered.csv",
        mime="text/csv"
    )

    st.markdown("---")

    # =====================================================
    # DATA SUMMARY
    # =====================================================

    st.markdown("## 📋 Dataset Summary")

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Rows",
        f"{filtered_df.shape[0]:,}"
    )

    c2.metric(
        "Columns",
        filtered_df.shape[1]
    )

    c3.metric(
        "Duplicate Rows",
        filtered_df.duplicated().sum()
    )

    st.markdown("### Data Types")

    dtype_df = pd.DataFrame({
        "Column": filtered_df.columns,
        "Data Type": filtered_df.dtypes.astype(str).values,
        "Missing Values": filtered_df.isnull().sum().values
    })

    st.dataframe(
        dtype_df,
        use_container_width=True
    )

# =========================================================
# FOOTER
# =========================================================

st.markdown("---")

st.markdown(
    "<center>🏦 Bank Marketing & Customer Behaviour Analysis | "
    "Interactive Streamlit Dashboard</center>",
    unsafe_allow_html=True
)