
import sqlite3

# Connect to database
connection = sqlite3.connect("hotel_bookings.db")
cursor = connection.cursor()

# Retrieve all booking records
cursor.execute("SELECT * FROM bookings")

# Fetch all records
records = cursor.fetchall()

# Display records
print("\n===== HOTEL BOOKING RECORDS =====\n")

for record in records:
    print("Booking ID:", record[0])
    print("Guest Name:", record[1])
    print("Room Type:", record[2])
    print("Check-in:", record[3])
    print("Check-out:", record[4])
    print("Nights:", record[5])
    print("Amount: ₹", record[6])
    print("Status:", record[7])
    print("--------------------------------")

# Close connection
connection.close()
