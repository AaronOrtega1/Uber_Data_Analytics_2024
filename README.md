# Uber Data Analytics 2024.

## Project Overview.


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



