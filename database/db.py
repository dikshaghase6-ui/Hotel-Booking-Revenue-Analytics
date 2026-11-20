
import sqlite3

def create_database():
    # Connect to the database
    connection = sqlite3.connect("hotel_bookings.db")

    # Create a cursor
    cursor = connection.cursor()

    # Create bookings table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS bookings (
            booking_id INTEGER PRIMARY KEY AUTOINCREMENT,
            guest_name TEXT NOT NULL,
            room_type TEXT NOT NULL,
            check_in DATE NOT NULL,
            check_out DATE NOT NULL,
            number_of_nights INTEGER NOT NULL,
            booking_amount REAL NOT NULL,
            booking_status TEXT NOT NULL
        )
    """)

    # Save changes
    connection.commit()

    # Close connection
    connection.close()

    print("Hotel booking database created successfully!")

if __name__ == "__main__":
    create_database()
