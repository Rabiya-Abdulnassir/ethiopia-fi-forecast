import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path


# ==========================
# PAGE CONFIG
# ==========================

st.set_page_config(
    page_title="Ethiopia Financial Inclusion Forecast",
    layout="wide"
)


# ==========================
# LOAD DATA
# ==========================

@st.cache_data
def load_data():

    base_dir = Path(__file__).resolve().parent.parent

    data_path = (
        base_dir
        / "data"
        / "processed"
        / "ethiopia_fi_enriched_data.csv"
    )

    df = pd.read_csv(data_path)

    df["date"] = pd.to_datetime(
        df["observation_date"],
        errors="coerce"
    )

    df["year"] = df["date"].dt.year

    return df


df = load_data()


# ==========================
# TITLE
# ==========================

st.title("🇪🇹 Ethiopia Financial Inclusion Forecast Dashboard")

st.write(
    """
    Interactive dashboard showing Ethiopia financial inclusion trends,
    mobile money growth, events, and forecasts for 2025-2027.
    """
)


# ==========================
# SIDEBAR
# ==========================

page = st.sidebar.selectbox(
    "Select Page",
    [
        "Overview",
        "Trends",
        "Forecasts",
        "Events Timeline",
        "Inclusion Projection"
    ]
)


# ==========================
# OVERVIEW
# ==========================

if page == "Overview":

    st.header("Overview")


    acc = df[
        df["indicator_code"]=="ACC_OWNERSHIP"
    ]

    mm = df[
        df["indicator_code"]=="ACC_MM_ACCOUNT"
    ]


    c1,c2,c3,c4 = st.columns(4)


    with c1:
        if len(acc)>0:
            st.metric(
                "Account Ownership",
                f"{acc['value_numeric'].max():.1f}%"
            )


    with c2:
        if len(mm)>0:
            st.metric(
                "Mobile Money Accounts",
                f"{mm['value_numeric'].max():.1f}%"
            )


    with c3:
        st.metric(
            "Total Records",
            len(df)
        )


    with c4:
        st.metric(
            "Indicators",
            df["indicator_code"].nunique()
        )


    if len(acc)>0:

        fig = px.line(
            acc,
            x="year",
            y="value_numeric",
            markers=True,
            title="Account Ownership Trend"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


    st.download_button(
        "Download Dataset",
        df.to_csv(index=False),
        "ethiopia_financial_inclusion_data.csv"
    )



# ==========================
# TRENDS
# ==========================

elif page=="Trends":

    st.header("Indicator Trends")


    indicator = st.selectbox(
        "Choose Indicator",
        df["indicator_code"].dropna().unique()
    )


    data = df[
        df["indicator_code"]==indicator
    ]


    fig = px.line(
        data,
        x="year",
        y="value_numeric",
        markers=True,
        title=indicator
    )


    st.plotly_chart(
        fig,
        use_container_width=True
    )


    channels = df[
        df["indicator_code"].isin(
            [
                "ACC_MM_ACCOUNT",
                "USG_TELEBIRR_USERS",
                "USG_MPESA_USERS"
            ]
        )
    ]


    fig2 = px.bar(
        channels,
        x="year",
        y="value_numeric",
        color="indicator_code",
        title="Mobile Money Channel Comparison"
    )


    st.plotly_chart(
        fig2,
        use_container_width=True
    )



# ==========================
# FORECASTS
# ==========================

elif page=="Forecasts":

    st.header("2025-2027 Forecasts")


    scenario = st.selectbox(
        "Scenario",
        [
            "Baseline",
            "Optimistic",
            "Pessimistic"
        ]
    )


    base_dir = Path(__file__).resolve().parent.parent


    forecast_file = (
        base_dir
        / "reports"
        / "account_ownership_forecast.csv"
    )


    if forecast_file.exists():

        forecast = pd.read_csv(
            forecast_file
        )


        fig = px.line(
            forecast,
            x="Year",
            y=scenario,
            markers=True,
            title=f"{scenario} Forecast"
        )


        st.plotly_chart(
            fig,
            use_container_width=True
        )


        st.dataframe(
            forecast
        )


        st.download_button(
            "Download Forecast CSV",
            forecast.to_csv(index=False),
            "forecast.csv"
        )


    else:

        st.warning(
            "Forecast file not found in reports folder."
        )



# ==========================
# EVENTS TIMELINE
# ==========================

elif page=="Events Timeline":

    st.header("Financial Inclusion Events Timeline")


    if "record_type" in df.columns:

        events = df[
            df["record_type"]=="event"
        ].copy()


        if len(events)>0:

            events["event_date"] = pd.to_datetime(
                events["observation_date"],
                errors="coerce"
            )


            fig = px.scatter(
                events,
                x="event_date",
                y="category",
                color="category",
                hover_data=["original_text"],
                title="Major Financial Inclusion Events"
            )


            st.plotly_chart(
                fig,
                use_container_width=True
            )

        else:

            st.info(
                "No event records available."
            )



# ==========================
# INCLUSION PROJECTION
# ==========================

elif page=="Inclusion Projection":

    st.header(
        "Progress Toward 60% Inclusion Target"
    )


    current = 49
    target = 60


    st.progress(
        current/target
    )


    st.write(
        f"""
        Current inclusion estimate: **{current}%**

        Target: **{target}%**
        """
    )


    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=current,
            title={
                "text":"Financial Inclusion (%)"
            },
            gauge={
                "axis":{
                    "range":[0,100]
                }
            }
        )
    )


    st.plotly_chart(
        fig,
        use_container_width=True
    )