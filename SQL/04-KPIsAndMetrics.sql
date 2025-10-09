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
    		when not fb.incomplete_rides and not fb.cancelled_by_customer and not fb.cancelled_by_driver then 1
    		else 0
    	end
    ) as completed_total,
	round(
        100.0 * sum(
            case 
    			when not fb.incomplete_rides and not fb.cancelled_by_customer and not fb.cancelled_by_driver then 1	
                else 0 
            end
        ) / count(*),
    2) as complete_percentage
from
	fact_bookings fb;
-- TOTAL and PERCENTAGE incompleted bookings
select
	count(*),
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

/*
 * ============================================================
 * FINANCIAL
 * ============================================================
 */
-- TOTAL revenue
select
	sum(fb.booking_value)
from
	fact_bookings fb ;
-- AVG revenue
select
	avg(fb.booking_value) as average_booking_value
from
	fact_bookings fb;
-- Revenue per Customer
select
	sum(fb.booking_value)/ count(distinct(dc.customer_id)) as revenue_per_customer
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
	count(*),
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
-- Avg VTAT
select
	round(avg(fb.avg_ctat), 2) as avg_ctat
from
	fact_bookings fb ;
-- Booking Completion Time Analysis
-- Month
select
	dt.month_name,
	count(*) as booking_by_month
from
	fact_bookings fb
join dim_time dt on
	fb.time_key = dt.time_key
group by
	dt.month_name
order by
	booking_by_month desc;
-- Quarter
select
	dt.quarter,
	count(*) as booking_by_quarter
from
	fact_bookings fb
join dim_time dt on
	fb.time_key = dt.time_key
group by
	dt.quarter
order by
	booking_by_quarter desc;
-- DOW
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
-- Time of Day
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
