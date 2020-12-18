class Cars():
    base_price = 100
    km_price = 20
    def __init__(self, id, category, model, milage):
        self.car_id = id
        self.category=category
        self.model = model
        self.milage = milage
        self.rentals = []

    def __str__(self):
        return f"{self.car_id} {self.category}"
    def __repr__(self):
        return f"{self.car_id}"

    def add_rental(self, rental):
        self.rentals.append(rental)

    def get_rental_from_bookingid(self, id):
        for rental in self.rentals:
            if id in rental:
                return rental
        return False
    def remove_booking_with_id(self, id):
        for rental in self.rentals:
            if id in rental:
                self.rentals.remove(rental)
                return True
        return False
    def calc_price(self,return_date, booking_id,milage):
        rental = self.get_rental_from_bookingid(booking_id)
        old_milage = self.milage
        self.milage = milage
        if not rental:
            return None
        rent_days = (return_date-rental[0]).days
        if rent_days < 1:
            rent_days = 1
        if self.category == "compact":
            price = self.base_price*rent_days
            return price
        if self.category == "premium":
            price = self.base_price*rent_days*1.2+(self.km_price*(self.milage-old_milage))
            return price
        if self.category == "minivan":
            price = self.base_price*rent_days*1.7+(self.km_price*(self.milage-old_milage)*1.5)
            return price
        return None

    def is_available(self, date, days):
        for rental in self.rentals:
            if rental[0] <= date <= rental[0]+rental[1] and rental[0] <= date+days <= rental[0]+ rental[1]:
                return False
        return True