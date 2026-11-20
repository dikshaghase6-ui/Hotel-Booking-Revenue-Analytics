# 🏨 Hotel Booking & Revenue Analytics System

A Python-based web application designed to manage hotel bookings and analyze revenue performance using interactive dashboards and reports.

## 📌 Project Overview

The Hotel Booking & Revenue Analytics System helps users manage hotel reservations, track booking information, and understand hotel revenue through visual reports.

The application uses Python, SQLite, Pandas, and Streamlit to provide a simple and interactive hotel management and analytics experience.

## ✨ Features

### 📊 Dashboard
- View total bookings and confirmed bookings.
- Track cancelled bookings.
- Monitor total hotel revenue.
- View Average Daily Rate (ADR).
- Analyze estimated occupancy and RevPAR.
- Explore revenue and booking charts.
- Filter bookings by date, room type, and status.

### ➕ Add New Booking
- Add new guest bookings.
- Select room types and booking status.
- Enter check-in and check-out dates.
- Calculate the number of nights automatically.
- Validate booking details before saving.

### ✏️ Manage Bookings
- View all existing bookings.
- Select bookings using their Booking ID.
- Update guest and reservation details.
- Delete bookings with confirmation.

### 📈 Reports & Analytics
- View booking summaries.
- Analyze revenue by room type.
- Track monthly revenue.
- View booking status reports.
- Download booking reports as CSV files.

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Main programming language |
| SQLite | Database management |
| Pandas | Data processing and analysis |
| Streamlit | Web application and dashboard |
| Matplotlib | Data visualization |

## 📂 Project Structure

```text
Hotel_Booking_Analytics/
│
├── analysis/
│
├── data/
│
├── database/
│
├── dashboard/
│   ├── app.py
│   └── pages/
│       ├── add_booking.py
│       ├── manage_bookings.py
│       └── reports.py
│
├── hotel_bookings.db
├── main.py
├── requirements.txt
├── README.md
└── .gitignore
```

## ⚙️ Installation & Setup

### 1. Clone the Repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
```

### 2. Navigate to the Project Folder

```bash
cd Hotel_Booking_Analytics
```

### 3. Create a Virtual Environment

```bash
python3 -m venv .venv
```

### 4. Activate the Virtual Environment

For macOS:

```bash
source .venv/bin/activate
```

### 5. Install Required Libraries

```bash
pip install -r requirements.txt
```

### 6. Run the Application

```bash
python3 -m streamlit run dashboard/app.py
```

The application will open in your web browser.

## 🗄️ Database

The project uses SQLite to store hotel booking information.

The bookings table includes:

- Booking ID
- Guest Name
- Room Type
- Check-in Date
- Check-out Date
- Number of Nights
- Booking Amount
- Booking Status

## 🎯 Learning Outcomes

Through this project, I gained practical experience in:

- Python programming.
- SQL and SQLite database operations.
- CRUD operations (Create, Read, Update and Delete).
- Data manipulation using Pandas.
- Interactive dashboard development using Streamlit.
- Data visualization and revenue analysis.
- Building a Python-based database application.

## 👩‍💻 Author

**Diksha Ghase**

GitHub: Add your GitHub profile link here.

---

*This project was developed as a practical learning project to strengthen my Python, database management, and data analytics skills.*