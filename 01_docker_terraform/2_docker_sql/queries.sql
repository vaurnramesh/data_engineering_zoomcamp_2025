-- Query1: Implicit Inner Join
SELECT
	tpep_pickup_datetime,
	tpep_dropoff_datetime,
	total_amount,
	CONCAT(zpu."Borough", ' | ', zpu."Zone") AS "pickup_location",
	CONCAT(zdo."Borough", ' | ', zdo."Zone") AS "dropoff_location"
FROM 
	yellow_taxi_trips t,
	zones zpu,
	zones zdo
WHERE 
	 t."PULocationID" = zpu."LocationID"
    AND t."DOLocationID" = zdo."LocationID"
LIMIT 100;


-- Query2: Checking for nulls
SELECT
	tpep_pickup_datetime,
	tpep_dropoff_datetime,
	total_amount,
	"PULocationID",
	"DOLocationID"
FROM 
	yellow_taxi_trips t

WHERE 
	"PULocationID" IS NULL 
	OR "DOLocationID" IS NULL
;


-- Query3: Checking for nulls if t1 pickup/dropoff locationId is present in t2 pickup/dropopff locationId

SELECT
	tpep_pickup_datetime,
	tpep_dropoff_datetime,
	total_amount,
	"PULocationID",
	"DOLocationID"
FROM 
	yellow_taxi_trips t

WHERE 
	(
	"PULocationID" NOT IN
		SELECT "LocationID" FROM zones
	) 
	OR
	"DOLocationID" NOT IN
	(
		SELECT "LocationID" FROM zones
	)

-- Query4: Always use LEFT Join to include the NULLS in the table

SELECT
	(tpep_pickup_datetime::DATE) as pickup_date,
	(tpep_dropoff_datetime::DATE) as dropoff_date,
	total_amount,
	CONCAT(zpu."Borough", ' | ', zpu."Zone") AS "pickup_location",
	CONCAT(zdo."Borough", ' | ', zdo."Zone") AS "dropoff_location"
FROM 
	yellow_taxi_trips t
LEFT JOIN zones zpu ON 
	 t."PULocationID" = zpu."LocationID"
LEFT JOIN zones zdo ON	 
     t."DOLocationID" = zdo."LocationID"
GROUP BY 1,2,3,4,5
ORDER BY dropoff_date ASC

