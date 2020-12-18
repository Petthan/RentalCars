from flask import Flask, request
from flask_restful import Api,Resource, reqparse, abort
from uuid import uuid4
from datetime import datetime,timedelta
from validation import validate_birthdate,validate_date,validate_days,validate_name
from cars import Cars
import os
from load_data import load_cars
import json

class CustomEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return str(obj)
        if isinstance(obj, timedelta):
            return str(obj)
        if isinstance(obj, Cars):
            return {'milage':obj.milage, 'car_id':obj.car_id}
        return json.JSONEncoder.default(self, obj)

app = Flask(__name__)
api = Api(app)
app.config["RESTFUL_JSON"] = {'cls': CustomEncoder}
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "Very secret key")

app.cars = load_cars()
app.car_rental = {}

def abort_if_rental_not_exist(booking_id):
    if booking_id not in app.car_rental:
        abort(404, message=f"Could not find this rental {booking_id}")

def check_available_cars(date,days,category):

    for car in app.cars:
        if car.category == category:
            if car.is_available(date,days):
                return car
    return False

class Rental(Resource):
    def get(self, booking_id):
        abort_if_rental_not_exist(booking_id)
        return app.car_rental[booking_id], 200
        
    def put(self):
        rent_id = str(uuid4())
        args = add_rental_args.parse_args()

        car = check_available_cars(args.fromdate, args.days, args.category)
        if not car:
            return {"message" : "No available cars"}, 400
        args["car"] = car
        car.add_rental((args.fromdate, args.days,rent_id))
        app.car_rental[rent_id] = args
        return {"booking_id": rent_id}, 201

def validate_return_date(returndate,fromdate):
    if returndate < fromdate:
        abort(404, message=f"return date cant be before rentdate")

class Return(Resource):
    def put(self):
        args = return_rental_args.parse_args()
        abort_if_rental_not_exist(args.booking_id)

        validate_return_date(args.date,app.car_rental[args.booking_id]["fromdate"])
        car = app.car_rental[args.booking_id]["car"]
        price = car.calc_price(args.date, args.booking_id,args.milage)
        if not price:
            return {"message": f"Cant calculate price for this booking {car}"}, 500
        car.remove_booking_with_id(args.booking_id)
        app.car_rental.pop(args.booking_id, None)

        return {"price": price}, 200

add_rental_args = reqparse.RequestParser()
add_rental_args.add_argument("category", choices=("Compact","Premium", "Minivan"),case_sensitive=False, type=str, help="Invalid category of car", required = True)
add_rental_args.add_argument("birthdate", type=validate_birthdate, required = True)
add_rental_args.add_argument("fromdate", type=validate_date ,required = True)
add_rental_args.add_argument("days", type=validate_days, required = True)
add_rental_args.add_argument("name", type=validate_name,help="name of customer", required = True)
api.add_resource(Rental, "/carrental", "/carrental/<string:booking_id>")

return_rental_args = reqparse.RequestParser()
return_rental_args.add_argument("booking_id", type=str, required=True)
return_rental_args.add_argument("date",type=validate_date, required=True)
return_rental_args.add_argument("milage", type=int, required=True)
api.add_resource(Return, "/carreturn")


if __name__ == "__main__":
    app.run(debug=True)