class Vehicle:
  def __init__(self, make, model, year):
    self.make = make
    self.model = model
    self.year = year
  def get_info(self):
   print (f"Марка: {self.make}, Модель: {self.model}, Год:{self.year}.")

class Car(Vehicle):
    def start_engine(self):
      print("Машина завелась!")

class Bicycle(Vehicle):
  def ring_bell(self):
    print("Звенит звонок велосипеда!")

vehicle = Vehicle(make = "veh_1", model = "jup", year = 2000)
vehicle.get_info()

car = Car(make = "BWV", model = "E30", year = 1997)
car.get_info()
car.start_engine()

bicycle  = Bicycle (make = "Stels", model = "Sport", year = 2008)
bicycle.get_info()
bicycle.ring_bell()