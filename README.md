# Rental Cars

## start api

python3 main.py

### http-put /carrental

Five required datapoints:
Type | key | value
-----|------|-----
String | category | one of (compact,premium,minivan)
String | birthdate | year/month/day of customer
String | fromdate | year/month/day of rent
Int | days | how many days to rent
String | name |  Name of customer 


curl example:

    curl -X PUT -H "Content-Type: application/json" localhost:5000/carrental -d '{"category": "premium", "name": "Peter", "birthdate": "2000/02/13", "fromdate": "2020/12/15", "days": 4}'

Response:

    {
        "booking_id": "a4c92503-650b-48bf-a665-c8ca913c6cc9"
    }

### http-get /carrental/booking_id

curl example:

    curl -X GET localhost:5000/carrental/a4c92503-650b-48bf-a665-c8ca913c6cc9

Response:

    {
        "category": "premium",
        "birthdate": "2000-02-13 00:00:00",
        "fromdate": "2020-12-15 00:00:00",
        "days": "4 days, 0:00:00",
        "name": "Peter",
        "car": {
            "milage": 2000,
            "car_id": 105
        }
    }

### http-put /carreturn

Type | key | value
-----|------|-----
String | booking_id | booking id for rental
String | date | year/month/day of return
Int | Milage |  current milage of car



curl example:

    curl -XPUT -H "Content-Type: application/json" localhost:5000/carreturn -d '{"booking_id": "527bde99-697a-4460-ac85-6eebf86a2990", "date": "2020/12/19", "milage": 2100}'

Response:

    {
        "price": 2480.0
    }






## run auto tests

python3 CarRentTest.py

