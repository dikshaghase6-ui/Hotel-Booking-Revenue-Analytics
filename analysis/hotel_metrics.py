
import sqlite3
import pandas as pd

# Connect to database
connection = sqlite3.connect("hotel_bookings.db")

# Read confirmed bookings
df = pd.read_sql_query("""
    SELECT *
    FROM bookings
    WHERE booking_status = 'Confirmed'
""", connection)

connection.close()

# Calculate total revenue
total_revenue = df["booking_amount"].sum()

# Calculate total occupied room nights
occupied_nights = df["number_of_nights"].sum()

# Assume hotel has 10 rooms
total_rooms = 10

# Our sample period is January to March 2026 (90 days)
total_days = 90

# Calculate total available room nights
available_room_nights = total_rooms * total_days

# Calculate ADR
adr = total_revenue / occupied_nights

# Calculate occupancy rate
occupancy_rate = (occupied_nights / available_room_nights) * 100

# Calculate RevPAR
revpar = total_revenue / available_room_nights

# Display results
print("\n===== HOTEL PERFORMANCE METRICS =====")

print("Total Revenue: ₹", total_revenue)
print("Occupied Room Nights:", occupied_nights)

print("ADR: ₹", round(adr, 2))
print("Occupancy Rate:", round(occupancy_rate, 2), "%")
print("RevPAR: ₹", round(revpar, 2))

