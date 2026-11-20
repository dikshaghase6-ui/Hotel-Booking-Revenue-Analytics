
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

# Connect to database
connection = sqlite3.connect("hotel_bookings.db")

# Read confirmed bookings
df = pd.read_sql_query("""
    SELECT room_type, booking_amount
    FROM bookings
    WHERE booking_status = 'Confirmed'
""", connection)

connection.close()

# Calculate revenue by room type
revenue = df.groupby("room_type")["booking_amount"].sum()

# Display revenue
print("\nRevenue by Room Type:")
print(revenue)

# Create bar chart
plt.figure(figsize=(8, 5))

revenue.plot(kind="bar")

plt.title("Hotel Revenue by Room Type")
plt.xlabel("Room Type")
plt.ylabel("Revenue (₹)")

plt.xticks(rotation=0)
plt.tight_layout()

# Save chart
plt.savefig("analysis/revenue_chart.png")

# Display chart
plt.show()

print("\nRevenue chart created successfully!")
