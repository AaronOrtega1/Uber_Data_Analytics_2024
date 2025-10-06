/*
* ==============================================================================================
* ONLY FOR REFERENCE CREATION AND POPULATION OF FACT AND DIMENSION TABLES HANDLED AUTOMATICALLY
* ==============================================================================================
-- dim_vehicle_types
drop table if exists dim_vehicle_types;

create table dim_vehicle_types (
    vehicle_type_key SERIAL primary key,
    vehicle_type VARCHAR(50),
    vehicle_category VARCHAR(50)
);
-- dim_time
drop table if exists dim_time;

create table dim_time (
    time_key SERIAL primary key,
    booking_timestamp TIMESTAMP,
    date DATE,
    hour INT,
    day_of_week INT,
    day_name VARCHAR(10),
    month INT,
    month_name VARCHAR(10),
    quarter INT,
    year INT,
    time_of_day VARCHAR(20)
);
-- dim_payment_methods
drop table if exists dim_payment_methods;

create table dim_payment_methods (
    payment_method_key SERIAL primary key,
    payment_method VARCHAR(50),
    payment_type VARCHAR(20)
);
-- dim_booking_status
drop table if exists dim_booking_status;

create table dim_booking_status (
    status_key SERIAL primary key,
    booking_status VARCHAR(50),
    cancellation_reason VARCHAR(300),
    incomplete_reason TEXT,
    status_category VARCHAR(20)
);
-- dim_customers
drop table if exists dim_customers;

create table dim_customers (
    customer_key SERIAL primary key,
    customer_id VARCHAR(50),
    customer_behavior_category VARCHAR(50),
	total_bookings_count INT,
    cancellation_rate DECIMAL(5, 2)
);
-- dim_locations
drop table if exists dim_locations;

create table dim_locations (
    location_key SERIAL primary key,
    pickup_location VARCHAR(200),
    drop_location VARCHAR(200),
    route_category VARCHAR(50)
);
*/

