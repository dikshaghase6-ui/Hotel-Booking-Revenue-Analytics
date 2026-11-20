
import sqlite3

# Connect to our database
connection = sqlite3.connect("hotel_bookings.db")
cursor = connection.cursor()

# Sample hotel booking records
bookings = [
    ("Rahul Sharma", "Deluxe", "2026-01-05", "2026-01-08", 3, 9000, "Confirmed"),
    ("Priya Patil", "Standard", "2026-01-10", "2026-01-12", 2, 4000, "Confirmed"),
    ("Amit Verma", "Suite", "2026-01-15", "2026-01-19", 4, 20000, "Confirmed"),
    ("Sneha Joshi", "Deluxe", "2026-02-02", "2026-02-05", 3, 9000, "Cancelled"),
    ("Rohan Mehta", "Standard", "2026-02-10", "2026-02-13", 3, 6000, "Confirmed"),
    ("Neha Singh", "Suite", "2026-02-18", "2026-02-20", 2, 10000, "Confirmed"),
    ("Karan Shah", "Deluxe", "2026-03-01", "2026-03-04", 3, 9000, "Confirmed"),
    ("Anjali Desai", "Standard", "2026-03-08", "2026-03-10", 2, 4000, "Cancelled"),
    ("Vikas Kumar", "Suite", "2026-03-15", "2026-03-19", 4, 20000, "Confirmed"),
    ("Pooja Nair", "Deluxe", "2026-03-22", "2026-03-25", 3, 9000, "Confirmed")
]

# Insert records into bookings table
cursor.executemany("""
    INSERT INTO bookings
    (guest_name, room_type, check_in, check_out,
     number_of_nights, booking_amount, booking_status)
    VALUES (?, ?, ?, ?, ?, ?, ?)
""", bookings)

# Save changes
connection.commit()

# Close database connection
connection.close()

print("10 hotel booking records inserted successfully!")
