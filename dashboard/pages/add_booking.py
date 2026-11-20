
import streamlit as st
import sqlite3
from datetime import date
from pathlib import Path

# PAGE CONFIGURATION
st.set_page_config(
    page_title="Add New Booking",
    page_icon="🏨",
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

    .form-heading {
        color: #172B4D;
        font-size: 21px;
        font-weight: 700;
        margin-bottom: 12px;
    }

    .info-card {
        background-color: white;
        padding: 22px;
        border-radius: 14px;
        border: 1px solid #E6ECF2;
        border-left: 5px solid #159D91;
        margin-top: 20px;
    }

    div.stButton > button,
    div.stFormSubmitButton > button {
        background-color: #159D91;
        color: white;
        border: none;
        border-radius: 9px;
        font-weight: 600;
        min-height: 45px;
    }

    div.stButton > button:hover,
    div.stFormSubmitButton > button:hover {
        background-color: #117F76;
        color: white;
    }

    hr {
        border-color: #E2E8F0;
    }
</style>
""", unsafe_allow_html=True)


# PAGE TITLE
st.title("➕ Add New Hotel Booking")

st.caption(
    "Register a new guest and manage their hotel reservation details."
)

st.divider()


# BOOKING FORM
st.markdown(
    '<div class="form-heading">👤 Guest Information</div>',
    unsafe_allow_html=True
)

with st.form("booking_form"):

    guest_name = st.text_input(
        "Guest Name",
        placeholder="Enter guest's full name"
    )

    col1, col2 = st.columns(2)

    with col1:
        room_type = st.selectbox(
            "Room Type",
            ["Standard", "Deluxe", "Suite"]
        )

    with col2:
        booking_status = st.selectbox(
            "Booking Status",
            ["Confirmed", "Cancelled"]
        )

    st.divider()

    st.markdown(
        '<div class="form-heading">📅 Booking Information</div>',
        unsafe_allow_html=True
    )

    col3, col4 = st.columns(2)

    with col3:
        check_in = st.date_input(
            "Check-in Date",
            value=date.today()
        )

    with col4:
        check_out = st.date_input(
            "Check-out Date",
            value=date.today()
        )

    booking_amount = st.number_input(
        "Booking Amount (₹)",
        min_value=0.0,
        value=9000.0,
        step=500.0
    )

    st.divider()

    submitted = st.form_submit_button(
        "💾 Save Booking",
        use_container_width=True
    )


# SAVE BOOKING
if submitted:

    if not guest_name.strip():
        st.error("Please enter the guest name.")

    elif check_out <= check_in:
        st.error("Check-out date must be after check-in date.")

    elif booking_amount <= 0:
        st.error("Please enter an amount greater than zero.")

    else:

        number_of_nights = (check_out - check_in).days

        try:
            with sqlite3.connect(str(DB_PATH)) as connection:

                cursor = connection.cursor()

                cursor.execute(
                    """
                    INSERT INTO bookings (
                        guest_name,
                        room_type,
                        check_in,
                        check_out,
                        number_of_nights,
                        booking_amount,
                        booking_status
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        guest_name.strip(),
                        room_type,
                        check_in.strftime("%Y-%m-%d"),
                        check_out.strftime("%Y-%m-%d"),
                        number_of_nights,
                        booking_amount,
                        booking_status
                    )
                )

            st.success("Booking added successfully! 🎉")

            st.markdown(
                '<div class="form-heading">📋 Booking Summary</div>',
                unsafe_allow_html=True
            )

            with st.container(border=True):

                st.write(f"**Guest Name:** {guest_name.strip()}")
                st.write(f"**Room Type:** {room_type}")
                st.write(f"**Check-in:** {check_in}")
                st.write(f"**Check-out:** {check_out}")
                st.write(f"**Number of Nights:** {number_of_nights}")
                st.write(f"**Booking Amount:** ₹{booking_amount:,.2f}")
                st.write(f"**Booking Status:** {booking_status}")

        except sqlite3.Error as error:
            st.error(f"Database error: {error}")
