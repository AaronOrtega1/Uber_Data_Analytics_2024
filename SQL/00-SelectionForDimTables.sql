/*
* ==============================================================================================
* ONLY FOR REFERENCE CREATION AND POPULATION OF FACT AND DIMENSION TABLES HANDLED AUTOMATICALLY
* ==============================================================================================
-- dim_vehicle_types
select
	distinct 
    vehicle_type,
	case
		when vehicle_type in ('Go Sedan', 'Premier Sedan') then 'Premium'
		when vehicle_type in ('Go Mini') then 'Standard'
		when vehicle_type in ('Auto') then 'Budget'
		when vehicle_type in ('Bike', 'eBike') then 'Two-wheeler'
		else 'Other'
	end as vehicle_category
from
	staging_bookings;
-- dim_time
select
	distinct
    booking_timestamp,
	DATE(booking_timestamp),
	extract(hour from booking_timestamp) as hour,
	extract(DOW from booking_timestamp) as day_of_the_week,
	TO_CHAR(booking_timestamp, 'Day') as str_day_of_the_week,
	extract(month from booking_timestamp) as month,
	TO_CHAR(booking_timestamp, 'Month') as str_month,
	extract(QUARTER from booking_timestamp) as quarter_of_year,
	extract(year from booking_timestamp) as year,
	case
		when extract(hour from booking_timestamp) between 6 and 11 then 'Morning'
		when extract(hour from booking_timestamp) between 12 and 17 then 'Afternoon'
		when extract(hour from booking_timestamp) between 18 and 23 then 'Evening'
		else 'Night'
	end as time_of_day
from
	staging_bookings;
-- dim_payment_methods
select
	distinct
    payment_method,
	case
		when payment_method in ('UPI', 'Debit Card', 'Credit Card', 'Uber Wallet') then 'Digital'
		when payment_method = 'Cash' then 'Cash'
		else 'Other'
	end
from
	staging_bookings
where
	payment_method is not null;
-- dim_booking_status
select
	distinct
    booking_status,
	coalesce(reason_for_cancelling_by_customer , driver_cancellation_reason) as cancellation_rides_reason,
	incomplete_rides_reason,
	case
		when booking_status = 'Completed' then 'Completed'
		when booking_status in ('Cancelled by Customer', 'Cancelled by Driver') then 'Cancelled'
		when booking_status = 'No Driver Found' then 'No Driver'
		when booking_status = 'Incomplete' then 'Incomplete'
		else 'Other'
	end
from
	staging_bookings;
-- dim_customers
select
	customer_id,
	case
		when COUNT(*) > 10 then 'Frequent'
		when COUNT(*) between 5 and 10 then 'Regular'
		else 'Occasional'
	end,
	COUNT(*) as cancellations,
	ROUND(SUM(case when cancelled_rides_by_customer then 1 else 0 end) * 100.0 / COUNT(*), 2) as calcellation_percentage
from
	staging_bookings
group by
	customer_id;
-- dim_locations
select
	distinct
    pickup_location,
	drop_location,
	case
		when pickup_location != drop_location then 'Inter-location'
		else 'Same-location'
	end
from
	staging_bookings;

*/
