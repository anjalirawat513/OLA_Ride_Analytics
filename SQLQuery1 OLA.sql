SELECT * FROM OLA_DataSet
--Q1.Retrieve all successful bookings:

SELECT *
FROM OLA_DataSet
WHERE Booking_Status = 'Success';

--Q2. Find the average ride distance for each vehicle type:

SELECT
    Vehicle_Type,
    AVG(Ride_Distance) AS Avg_Ride_Distance
FROM
    OLA_DataSet
GROUP BY
    Vehicle_Type;


--Q3. Get the total number of cancelled rides by customers:

SELECT
    COUNT(Canceled_Rides_by_Customer)
FROM
    OLA_DataSet;

--Q4. List the top 5 customers who booked the highest number of rides:

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
FETCH NEXT 5 ROWS ONLY;


--Q5. Get the number of rides cancelled by drivers due to personal and car-related issues:

SELECT COUNT(*) FROM OLA_DataSet
WHERE Canceled_Rides_by_Driver = 'Personal & Car related issue'

--Q6. Find the maximum and minimum driver ratings for Prime Sedan bookings:

SELECT MAX(Driver_Ratings) AS max_rating,
MIN(Driver_Ratings) AS min_rating
FROM OLA_DataSet
WHERE Vehicle_Type = 'Prime Sedan';

--Q7. Retrieve all rides where payment was made using UPI:

SELECT * FROM OLA_DataSet
WHERE Payment_Method = 'UPI';

--Q8. Find the average customer rating per vehicle type:

SELECT
    Vehicle_Type,
    CAST(AVG(TRY_CAST(Customer_Rating AS FLOAT)) AS DECIMAL(10,2)) AS avg_customer_rating
FROM
    OLA_DataSet
GROUP BY
    Vehicle_Type;

--Q9. Calculate the total booking value of rides completed successfully:

SELECT SUM(Booking_Value) AS Total_Successful_Value
FROM OLA_DataSet
WHERE Booking_Status = 'Success';

--Q10. List all incomplete rides along with the reason

SELECT Booking_ID, Incomplete_Rides_Reason
FROM OLA_DataSet
WHERE Incomplete_Rides = 'Yes';
