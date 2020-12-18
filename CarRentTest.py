from app import app
import unittest
class FlaskTestCase(unittest.TestCase):
    def setUp(self):
        self.tester = app.test_client(self)

    def test_check_secrey_key_exist(self):
        self.assertTrue("SECRET_KEY" in app.config)
        self.assertTrue(app.config["SECRET_KEY"])

    def test_add_rental(self):
        r = self.tester.put('/carrental', json={"category": "Premium", "name": "peter", "birthdate": "1989/04/20", "fromdate": "2020/12/15", "days": 4})
        self.assertEqual(r.status_code, 201)
        self.assertIsInstance(r.json, dict)
        self.assertTrue("booking_id" in r.json)

    def test_add_rental_bad_data(self):
        r = self.tester.put('/carrental', json={"category": "sportcar", "name": "dennis", "birthdate": "1995/02/13", "fromdate": "2020/12/15", "days": 4})
        self.assertEqual(r.status_code, 400)
        self.assertIsInstance(r.json, dict)
        self.assertTrue("message" in r.json)


    def test_compare_prices_same_rent(self):
        #same booking different car category, verify price order
        r1 = self.tester.put('/carrental', json={"category": "compact", "name": "erik", "birthdate": "1990/05/12", "fromdate": "2021/12/15", "days": 4})
        r2 = self.tester.put('/carrental', json={"category": "premium", "name": "björn", "birthdate": "1990/05/12", "fromdate": "2021/12/15", "days": 4})
        r3 = self.tester.put('/carrental', json={"category": "minivan", "name": "emil", "birthdate": "1990/05/12", "fromdate": "2021/12/15", "days": 4})

        g1 = self.tester.get('/carrental/' + r1.json["booking_id"])
        g2 = self.tester.get('/carrental/' + r2.json["booking_id"])
        g3 = self.tester.get('/carrental/' + r3.json["booking_id"])

        d1 = {"booking_id": r1.json["booking_id"], "date": "2021/12/19", "milage": g1.json["car"]["milage"]+100}
        d2 = {"booking_id": r2.json["booking_id"], "date": "2021/12/19", "milage": g2.json["car"]["milage"]+100}
        d3 = {"booking_id": r3.json["booking_id"], "date": "2021/12/19", "milage": g3.json["car"]["milage"]+100}

        p1 = self.tester.put('/carreturn', json=d1)
        p2 = self.tester.put('/carreturn', json=d2)
        p3 = self.tester.put('/carreturn', json=d3)
        self.assertTrue(p1.json["price"] < p2.json["price"] < p3.json["price"])

    def test_get_rental(self):
        r = self.tester.put('/carrental', json={"category": "minivan", "name": "peter", "birthdate": "1991/02/13", "fromdate": "2020/12/15", "days": 4})
        r = self.tester.get('/carrental/' + r.json["booking_id"])
        self.assertEqual(r.status_code, 200)
        self.assertIsInstance(r.json, dict)
        self.assertTrue("category" in r.json)
        self.assertTrue("birthdate" in r.json)
        self.assertTrue("fromdate" in r.json)
        self.assertTrue("days" in r.json)
        self.assertTrue("name" in r.json)
        self.assertTrue("car" in r.json)
        self.assertTrue("milage" in r.json["car"])
        self.assertTrue("car_id" in r.json["car"])

    def test_return_rental(self):
        r = self.tester.put('/carrental', json={"category": "compact", "name": "peter", "birthdate": "1991/02/13", "fromdate": "2020/12/15", "days": 4})
        booking_id = r.json["booking_id"]
        r = self.tester.get('/carrental/' + booking_id)
        rd = {"booking_id": booking_id, "date": "2020/12/19", "milage": r.json["car"]["milage"]+100}
        r = self.tester.put('/carreturn', json=rd)
        self.assertIsInstance(r.json, dict)
        self.assertTrue("price" in r.json)
        self.assertTrue(r.status_code, 200)

    def test_check_return_early_rental(self):
        r = self.tester.put('/carrental', json={"category": "minivan", "name": "jonas", "birthdate": "1985/01/12", "fromdate": "2020/12/15", "days": 4})
        booking_id = r.json["booking_id"]
        r = self.tester.get('/carrental/' + booking_id)
        rd = {"booking_id": booking_id, "date": "2020/12/17", "milage": r.json["car"]["milage"]+100}
        r = self.tester.put('/carreturn', json=rd)
        r = self.tester.get('/carrental/' + booking_id)
        self.assertIsInstance(r.json, dict)
        self.assertTrue(r.status_code, 404)
        self.assertTrue("Could not find" in  r.json["message"])

    def test_young_renter(self):
        #kids cant drive
        r = self.tester.put('/carrental', json={"category": "Premium", "name": "kalle", "birthdate": "2010/02/13", "fromdate": "2020/12/15", "days": 40})
        self.assertTrue(r.status_code, 404)
        self.assertIsInstance(r.json, dict)
        self.assertTrue('Not old enough' in r.json["message"]["birthdate"])
        

    def test_add_rental_no_cars(self):
        #rent all cars
        r = self.tester.put('/carrental', json={"category": "Premium", "name": "petter", "birthdate": "2000/05/12", "fromdate": "2020/12/15", "days": 4})
        r = self.tester.put('/carrental', json={"category": "Premium", "name": "petter", "birthdate": "2000/05/12", "fromdate": "2020/12/15", "days": 4})
        r = self.tester.put('/carrental', json={"category": "Premium", "name": "petter", "birthdate": "2000/05/12", "fromdate": "2020/12/15", "days": 4})
        r = self.tester.put('/carrental', json={"category": "Premium", "name": "petter", "birthdate": "2000/05/12", "fromdate": "2020/12/15", "days": 4})
        r = self.tester.put('/carrental', json={"category": "Premium", "name": "petter", "birthdate": "2000/05/12", "fromdate": "2020/12/15", "days": 4})
        self.assertEqual(r.status_code, 400)
        self.assertIsInstance(r.json, dict)
        self.assertEqual("No available cars", r.json["message"])


if __name__ == '__main__':
    unittest.main()