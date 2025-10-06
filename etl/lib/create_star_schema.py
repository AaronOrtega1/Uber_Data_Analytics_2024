from sqlalchemy import text


class StarSchemaCreator:
    def __init__(self, engine):
        """
        Initiliaze the StarSchemaCreator with a database engine.

        Args:
            engine: sqlalchemy engine instance
        """
        self.engine = engine

    def _drop_existing_tables(self):
        """
        Method to drop all existing tables if they already exist.
        """
        tables_to_drop = [
            "fact_bookings",
            "dim_customers",
            "dim_vehicle_types",
            "dim_locations",
            "dim_time",
            "dim_payment_",
        ]

        with self.engine.connect() as conn:
            for table in tables_to_drop:
                conn.execute(text(f"DROP TABLE IF EXISTS {table} CASCADE"))
            conn.commit()

    def _create_dimension_tables(self):
        """
        Method to create all the dimension tables.
        """
        with self.engine.connect() as conn:
            # dim_vehicle_types
            conn.execute(
                text(
                    """
                    CREATE TABLE dim_vehicle_types (
                        vehicle_type_key SERIAL primary key,
                        vehicle_type VARCHAR(50),
                        vehicle_category VARCHAR(50)
                    )
                """
                )
            )

            # dim_time
            conn.execute(
                text(
                    """
                    CREATE TABLE dim_time (
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
                    )
                    """
                )
            )

            # dim_payment_methods
            conn.execute(
                text(
                    """
                    CREATE TABLE dim_payment_methods (
                        payment_method_key SERIAL primary key,
                        payment_method VARCHAR(50),
                        payment_type VARCHAR(20)
                    )
                    """
                )
            )

            # dim_booking_status
            conn.execute(
                text(
                    """
                    CREATE TABLE dim_booking_status (
                        status_key SERIAL primary key,
                        booking_status VARCHAR(50),
                        cancellation_reason VARCHAR(300),
                        incomplete_reason TEXT,
                        status_category VARCHAR(20)
                    )
                    """
                )
            )

            # dim_customers
            conn.execute(
                text("""
                CREATE TABLE dim_customers (
                    customer_key SERIAL primary key,
                    customer_id VARCHAR(50),
                    customer_behavior_category VARCHAR(50),
                    total_bookings_count INT,
                    cancellation_rate DECIMAL(5, 2)
                );
            """)
            )

            # dim_locations
            conn.execute(
                text(
                    """
                    CREATE TABLE dim_locations (
                        location_key SERIAL primary key,
                        pickup_location VARCHAR(200),
                        drop_location VARCHAR(200),
                        route_category VARCHAR(50)
                    );
                    """
                )
            )

            conn.commit()

    def _populate_dimension_tables(self):
        """
        Method to populate dimension tables.
        """

        with self.engine.connect() as conn:
            # dim_vehicle_types
            conn.execute(
                text("""
                insert
                    into
                    dim_vehicle_types (vehicle_type,
                    vehicle_category)
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
            """)
            )
            # dim_time
            conn.execute(
                text("""
                insert
                    into
                    dim_time (booking_timestamp,
                    date,
                    hour,
                    day_of_week,
                    day_name,
                    month,
                    month_name,
                    quarter,
                    year,
                    time_of_day)
                select
                    distinct
                    booking_timestamp,
                    DATE(booking_timestamp),
                    extract(hour from booking_timestamp),
                    extract(DOW from booking_timestamp),
                    TO_CHAR(booking_timestamp, 'Day'),
                    extract(month from booking_timestamp),
                    TO_CHAR(booking_timestamp, 'Month'),
                    extract(QUARTER from booking_timestamp),
                    extract(year from booking_timestamp),
                    case
                        when extract(hour from booking_timestamp) between 6 and 11 then 'Morning'
                        when extract(hour from booking_timestamp) between 12 and 17 then 'Afternoon'
                        when extract(hour from booking_timestamp) between 18 and 23 then 'Evening'
                        else 'Night'
                    end
                from
                    staging_bookings;
            """)
            )
            # dim_payment_methods
            conn.execute(
                text("""
                insert
                    into
                    dim_payment_methods (payment_method,
                    payment_type)
                select
                    distinct
                    payment_method,
                    case
                        when payment_method in ('UPI', 'Debit Card', 'Credit Card') then 'Digital'
                        when payment_method = 'Cash' then 'Cash'
                        else 'Other'
                    end
                from
                    staging_bookings
                where
                    payment_method is not null;
            """)
            )
            # dim_booking_status
            conn.execute(
                text("""
                insert
                    into
                    dim_booking_status (booking_status,
                    cancellation_reason,
                    incomplete_reason,
                    status_category)
                select
                    distinct
                    booking_status,
                    coalesce(reason_for_cancelling_by_customer, driver_cancellation_reason),
                    incomplete_rides_reason,
                    case
                        when booking_status = 'Completed' then 'Completed'
                        when booking_status in ('Cancelled by Customer', 'Cancelled by Driver') then 'Cancelled'
                        when booking_status = 'No Driver Found' then 'No Driver'
                        when booking_status = 'Incomplete' then 'Incomplete'
                        else 'Other'
                    end
                from
                    staging_bookings
            """)
            )
            # dim_customers
            conn.execute(
                text("""
                insert
                    into
                    dim_customers (customer_id,
                    customer_behavior_category,
                    total_bookings_count,
                    cancellation_rate)
                select
                    customer_id,
                    case
                        when COUNT(*) > 10 then 'Frequent'
                        when COUNT(*) between 5 and 10 then 'Regular'
                        else 'Occasional'
                    end,
                    COUNT(*),
                    ROUND(SUM(case when cancelled_rides_by_customer then 1 else 0 end) * 100.0 / COUNT(*), 2)
                from
                    staging_bookings
                group by
                    customer_id
            """)
            )
            # dim_locations
            conn.execute(
                text("""
                insert
                    into
                    dim_locations (pickup_location,
                    drop_location,
                    route_category)
                select
                    distinct
                    pickup_location,
                    drop_location,
                    case
                        when pickup_location != drop_location then 'Inter-location'
                        else 'Same-location'
                    end
                from
                    staging_bookings
            """)
            )
            conn.commit()

    def _create_fact_table(self):
        """
        Method to create the fact table of the star schema.
        """
        with self.engine.connect() as conn:
            conn.execute(
                text("""
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
                )
            """)
            )
            conn.commit()

    def _populated_fact_table(self):
        """
        Master method to create the entire star schema.
        """
        with self.engine.connect() as conn:
            conn.execute(
                text(
                    """
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
                """
                )
            )

            conn.commit()

    def create_star_schema(self):
        """
        Master method to create the entire star schema.
        """
        self._drop_existing_tables()
        self._create_dimension_tables()
        self._populate_dimension_tables()
        self._create_fact_table()
        self._populated_fact_table()
        print(
            "StarSchemaCreator finished. staging_bookings table transformed into star schema."
        )
