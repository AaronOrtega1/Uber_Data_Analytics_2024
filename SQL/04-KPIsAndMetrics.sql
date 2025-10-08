/*
* ==============================================================================================
* KPIs and Metrics using SQL that will be displayed in the Power BI dashboard.
* ==============================================================================================
*/
-- TOTAL bookings
select
	count(*)
from
	fact_bookings fb ;
-- TOTAL revenue
select
	sum(fb.booking_value)
from
	fact_bookings fb ;
-- TOTAL cancelled rides.
select
	count(*)
from
	fact_bookings fb
where
	fb.cancelled_by_customer is true
	or fb.cancelled_by_driver is true;
-- PERCENTAGE cancelled rides.
select
	ROUND(
        100.0 * SUM(
            case 
                when fb.cancelled_by_customer or fb.cancelled_by_driver then 1 
                else 0 
            end
        ) / COUNT(*),
    2) as cancellation_percentage
from
	fact_bookings fb;
