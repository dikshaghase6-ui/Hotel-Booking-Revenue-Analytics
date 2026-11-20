
import sqlite3
import pandas as pd

# Connect to database
connection = sqlite3.connect("hotel_bookings.db")

# Read booking data into a Pandas DataFrame
df = pd.read_sql_query("SELECT * FROM bookings", connection)

# Close connection
connection.close()

# Display all booking records
print("\n===== HOTEL BOOKING DATA =====")
print(df)

# Display basic information
print("\n===== DATA INFORMATION =====")
print(df.info())

# Calculate total bookings
print("\nTotal Bookings:", len(df))

# Calculate confirmed bookings
confirmed = df[df["booking_status"] == "Confirmed"]
print("Confirmed Bookings:", len(confirmed))

# Calculate cancelled bookings
cancelled = df[df["booking_status"] == "Cancelled"]
print("Cancelled Bookings:", len(cancelled))

# Calculate total confirmed revenue
print("Total Revenue: ₹", confirmed["booking_amount"].sum())

# Calculate average booking amount
print("Average Booking Amount: ₹", confirmed["booking_amount"].mean())

# Revenue by room type
print("\n===== REVENUE BY ROOM TYPE =====")
print(
    confirmed.groupby("room_type")["booking_amount"]
    .sum()
    .sort_values(ascending=False)
)

