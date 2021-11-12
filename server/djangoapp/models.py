from django.db import models
from django.utils.timezone import now


# Create your models here.

# <HINT> Create a Car Make model `class CarMake(models.Model)`:
# - Name
# - Description
# - Any other fields you would like to include in car make model
# - __str__ method to print a car make object
class CarMake(models.Model):
    name = models.CharField(null=False, max_length=60, default="Car Make name")
    description = models.CharField(null=False, max_length=200, default="Car Make description")
    
    # Create a toString method for object string representation
    def __str__(self):
        return "Name: " + self.name + "," + "Description: " + self.description


# <HINT> Create a Car Model model `class CarModel(models.Model):`:
# - Many-To-One relationship to Car Make model (One Car Make has many Car Models, using ForeignKey field)
# - Name
# - Dealer id, used to refer a dealer created in cloudant database
# - Type (CharField with a choices argument to provide limited choices such as Sedan, SUV, WAGON, etc.)
# - Year (DateField)
# - Any other fields you would like to include in car model
# - __str__ method to print a car make object
class CarModel(models.Model):
    SEDAN = 'sedan'
    SUV = 'suv'
    WAGON = 'wagon'
    TYPE = [
        (SEDAN, 'Sedan'),
        (SUV, 'Suv'),
        (WAGON, 'Wagon'),
    ]
    name = models.CharField(null=False, max_length=100, default='Car Model name')
    dealerId = models.IntegerField()
    type = models.CharField(max_length=5, choices=TYPE, default=SEDAN)
    make = models.ForeignKey(CarMake, null=True, on_delete=models.CASCADE)
    year = models.DateField(default=now)
    # Create a toString method for object string representation
    def __str__(self):
        return "Name: " + self.name + "," + "Dealer Id: " + str(self.dealerId) + "," + "Type: " + self.type + "," + "Year: " + str(self.year)

# <HINT> Create a plain Python class `CarDealer` to hold dealer data
class CarDealer:

    def __init__(self, address, city, full_name, id, lat, long, short_name, st, state, zip):
        # Dealer address
        self.address = address
        # Dealer city
        self.city = city
        # Dealer Full Name
        self.full_name = full_name
        # Dealer id
        self.id = id
        # Location lat
        self.lat = lat
        # Location long
        self.long = long
        # Dealer short name
        self.short_name = short_name
        # Dealer state
        self.st = st
        self.state = state
        # Dealer zip
        self.zip = zip

    def __str__(self):
        return "Dealer name: " + self.full_name

# <HINT> Create a plain Python class `DealerReview` to hold review data
class DealerReview:

    def __init__(self, dealership, name, purchase, review, purchase_date, car_make, car_model, car_year, id):
        # Dealership
        self.dealership = dealership
        # name
        self.name = name
        # purchase
        self.purchase = purchase
        # review
        self.review = review
        # purchase_date
        self.purchase_date = purchase_date
        # car_make
        self.car_make = car_make
        # car_model
        self.car_model = car_model
        # car_year
        self.car_year = car_year
        # self.sentiment = sentiment
        # Dealer id
        self.id = id

    def __str__(self):
        return "Car Model: " + self.car_model
