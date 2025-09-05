CREATE TABLE IF NOT EXISTS staging_bookings (
    booking_id TEXT PRIMARY KEY,
    customer_id TEXT NOT NULL,
    booking_timestamp TIMESTAMP NOT NULL,
    booking_status TEXT NOT NULL,
    vehicle_type TEXT,
    pickup_location TEXT,
    drop_location TEXT,
    avg_vtat NUMERIC(5,2), -- vehicle time arrival target
    avg_ctat NUMERIC(5,2), -- customer time arrival target
    cancelled_by_customer BOOLEAN,
    customer_cancellation_reason TEXT,
    cancelled_by_driver BOOLEAN,
    driver_cancellation_reason TEXT,
    incomplete BOOLEAN,
    incomplete_reason TEXT,
    booking_value NUMERIC(10,2),
    ride_distance NUMERIC(6,2),
    driver_rating NUMERIC(2,1),
    customer_rating NUMERIC(2,1),
    payment_method TEXT
);
