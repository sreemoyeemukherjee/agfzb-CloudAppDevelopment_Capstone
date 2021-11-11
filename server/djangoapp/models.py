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


# <HINT> Create a plain Python class `DealerReview` to hold review data
