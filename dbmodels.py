# Create your models here.
from django.db import models

# Location Model
class Location(models.Model):
    locationID = models.AutoField(primary_key=True)
    address = models.CharField(max_length=255)
    coordinates = models.CharField(max_length=255)  # You can use GeoDjango for more accurate geolocation handling

    def getAvailableVehicles(self):
        return Vehicle.objects.filter(location=self, isDefective=False)

    def __str__(self):
        return self.address

# Vehicle Model
class Vehicle(models.Model):
    vehicleID = models.AutoField(primary_key=True)
    type = models.CharField(max_length=50)
    batteryStatus = models.FloatField()
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True)
    isDefective = models.BooleanField(default=False)

    def updateLocation(self, newLocation):
        self.location = newLocation
        self.save()

    def updateBatteryStatus(self, newStatus):
        self.batteryStatus = newStatus
        self.save()

    def setDefectiveStatus(self, isDefective):
        self.isDefective = isDefective
        self.save()

    def __str__(self):
        return f'Vehicle {self.vehicleID} ({self.type})'

# Customer Model
class Customer(models.Model):
    customerID = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    accountBalance = models.FloatField()
    activeRental = models.OneToOneField('Rental', null=True, blank=True, on_delete=models.SET_NULL, related_name='active_customer')

    def rentVehicle(self, location, vehicleType):
        available_vehicle = Vehicle.objects.filter(location=location, type=vehicleType, isDefective=False).first()
        if available_vehicle:
            rental = Rental.objects.create(vehicle=available_vehicle, customer=self)
            self.activeRental = rental
            self.save()
            return True
        return False

    def returnVehicle(self, vehicle, location):
        if self.activeRental and self.activeRental.vehicle == vehicle:
            self.activeRental.endTime = models.DateTimeField(auto_now=True)
            self.activeRental.save()
            self.activeRental = None
            self.save()
            return True
        return False

    def reportDefective(self, vehicle):
        vehicle.setDefectiveStatus(True)
        return True

    def payCharges(self, amount):
        if self.accountBalance >= amount:
            self.accountBalance -= amount
            self.save()
            return True
        return False

    def __str__(self):
        return self.name

# Rental Model
class Rental(models.Model):
    rentalID = models.AutoField(primary_key=True)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='rentals')
    startTime = models.DateTimeField(auto_now_add=True)
    endTime = models.DateTimeField(null=True, blank=True)

    def calculateCharges(self):
        if self.endTime:
            duration = self.endTime - self.startTime
            return duration.total_seconds() / 3600 * 10  # Example: $10 per hour
        return 0

    def __str__(self):
        return f'Rental {self.rentalID} - {self.vehicle} rented by {self.customer}'

# Operator Model
class Operator(models.Model):
    operatorID = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)

    def trackVehicleLocation(self, vehicle):
        return vehicle.location

    def chargeVehicle(self, vehicle):
        vehicle.updateBatteryStatus(100)
        return True

    def repairVehicle(self, vehicle):
        vehicle.setDefectiveStatus(False)
        return True

    def moveVehicle(self, vehicle, newLocation):
        vehicle.updateLocation(newLocation)
        return True

    def __str__(self):
        return self.name

# VehicleActivity Model
class VehicleActivity(models.Model):
    activityID = models.AutoField(primary_key=True)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    activityType = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.activityType} on {self.vehicle} at {self.timestamp}'

# Report Model
class Report(models.Model):
    reportID = models.AutoField(primary_key=True)
    startDate = models.DateField()
    endDate = models.DateField()
    activities = models.ManyToManyField(VehicleActivity)

    def visualizeData(self):
        pass

    def __str__(self):
        return f'Report {self.reportID} - {self.startDate} to {self.endDate}'

# Manager Model
class Manager(models.Model):
    managerID = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)

    def generateVehicleReport(self, startDate, endDate):
        activities = VehicleActivity.objects.filter(timestamp__range=[startDate, endDate])
        report = Report.objects.create(startDate=startDate, endDate=endDate)
        report.activities.set(activities)
        return report

    def __str__(self):
        return self.name