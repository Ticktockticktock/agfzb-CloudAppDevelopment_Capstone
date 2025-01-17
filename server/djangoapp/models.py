from django.db import models
from datetime import datetime

# Create your models here.

# <HINT> Create a Car Make model `class CarMake(models.Model)`:
# - Name
# - Description
# - Any other fields you would like to include in car make model
# - __str__ method to print a car make object
class CarMake(models.Model):
    name = models.CharField(null=False, max_length=50)
    description = models.CharField(max_length=500)

    def __str__(self):
        return self.name


# <HINT> Create a Car Model model `class CarModel(models.Model):`:
# - Many-To-One relationship to Car Make model (One Car Make has many Car Models, using ForeignKey field)
# - Name
# - Dealer id, used to refer a dealer created in cloudant database
# - Type (CharField with a choices argument to provide limited choices such as Sedan, SUV, WAGON, etc.)
# - Year (DateField)
# - Any other fields you would like to include in car model
# - __str__ method to print a car make object
class CarModel(models.Model):
    id = models.AutoField(primary_key=True) 
    carMake = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    name = models.CharField(null=False, max_length=80)

    DEALER_ID_CHOICES = [(r,r) for r in range(1, 51)]
    dealerID = models.IntegerField(('dealer id'), choices= DEALER_ID_CHOICES, default= 1)
    
    SEDAN = 'sedan'
    SUV = 'suv'
    WAGON = 'wagon'
    PICKUP = 'pickup'
    HATCHBACK = 'hatchback'
    SPORTSCAR = 'sportscar'
    
    TYPE_CHOICES = [
        (SEDAN, 'sedan'),
        (SUV, 'suv'),
        (WAGON, 'wagon'),
        (PICKUP, 'pickup'),
        (HATCHBACK, 'hatchback'),
        (SPORTSCAR, 'sportscar')
    ]

    carType = models.CharField(
        null=False,
        max_length=30,
        choices=TYPE_CHOICES,
        default=SEDAN
    )

    YEAR_CHOICES = [(r,r) for r in range(2000, datetime.today().year+1)]
    year = models.IntegerField(('year'), choices=YEAR_CHOICES, default=datetime.now().year)
    description = models.CharField(max_length=500)

    def __str__(self):
        return self.carMake.__str__() + " " + self.name + " " + str(self.year)


# <HINT> Create a plain Python class `CarDealer` to hold dealer data
class CarDealer:
    def __init__(self, address, city, full_name, id, lat, long, short_name, st, zip):
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
        # Dealer zip
        self.zip = zip

    def __str__(self):
        return "Dealer name: " + self.full_name


# <HINT> Create a plain Python class `DealerReview` to hold review data
class DealerReview:
    def __init__(self, dealership, name, purchase, review):
        self.dealership = dealership
        self.name = name
        self.purchase = purchase
        self.review = review
        self.purchase_date = ""
        self.car_make = ""
        self.car_model = ""
        self.car_year = ""
        self.sentiment = ""
