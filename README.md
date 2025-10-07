# 🚘 Uber Data Analytics 2024.

## 📌 Project Overview.

--- 

## Data Schema
- `booking_id`: Unique identifier for each ride booking.
- `booking_status`: Status of booking (Completed, Cancelled by Customer, Cancelled by Driver, etc.).
- `customer_id`: Unique identifier for customers.
- `vehicle_type`: Type of vehicle (Go Mini, Go Sedan, Auto, eBike/Bike, UberXL, Premier Sedan).
- `pick_up_location`: Starting location of the ride.
- `drop_location`: Destination location of the ride.
- `avg_vtat`: Average time for driver to reach pickup location (in minutes).
- `avg_ctat`: Average trip duration from pickup to destination (in minutes).
- `cancelled_by_customer`: Customer-initiated cancellation flag.
- `customer_cancellation_reason`: Reason for customer cancellation.
- `cancelled_by_driver`: Driver-initiated cancellation flag.
- `driver_cancellation_reason`: Reason for driver cancellation
- `incomplete_rides`: Incomplete ride flag
- `incomplete_rides_reason`: Reason for incomplete rides
- `booking_value`: Total fare amount for the ride
- `ride_distance`: Distance covered during the ride (in km)
- `driver_rating`: Rating given to driver (1-5 scale)
- `customer_rating`: Rating given by customer (1-5 scale)
- `payment_method`: Method used for payment (UPI, Cash, Credit Card, Uber Wallet, Debit Card)
- `booking_timestamp`: Timestamp of the booking.

---

## 🚀 Tech Stack

- **Database:** PostgreSQL (running in Docker).
- **ETL Job:** Python script (running in Docker).
- **Queries:** SQL.
- **Visualization:** Power BI.

---

## ⚙️ Local Setup Instructions

### Prerequisites

- Docker & Docker Compose

1. **Clone the repo**

```bash
git clone https://github.com/AaronOrtega1/SQL-PowerBI-Project.git
cd SQL-PowerBI-Project
```

2. **Create a .env file in the root of the folder with the next information**
```env
POSTGRES_DB=uber_db
POSTGRES_USER=uber_user
POSTGRES_PASSWORD=uber_passwordd
```

3. **Start PostgreSQL with Docker**

```bash
docker compose up -d
```

3. **The `docker-compose.yml` file automatically creates the Database.**
4. **Then a Python script runs that preprocess the data and loads it into a staging bookings table.**
5. **Then the Python script uses the data loaded into the staging table to create a star schema to have simpler queries and simplified Business Reporting logic.**
5. **To create a dashboard of your own, you have to connect the PostgreSQL DB to Power BI desktop also using the information in the `docker-compose.yml` file.**

---

## 




