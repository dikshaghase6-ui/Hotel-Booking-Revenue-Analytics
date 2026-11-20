
import streamlit as st
import sqlite3
import pandas as pd
from pathlib import Path

# PAGE CONFIGURATION
st.set_page_config(
    page_title="Hotel Reports",
    page_icon="📈",
    layout="wide"
)

# DATABASE LOCATION
BASE_DIR = Path(__file__).resolve().parent.parent.parent
DB_PATH = BASE_DIR / "hotel_bookings.db"

# CUSTOM DESIGN
st.markdown("""
<style>
    .main {
        background-color: #F7F9FC;
    }

    h1 {
        color: #172B4D;
        font-weight: 750;
    }

    h2, h3 {
        color: #203B5C;
    }

    .report-card {
        background: #FFFFFF;
        padding: 22px 18px;
        border-radius: 14px;
        border: 1px solid #E6ECF2;
        border-left: 5px solid #159D91;
        box-shadow: 0 3px 12px rgba(20, 40, 70, 0.06);
        min-height: 105px;
    }

    .report-label {
        color: #64748B;
        font-size: 14px;
        font-weight: 600;
        margin-bottom: 12px;
    }

    .report-value {
        color: #172B4D;
        font-size: 27px;
        font-weight: 750;
    }

    .section-heading {
        color: #172B4D;
        font-size: 23px;
        font-weight: 700;
        margin-top: 10px;
        margin-bottom: 15px;
    }

    div.stDownloadButton > button {
        background-color: #159D91;
        color: white;
        border: none;
        border-radius: 9px;
        font-weight: 600;
        min-height: 45px;
    }

    div.stDownloadButton > button:hover {
        background-color: #117F76;
        color: white;
    }

    [data-testid="stDataFrame"] {
        border-radius: 12px;
    }

    hr {
        border-color: #E2E8F0;
    }
</style>
""", unsafe_allow_html=True)


# REPORT CARD FUNCTION
def show_report_card(label, value):
    st.markdown(
        f"""
        <div class="report-card">
            <div class="report-label">{label}</div>
            <div class="report-value">{value}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


# PAGE TITLE
st.title("📈 Hotel Reports & Analytics")

st.caption(
    "Explore booking performance, revenue trends and hotel business insights."
)

st.divider()


# DATABASE CONNECTION
try:
    with sqlite3.connect(str(DB_PATH)) as connection:
        df = pd.read_sql_query(
            "SELECT * FROM bookings",
            connection
        )

except sqlite3.Error as error:
    st.error(f"Database connection error: {error}")
    st.stop()


# CHECK DATA
if df.empty:

    st.warning(
        "No booking data available. Please add some bookings first."
    )

else:

    # CONVERT DATE COLUMNS
    df["check_in"] = pd.to_datetime(df["check_in"])
    df["check_out"] = pd.to_datetime(df["check_out"])

    # CONFIRMED BOOKINGS ONLY
    confirmed = df[
        df["booking_status"] == "Confirmed"
    ].copy()

    # SUMMARY METRICS
    total_bookings = len(df)

    confirmed_bookings = len(confirmed)

    cancelled_bookings = len(
        df[df["booking_status"] == "Cancelled"]
    )

    total_revenue = confirmed["booking_amount"].sum()


    # BOOKING SUMMARY
    st.markdown(
        '<div class="section-heading">📊 Booking Summary</div>',
        unsafe_allow_html=True
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        show_report_card(
            "📋 Total Bookings",
            f"{total_bookings:,}"
        )

    with col2:
        show_report_card(
            "✅ Confirmed Bookings",
            f"{confirmed_bookings:,}"
        )

    with col3:
        show_report_card(
            "❌ Cancelled Bookings",
            f"{cancelled_bookings:,}"
        )

    with col4:
        show_report_card(
            "💰 Total Revenue",
            f"₹{total_revenue:,.0f}"
        )


    # REVENUE BY ROOM TYPE
    st.divider()

    st.markdown(
        '<div class="section-heading">💰 Revenue by Room Type</div>',
        unsafe_allow_html=True
    )

    if not confirmed.empty:

        room_revenue = (
            confirmed.groupby("room_type")["booking_amount"]
            .sum()
            .reset_index()
        )

        room_revenue.columns = [
            "Room Type",
            "Revenue"
        ]

        left, right = st.columns([1.5, 1])

        with left:
            st.bar_chart(
                room_revenue,
                x="Room Type",
                y="Revenue"
            )

        with right:
            st.subheader("Revenue Details")

            st.dataframe(
                room_revenue,
                use_container_width=True,
                hide_index=True
            )

    else:
        st.info(
            "No confirmed bookings available for revenue analysis."
        )


    # MONTHLY REVENUE
    st.divider()

    st.markdown(
        '<div class="section-heading">📅 Monthly Revenue Analysis</div>',
        unsafe_allow_html=True
    )

    if not confirmed.empty:

        confirmed["Month"] = (
            confirmed["check_in"]
            .dt.to_period("M")
            .astype(str)
        )

        monthly_revenue = (
            confirmed.groupby("Month")["booking_amount"]
            .sum()
            .reset_index()
        )

        monthly_revenue.columns = [
            "Month",
            "Revenue"
        ]

        st.line_chart(
            monthly_revenue,
            x="Month",
            y="Revenue"
        )

    else:
        st.info(
            "Monthly revenue will appear when confirmed bookings are available."
        )


    # BOOKING STATUS REPORT
    st.divider()

    st.markdown(
        '<div class="section-heading">📌 Booking Status Report</div>',
        unsafe_allow_html=True
    )

    status_data = (
        df["booking_status"]
        .value_counts()
        .reset_index()
    )

    status_data.columns = [
        "Booking Status",
        "Number of Bookings"
    ]

    left, right = st.columns([1.5, 1])

    with left:
        st.bar_chart(
            status_data,
            x="Booking Status",
            y="Number of Bookings"
        )

    with right:
        st.subheader("Status Details")

        st.dataframe(
            status_data,
            use_container_width=True,
            hide_index=True
        )


    # COMPLETE BOOKING REPORT
    st.divider()

    st.markdown(
        '<div class="section-heading">📄 Complete Booking Report</div>',
        unsafe_allow_html=True
    )

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )

    st.caption(
        f"Total records available: {len(df)}"
    )


    # DOWNLOAD REPORT
    st.divider()

    st.markdown(
        '<div class="section-heading">📥 Download Reports</div>',
        unsafe_allow_html=True
    )

    csv_data = df.copy()

    csv_data["check_in"] = (
        csv_data["check_in"].dt.strftime("%Y-%m-%d")
    )

    csv_data["check_out"] = (
        csv_data["check_out"].dt.strftime("%Y-%m-%d")
    )

    csv_file = csv_data.to_csv(
        index=False
    ).encode("utf-8")

    st.download_button(
        label="⬇️ Download Complete Booking Report",
        data=csv_file,
        file_name="hotel_complete_report.csv",
        mime="text/csv",
        use_container_width=True
    )

    st.success("Your hotel reports are ready! 🎉")
