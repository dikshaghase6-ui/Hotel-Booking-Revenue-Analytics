
import sqlite3

# Connect to database
connection = sqlite3.connect("hotel_bookings.db")
cursor = connection.cursor()

# Calculate total revenue from confirmed bookings
cursor.execute("""
    SELECT SUM(booking_amount)
    FROM bookings
    WHERE booking_status = 'Confirmed'
""")

total_revenue = cursor.fetchone()[0]

# Count confirmed bookings
cursor.execute("""
    SELECT COUNT(*)
    FROM bookings
    WHERE booking_status = 'Confirmed'
""")

confirmed_bookings = cursor.fetchone()[0]

# Count cancelled bookings
cursor.execute("""
    SELECT COUNT(*)
    FROM bookings
    WHERE booking_status = 'Cancelled'
""")

cancelled_bookings = cursor.fetchone()[0]

# Revenue by room type
cursor.execute("""
    SELECT room_type, SUM(booking_amount)
    FROM bookings
    WHERE booking_status = 'Confirmed'
    GROUP BY room_type
""")

room_revenue = cursor.fetchall()

# Display results
print("\n===== HOTEL REVENUE ANALYSIS =====")

print("Total Revenue: ₹", total_revenue)
print("Confirmed Bookings:", confirmed_bookings)
print("Cancelled Bookings:", cancelled_bookings)

print("\n===== REVENUE BY ROOM TYPE =====")

for room in room_revenue:
    print(room[0], ": ₹", room[1])

connection.close()
