from cars import Cars
def load_cars():
    cars = []
    cars_compact = {100 : {"category": "compact","model": "model1", "mileage": 1000},101 : {"category": "compact","model": "model1", "mileage": 2000},102 : {"category": "compact", "model": "model1", "mileage": 3000},103 : {"category": "compact", "model": "model1", "mileage": 4000}}
    cars_premium = {104 : {"category": "premium","model": "model1", "mileage": 1000},105 : {"category": "premium","model": "model1", "mileage": 2000},106 : {"category": "premium", "model": "model1", "mileage": 3000},107 : {"category": "premium", "model": "model1", "mileage": 4000}}
    cars_minivan = {108 : {"category": "minivan","model": "model1", "mileage": 1000},109 : {"category": "minivan","model": "model1", "mileage": 2000},110 : {"category": "minivan", "model": "model1", "mileage": 3000},111 : {"category": "minivan", "model": "model1", "mileage": 4000}}
    for id,car in cars_compact.items():
        mycar = Cars(id,car["category"], car["model"], car["mileage"])
        cars.append(mycar)
    for id,car in cars_premium.items():
        mycar = Cars(id,car["category"], car["model"], car["mileage"])
        cars.append(mycar)
    for id,car in cars_minivan.items():
        mycar = Cars(id,car["category"], car["model"], car["mileage"])
        cars.append(mycar)
    return cars