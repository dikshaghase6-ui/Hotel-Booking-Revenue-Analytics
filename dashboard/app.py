
import streamlit as st
import sqlite3
import pandas as pd
from pathlib import Path

# PAGE CONFIGURATION
st.set_page_config(
    page_title="Hotel Booking & Revenue Analytics",
    page_icon="🏨",
    layout="wide"
)

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

    .kpi-card {
        background: #FFFFFF;
        padding: 22px 20px;
        border-radius: 14px;
        border: 1px solid #E6ECF2;
        border-left: 5px solid #159D91;
        box-shadow: 0 3px 12px rgba(20, 40, 70, 0.06);
        min-height: 112px;
    }

    .kpi-label {
        color: #64748B;
        font-size: 14px;
        font-weight: 600;
        margin-bottom: 12px;
    }

    .kpi-value {
        color: #172B4D;
        font-size: 27px;
        font-weight: 750;
    }

    .section-heading {
        color: #172B4D;
        font-size: 23px;
        font-weight: 700;
        margin-top: 10px;
        margin-bottom: 18px;
    }

    div.stButton > button,
    div.stDownloadButton > button {
        border-radius: 9px;
        border: 1px solid #159D91;
        color: #FFFFFF;
        background-color: #159D91;
        font-weight: 600;
    }

    div.stButton > button:hover,
    div.stDownloadButton > button:hover {
        background-color: #117F76;
        color: white;
        border-color: #117F76;
    }

    [data-testid="stMetric"] {
        background: white;
        padding: 15px;
        border-radius: 12px;
        border: 1px solid #E6ECF2;
    }

    [data-testid="stDataFrame"] {
        border-radius: 10px;
    }

    hr {
        border-color: #E2E8F0;
    }
