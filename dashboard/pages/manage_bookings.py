
import streamlit as st
import sqlite3
from pathlib import Path
import pandas as pd

# PAGE CONFIGURATION
st.set_page_config(
    page_title="Manage Bookings",
    page_icon="📋",
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

    .section-heading {
        color: #172B4D;
        font-size: 22px;
        font-weight: 700;
        margin-top: 10px;
        margin-bottom: 15px;
    }

    .info-card {
        background: white;
        padding: 20px;
        border-radius: 14px;
        border: 1px solid #E6ECF2;
        border-left: 5px solid #159D91;
        margin-bottom: 15px;
    }

    div.stButton > button {
        border-radius: 9px;
        font-weight: 600;
        min-height: 42px;
    }

    div.stFormSubmitButton > button {
        background-color: #159D91;
        color: white;
        border: none;
        border-radius: 9px;
        font-weight: 600;
        min-height: 45px;
    }

    div.stFormSubmitButton > button:hover {
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


# PAGE TITLE
st.title("📋 Manage Hotel Bookings")

st.caption(
    "View, update and delete existing hotel booking records."
)


# SUCCESS MESSAGES
if st.session_state.get("update_success", False):
    st.success("Booking updated successfully! 🎉")
    st.session_state["update_success"] = False

if st.session_state.get("delete_success", False):
    st.success("Booking deleted successfully! 🎉")
    st.session_state["delete_success"] = False


st.divider()


# FETCH BOOKINGS
try:
    with sqlite3.connect(str(DB_PATH)) as connection:

        df = pd.read_sql_query(
            "SELECT * FROM bookings ORDER BY booking_id",
            connection
        )

except sqlite3.Error as error:
    st.error(f"Database error: {error}")
    st.stop()


if df.empty:
    st.warning("No bookings are available.")
    st.stop()


# DISPLAY ALL BOOKINGS
st.markdown(
    '<div class="section-heading">📑 All Booking Records</div>',
    unsafe_allow_html=True
)

st.dataframe(
    df,
    use_container_width=True,
    hide_index=True
)

st.caption(f"Total booking records: {len(df)}")


st.divider()


# SELECT BOOKING
st.markdown(
    '<div class="section-heading">🔍 Select a Booking</div>',
    unsafe_allow_html=True
)

booking_options = {}

for _, row in df.iterrows():

    booking_options[
        f"ID: {row['booking_id']} - {row['guest_name']}"
    ] = int(row["booking_id"])


selected_booking = st.selectbox(
    "Choose a booking to manage",
    list(booking_options.keys())
)

booking_id = booking_options[selected_booking]

booking = df[
    df["booking_id"] == booking_id
].iloc[0]


# SELECTED BOOKING INFORMATION
st.markdown(
    f"""
    <div class="info-card">
        <div style="color:#64748B; font-size:14px;">
            SELECTED BOOKING
        </div>
        <div style="color:#172B4D; font-size:22px; font-weight:700;">
            {booking['guest_name']}
        </div>
        <div style="color:#475569; margin-top:8px;">
            Booking ID: {booking_id}
            &nbsp; | &nbsp;
            Room: {booking['room_type']}
            &nbsp; | &nbsp;
            Status: {booking['booking_status']}
        </div>
    </div>
    """,
    unsafe_allow_html=True
)


st.divider()


# EDIT BOOKING
st.markdown(
    '<div class="section-heading">✏️ Edit Booking Details</div>',
    unsafe_allow_html=True
)

with st.form("edit_booking_form"):

    guest_name = st.text_input(
        "Guest Name",
        value=str(booking["guest_name"])
    )

    col1, col2 = st.columns(2)

    with col1:

        room_type = st.selectbox(
            "Room Type",
            ["Standard", "Deluxe", "Suite"],
            index=["Standard", "Deluxe", "Suite"].index(
                booking["room_type"]
            )
        )

    with col2:

        booking_status = st.selectbox(
            "Booking Status",
            ["Confirmed", "Cancelled"],
            index=["Confirmed", "Cancelled"].index(
                booking["booking_status"]
            )
        )

    col3, col4 = st.columns(2)

    with col3:

        check_in = st.date_input(
            "Check-in Date",
            value=pd.to_datetime(
                booking["check_in"]
            ).date()
        )

    with col4:

        check_out = st.date_input(
            "Check-out Date",
            value=pd.to_datetime(
                booking["check_out"]
            ).date()
        )

    booking_amount = st.number_input(
        "Booking Amount (₹)",
        min_value=0.0,
        value=float(booking["booking_amount"]),
        step=500.0
    )

    update_button = st.form_submit_button(
        "💾 Update Booking",
        use_container_width=True
    )


# UPDATE BOOKING
if update_button:

    if not guest_name.strip():

        st.error("Please enter the guest name.")

    elif check_out <= check_in:

        st.error("Check-out date must be after check-in date.")

    elif booking_amount <= 0:

        st.error("Booking amount must be greater than zero.")

    else:

        number_of_nights = (check_out - check_in).days

        try:

            with sqlite3.connect(str(DB_PATH)) as connection:

                connection.execute(
                    """
                    UPDATE bookings
                    SET
                        guest_name = ?,
                        room_type = ?,
                        check_in = ?,
                        check_out = ?,
                        number_of_nights = ?,
                        booking_amount = ?,
                        booking_status = ?
                    WHERE booking_id = ?
                    """,
                    (
                        guest_name.strip(),
                        room_type,
                        check_in.strftime("%Y-%m-%d"),
                        check_out.strftime("%Y-%m-%d"),
                        number_of_nights,
                        booking_amount,
                        booking_status,
                        booking_id
                    )
                )

            st.session_state["update_success"] = True
            st.rerun()

        except sqlite3.Error as error:

            st.error(f"Database error: {error}")


st.divider()


# DELETE BOOKING
st.markdown(
    '<div class="section-heading">🗑️ Delete Booking</div>',
    unsafe_allow_html=True
)

st.warning(
    f"You are about to permanently delete booking ID "
    f"{booking_id} for {booking['guest_name']}."
)

confirm_delete = st.checkbox(
    "I confirm that I want to permanently delete this booking."
)

if st.button(
    "🗑️ Delete Selected Booking",
    type="primary",
    disabled=not confirm_delete,
    use_container_width=True
):

    try:

        with sqlite3.connect(str(DB_PATH)) as connection:

            connection.execute(
                "DELETE FROM bookings WHERE booking_id = ?",
                (booking_id,)
            )

        st.session_state["delete_success"] = True
        st.rerun()

    except sqlite3.Error as error:

        st.error(f"Database error: {error}")


st.caption("Hotel Booking Management System")
