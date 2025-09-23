# queries.py

# Q1. Retrieve all successful bookings
GET_ALL_BOOKINGS = """
SELECT *
FROM OLA_DataSet
WHERE Booking_Status = 'Success'
"""

# Q2. Find the average ride distance for each vehicle type
AVG_RIDE_DISTANCE_BY_VEHICLE = """
SELECT
    Vehicle_Type,
    AVG(Ride_Distance) AS AvgDistance
FROM
    OLA_DataSet
GROUP BY
    Vehicle_Type
"""

# Q3. Get the total number of cancelled rides by customers
TOTAL_CANCELLED_BY_CUSTOMERS = """
SELECT
    COUNT(Canceled_Rides_by_Customer) AS TotalCancelledByCustomers
FROM
    OLA_DataSet
"""

# Q4. Top 5 customers with highest rides
TOP_5_CUSTOMERS = """
SELECT
    Customer_ID,
    COUNT(Booking_ID) AS total_rides
FROM
    OLA_DataSet
GROUP BY
    Customer_ID
ORDER BY
    total_rides DESC
OFFSET 0 ROWS
FETCH NEXT 5 ROWS ONLY
"""

# Q5. Cancelled by driver (personal & car related)
CANCELLED_BY_DRIVER_ISSUES = """
SELECT COUNT(*) AS CancelledByDrivers
FROM OLA_DataSet
WHERE Canceled_Rides_by_Driver = 'Personal & Car related issue'
"""

# Q6. Max & Min driver rating for Prime Sedan
DRIVER_RATING_STATS_PRIME_SEDAN = """
SELECT MAX(Driver_Ratings) AS MaxRating,
       MIN(Driver_Ratings) AS MinRating
FROM OLA_DataSet
WHERE Vehicle_Type = 'Prime Sedan'
"""

# Q7. Rides paid via UPI
RIDES_WITH_UPI = """
SELECT *
FROM OLA_DataSet
WHERE Payment_Method = 'UPI'
"""

# Q8. Average customer rating per vehicle type
AVG_CUSTOMER_RATING_BY_VEHICLE = """
SELECT
    Vehicle_Type,
    CAST(AVG(TRY_CAST(Customer_Rating AS FLOAT)) AS DECIMAL(10,2)) AS AvgCustomerRating
FROM
    OLA_DataSet
GROUP BY
    Vehicle_Type
"""

# Q9. Total booking value of successful rides
TOTAL_BOOKING_VALUE_SUCCESS = """
SELECT SUM(Booking_Value) AS Total_Successful_Value
FROM OLA_DataSet
WHERE Booking_Status = 'Success'
"""

# Q10. Incomplete rides with reason
INCOMPLETE_RIDES_WITH_REASON = """
SELECT Booking_ID, Incomplete_Rides_Reason
FROM OLA_DataSet
WHERE Incomplete_Rides = 'Yes'
"""
