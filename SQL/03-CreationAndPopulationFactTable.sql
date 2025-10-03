/*
* ==============================================================================================
* ONLY FOR REFERENCE CREATION AND POPULATION OF FACT AND DIMENSION TABLES HANDLED AUTOMATICALLY
* ==============================================================================================

drop table if exists fact_bookings;

create table fact_bookings (
    booking_id VARCHAR(50) primary key,
    customer_key INT,
    vehicle_type_key INT,
    location_key INT,
    time_key INT,
    payment_method_key INT,
    status_key INT,
    booking_value DECIMAL(10, 2),
    ride_distance DECIMAL(6, 2),
    avg_vtat DECIMAL(5, 2),
    avg_ctat DECIMAL(5, 2),
    driver_rating DECIMAL(2, 1),
    customer_rating DECIMAL(2, 1),
    cancelled_by_customer BOOL,
    cancelled_by_driver BOOL,
    incomplete_rides BOOL
);

insert
	into
	fact_bookings (
    booking_id,
	customer_key,
	vehicle_type_key,
	location_key,
	time_key,
	payment_method_key,
	status_key,
	booking_value,
	ride_distance,
	avg_vtat,
	avg_ctat,
	driver_rating,
	customer_rating,
	cancelled_by_customer,
	cancelled_by_driver,
	incomplete_rides
)
select
	sb.booking_id,
	dc.customer_key,
	vt.vehicle_type_key,
	loc.location_key,
	dt.time_key,
	pm.payment_method_key,
	bs.status_key,
	sb.booking_value,
	sb.ride_distance,
	sb.avg_vtat,
	sb.avg_ctat,
	sb.driver_ratings,
	sb.customer_rating,
	sb.cancelled_rides_by_customer,
	sb.cancelled_rides_by_driver,
	sb.incomplete_rides
from
	staging_bookings sb
left join dim_customers dc on
	sb.customer_id = dc.customer_id
left join dim_vehicle_types vt on
	sb.vehicle_type = vt.vehicle_type
left join dim_locations loc on
	sb.pickup_location = loc.pickup_location
	and sb.drop_location = loc.drop_location
left join dim_time dt on
	sb.booking_timestamp = dt.booking_timestamp
left join dim_payment_methods pm on
	sb.payment_method = pm.payment_method
left join dim_booking_status bs on
	sb.booking_status = bs.booking_status
	and coalesce(sb.reason_for_cancelling_by_customer, '') = coalesce(bs.cancellation_reason, '')
	and coalesce(sb.incomplete_rides_reason, '') = coalesce(bs.incomplete_reason, '');

select * from fact_bookings fb;


*/