</style>
""", unsafe_allow_html=True)


# KPI CARD FUNCTION
def show_kpi(label, value):
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-label">{label}</div>
            <div class="kpi-value">{value}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


# DATABASE LOCATION
BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "hotel_bookings.db"


# SIDEBAR NAVIGATION
st.sidebar.title("🏨 Hotel Management")

st.sidebar.page_link(
    "app.py",
    label="Dashboard",
    icon="📊"
)

st.sidebar.page_link(
    "pages/add_booking.py",
    label="Add Booking",
    icon="➕"
)

st.sidebar.page_link(
    "pages/manage_bookings.py",
    label="Manage Bookings",
    icon="📋"
)

st.sidebar.page_link(
    "pages/reports.py",
    label="Reports",
    icon="📈"
)

st.sidebar.divider()
st.sidebar.caption("Hotel Booking Management System")


# DATABASE CONNECTION
try:
    connection = sqlite3.connect(str(DB_PATH))

    df = pd.read_sql_query(
        "SELECT * FROM bookings",
        connection
    )

    connection.close()

except Exception as error:
    st.error(f"Database connection error: {error}")
    st.stop()


if df.empty:
    st.title("🏨 Hotel Booking & Revenue Analytics")
    st.warning("No booking records found. Please add a booking.")
    st.stop()


# DATE CONVERSION
df["check_in"] = pd.to_datetime(df["check_in"])
df["check_out"] = pd.to_datetime(df["check_out"])


# DASHBOARD TITLE
st.title("🏨 Hotel Booking & Revenue Analytics")

st.caption(
    "Monitor hotel bookings, revenue and business performance."
)


# QUICK NAVIGATION BUTTONS
st.markdown(
    '<div class="section-heading">⚡ Quick Actions</div>',
    unsafe_allow_html=True
)

nav1, nav2, nav3 = st.columns(3)

with nav1:
    st.page_link(
        "pages/add_booking.py",
        label="➕ Add New Booking",
        use_container_width=True
    )

with nav2:
    st.page_link(
        "pages/manage_bookings.py",
        label="📋 Manage Bookings",
        use_container_width=True
    )

with nav3:
    st.page_link(
        "pages/reports.py",
        label="📈 View Reports",
        use_container_width=True
    )


st.divider()


# SIDEBAR FILTERS
st.sidebar.header("Dashboard Filters")

min_date = df["check_in"].min().date()
max_date = df["check_in"].max().date()

selected_dates = st.sidebar.date_input(
    "Select Check-in Date Range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

room_options = sorted(df["room_type"].unique())

selected_rooms = st.sidebar.multiselect(
    "Select Room Type",
    room_options,
    default=room_options
)

status_options = sorted(df["booking_status"].unique())

selected_status = st.sidebar.multiselect(
    "Select Booking Status",
    status_options,
    default=status_options
)


# FILTER DATA
if len(selected_dates) == 2:

    start_date, end_date = selected_dates

    filtered_df = df[
        (df["check_in"].dt.date >= start_date) &
        (df["check_in"].dt.date <= end_date) &
        (df["room_type"].isin(selected_rooms)) &
        (df["booking_status"].isin(selected_status))
    ]

else:

    filtered_df = df[
        (df["room_type"].isin(selected_rooms)) &
        (df["booking_status"].isin(selected_status))
    ]


# CONFIRMED BOOKINGS
confirmed = filtered_df[
    filtered_df["booking_status"] == "Confirmed"
]


# CALCULATE METRICS
total_revenue = confirmed["booking_amount"].sum()

total_bookings = len(filtered_df)

confirmed_count = len(confirmed)

cancelled_count = len(
    filtered_df[
        filtered_df["booking_status"] == "Cancelled"
    ]
)

occupied_nights = confirmed["number_of_nights"].sum()

adr = (
    total_revenue / occupied_nights
    if occupied_nights > 0 else 0
)

if len(selected_dates) == 2:
    number_of_days = (end_date - start_date).days + 1
else:
    number_of_days = (max_date - min_date).days + 1

available_nights = 10 * number_of_days

occupancy = (
    occupied_nights / available_nights * 100
    if available_nights > 0 else 0
)

revpar = (
    total_revenue / available_nights
    if available_nights > 0 else 0
)


# KEY PERFORMANCE INDICATORS
st.markdown(
    '<div class="section-heading">📊 Key Performance Indicators</div>',
    unsafe_allow_html=True
)

col1, col2, col3, col4 = st.columns(4)

with col1:
    show_kpi("💰 Total Revenue", f"₹{total_revenue:,.0f}")

with col2:
    show_kpi("📋 Total Bookings", f"{total_bookings:,}")

with col3:
    show_kpi("✅ Confirmed Bookings", f"{confirmed_count:,}")

with col4:
    show_kpi("❌ Cancelled Bookings", f"{cancelled_count:,}")


st.write("")

col5, col6, col7 = st.columns(3)

with col5:
    show_kpi("🏷️ Average Daily Rate (ADR)", f"₹{adr:,.2f}")

with col6:
    show_kpi("🛏️ Occupancy Rate", f"{occupancy:.2f}%")

with col7:
    show_kpi("📈 Revenue Per Available Room", f"₹{revpar:,.2f}")


# ROOM REVENUE AND BOOKING STATUS
st.divider()

left, right = st.columns(2)

with left:

    st.subheader("💰 Revenue by Room Type")

    room_revenue = confirmed.groupby(
        "room_type"
    )["booking_amount"].sum()

    if not room_revenue.empty:
        st.bar_chart(room_revenue)
    else:
        st.info("No confirmed booking revenue available.")


with right:

    st.subheader("📌 Booking Status")

    status_count = filtered_df["booking_status"].value_counts()

    if not status_count.empty:
        st.bar_chart(status_count)
    else:
        st.info("No booking records available.")


# MONTHLY REVENUE
st.divider()

st.subheader("📅 Monthly Revenue Analysis")

monthly_data = confirmed.copy()

monthly_data["Month"] = (
    monthly_data["check_in"].dt.to_period("M").astype(str)
)

monthly_revenue = (
    monthly_data.groupby("Month")["booking_amount"]
    .sum()
    .sort_index()
)

if not monthly_revenue.empty:

    st.bar_chart(monthly_revenue)

    st.subheader("Monthly Revenue Details")

    st.dataframe(
        monthly_revenue.reset_index(),
        use_container_width=True,
        hide_index=True
    )

else:
    st.info("No monthly revenue data available for the selected filters.")


# BOOKING TABLE
st.divider()

st.subheader("📋 All Hotel Bookings")

st.dataframe(
    filtered_df,
    use_container_width=True,
    hide_index=True
)

st.caption(
    f"Showing {len(filtered_df)} booking records."
)


# CSV DOWNLOAD
st.divider()

st.subheader("📥 Download Booking Report")

csv_data = filtered_df.copy()

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
    label="⬇️ Download Booking Report (CSV)",
    data=csv_file,
    file_name="hotel_booking_report.csv",
    mime="text/csv"
)

st.success("Dashboard loaded successfully!")
