/*
* ==============================================================================================
* KPIs and Metrics using SQL that will be displayed in the Power BI dashboard.
* ==============================================================================================
*/
/*
 * ============================================================
 * Performance
 * ============================================================
 */
-- TOTAL bookings and TOTAL completed bookings
select
	count(*) as total_bookings,
	sum(
    	case
    		when fb.status_key = 11 then 1
    		else 0
    	end
    ) as completed_total,
	round(
        100.0 * sum(
            case 
    			when fb.status_key = 11 then 1
                else 0 
            end
        ) / count(*),
    2) as complete_percentage
from
	fact_bookings fb;
-- TOTAL and PERCENTAGE incompleted bookings
select
	count(*) as total_bookings,
	sum(
    	case
    		when fb.incomplete_rides then 1
    		else 0
    	end
    ) as incomplete_total,
	round(
        100.0 * sum(
            case 
                when fb.incomplete_rides then 1 
                else 0 
            end
        ) / count(*),
    2) as incomplete_percentage
from
	fact_bookings fb;
-- TOTAL and PERCENTAGE cancelled rides.
select
	count(*),
	sum(
        case 
            when fb.cancelled_by_customer or fb.cancelled_by_driver then 1 
            else 0 
        end
    ) as cancellation_total,
	round(
        100.0 * sum(
            case 
                when fb.cancelled_by_customer or fb.cancelled_by_driver then 1 
                else 0 
            end
        ) / count(*),
    2) as cancellation_percentage
from
	fact_bookings fb;
-- TOTAL bookings and TOTAL bookings where driver was not found
select
	count(*) as total_bookings,
	sum(
    	case
    		when fb.status_key = 5 then 1
    		else 0
    	end
    ) as no_driver_total,
	round(
        100.0 * sum(
            case 
    			when fb.status_key = 5 then 1
                else 0 
            end
        ) / count(*),
    2) as no_driver_percentage
from
	fact_bookings fb;

/*
 * ============================================================
 * FINANCIAL
 * ============================================================
 */
-- TOTAL revenue
select
	sum(fb.booking_value) as total_revenue
from
	fact_bookings fb ;
-- AVG revenue
select
	round(avg(fb.booking_value), 2) as average_booking_value
from
	fact_bookings fb;
-- Revenue per Customer
select
	round(sum(fb.booking_value)/ count(distinct(dc.customer_id)), 2) as revenue_per_customer
from
	fact_bookings fb
join dim_customers dc on
	fb.customer_key = dc.customer_key;

/*
 * ============================================================
 * Customer Behavior
 * ============================================================
 */
-- Customer Segmentation
select
	dc.customer_behavior_category ,
	count(*) as number_of_customers,
	dc.cancellation_rate,
	dc.total_bookings_count
from
	dim_customers dc
group by
	dc.customer_behavior_category,
	dc.cancellation_rate,
	dc.total_bookings_count
order by
	dc.total_bookings_count desc ;
-- Avg Customer Rating
select
	round(avg(fb.customer_rating), 2) as avg_customer_rating
from
	fact_bookings fb ;
-- Avg Driver Rating
select
	round(avg(fb.driver_rating), 2) as avg_driver_rating
from
	fact_bookings fb ;

/*
 * ============================================================
 * Operation Efficiency
 * ============================================================
 */
-- Avg Ride Distance
select
	round(avg(fb.ride_distance), 2) as avg_ride_distance_km
from
	fact_bookings fb ;
-- Avg VTAT
select
	round(avg(fb.avg_vtat), 2) as avg_vtat
from
	fact_bookings fb ;
-- Avg CTAT
select
	round(avg(fb.avg_ctat), 2) as avg_ctat
from
	fact_bookings fb ;
-- Booking Completion Time Analysis
-- Bookings by Month
select
	dt.month_name,
	count(*) as bookings_by_month
from
	fact_bookings fb
join dim_time dt on
	fb.time_key = dt.time_key
group by
	dt.month_name
order by
	bookings_by_month desc;
-- Bookings by Quarter
select
	dt.quarter,
	count(*) as bookings_by_quarter
from
	fact_bookings fb
join dim_time dt on
	fb.time_key = dt.time_key
group by
	dt.quarter
order by
	bookings_by_quarter desc;
-- Bookings by DOW
select
	dt.day_name,
	count(*) as bookings_by_dow
from
	fact_bookings fb
join dim_time dt on
	fb.time_key = dt.time_key
group by
	dt.day_name
order by
	bookings_by_dow desc;
-- Bookings by Time of Day
select
	dt.time_of_day,
	count(*) as bookings_by_time_of_day
from
	fact_bookings fb
join dim_time dt on
	fb.time_key = dt.time_key
group by
	dt.time_of_day
order by
	bookings_by_time_of_day desc;

/*
 * ============================================================
 * Categorical Insights
 * ============================================================
 */
-- Bookings by vehicle type
select
	dvt.vehicle_type,
	count(*) as count_vehicle_type
from
	fact_bookings fb
join dim_vehicle_types dvt on
	fb.vehicle_type_key = dvt.vehicle_type_key
group by
	dvt.vehicle_type
order by
	count_vehicle_type desc;
-- Bookings by payment method
select
	dpm.payment_method,
	count(*) as count_payment_methods
from
	fact_bookings fb
join dim_payment_methods dpm on
	fb.payment_method_key = dpm.payment_method_key
group by
	dpm.payment_method
order by
	count_payment_methods desc;
-- Bookings by status category
select
	dbs.booking_status,
	count(*) as count_status
from
	fact_bookings fb
join dim_booking_status dbs on
	fb.status_key = dbs.status_key
group by
	dbs.booking_status 
order by
	count_status desc;
-- Reason to cancel of customers
select
	dbs.cancellation_reason,
	count(*) as count_per_reason
from
	fact_bookings fb
join dim_booking_status dbs on
	fb.status_key = dbs.status_key
where
	fb.cancelled_by_customer is true
group by
	dbs.cancellation_reason
order by
	count_per_reason desc;
