from django.db import models
from django.contrib.auth.hashers import make_password, check_password
from django.utils import timezone


# UserType Model
class UserType(models.Model):
    typeID = models.AutoField(primary_key=True)
    typeName = models.CharField(max_length=50)

    def __str__(self):
        return self.typeName

# Operator Model
class Operator(models.Model):
    operatorID = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    password = models.CharField(max_length=128)  # Storing hashed password
    userType = models.ForeignKey(UserType, on_delete=models.CASCADE, null=True, blank=True)

    def set_password(self, raw_password):
        self.password = make_password(raw_password)
        self.save()

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    def trackVehicleLocation(self, vehicle):
        return {'latitude': vehicle.latitude, 'longitude': vehicle.longitude}

    def chargeVehicle(self, vehicle):
        vehicle.updateBatteryStatus(100)
        return True

    def repairVehicle(self, vehicle):
        vehicle.setDefectiveStatus(False)
        return True

    def moveVehicle(self, vehicle, newLatitude, newLongitude):
        vehicle.updateLocation(newLatitude, newLongitude)
        return True

    def __str__(self):
        return self.name

# Manager Model
class Manager(models.Model):
    managerID = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    password = models.CharField(max_length=128)  # Storing hashed password
    userType = models.ForeignKey(UserType, on_delete=models.CASCADE, null=True, blank=True)

    def set_password(self, raw_password):
        self.password = make_password(raw_password)
        self.save()

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    def generateVehicleReport(self, startDate, endDate):
        activities = VehicleActivity.objects.filter(timestamp__range=[startDate, endDate])
        report = Report.objects.create(startDate=startDate, endDate=endDate)
        report.activities.set(activities)
        return report

    def __str__(self):
        return self.name

# Customer Model
class Customer(models.Model):
    customerID = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    password = models.CharField(max_length=128)  # Storing hashed password
    accountBalance = models.FloatField()
    activeRental = models.OneToOneField('Rental', null=True, blank=True, on_delete=models.SET_NULL, related_name='active_customer')
    userType = models.ForeignKey(UserType, on_delete=models.CASCADE, null=True, blank=True)

    def set_password(self, raw_password):
        self.password = make_password(raw_password)
        self.save()

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    def rentVehicle(self, latitude, longitude, vehicleType):
        available_vehicle = Vehicle.objects.filter(latitude=latitude, longitude=longitude, type=vehicleType, isDefective=False).first()
        if available_vehicle:
            rental = Rental.objects.create(vehicle=available_vehicle, customer=self)
            self.activeRental = rental
            self.save()
            return True
        return False

    def returnVehicle(self, vehicle, latitude, longitude):
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

class Location(models.Model):
    locationID = models.AutoField(primary_key=True)
    address = models.CharField(max_length=255)

    position_x = models.FloatField()
    position_y = models.FloatField()

    def getAvailableVehicles(self):
        return Vehicle.objects.filter(location=self, isDefective=False)

    def __str__(self):
        return self.address

# Vehicle Model
class Vehicle(models.Model):
    vehicleID = models.AutoField(primary_key=True)
    TYPE_CHOICES = [
        ('e_bike', 'Electric Bike'),
        ('scooter', 'Electric Scooter'),
    ]
    type = models.CharField(max_length=50, choices=TYPE_CHOICES)
    batteryStatus = models.FloatField()
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True)
    isDefective = models.BooleanField(default=False)
    cost_per_minute = models.DecimalField(max_digits=5, decimal_places=2, default=0.2)
    position_x=models.FloatField()
    position_y=models.FloatField()
    range = models.FloatField()

    def save(self, *args, **kwargs):
        if self.type == 'e_bike':
            self.cost_per_minute = 0.2
        elif self.type == 'scooter':
            self.cost_per_minute = 0.1
        elif self.type == 'scooter':
            self.cost_per_minute = 0.1
        elif self.type == 'scooter':
            self.cost_per_minute = 0.1
        super().save(*args, **kwargs)

    def updateRange(self, newRange):
        self.range = newRange
        self.save()

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

import threading
from django.utils import timezone
from datetime import timedelta, time


# Rental Model
class Rental(models.Model):
    rentalID = models.AutoField(primary_key=True)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    customer = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='rentals')
    startTime = models.DateTimeField(auto_now_add=True)
    endTime = models.DateTimeField(null=True, blank=True)
    startlocation = models.ForeignKey(Location, on_delete=models.CASCADE, null=True, related_name='start_rentals')
    endlocation = models.ForeignKey(Location, on_delete=models.CASCADE, null=True, related_name='end_rentals')

    def calculateCharges(self):
        if self.endTime:
            duration = self.endTime - self.startTime
            duration_in_minutes = duration.total_seconds() / 60
            rate = 0.2 if self.vehicle.type == 'e_bike' else 0.1
            return round(duration_in_minutes * rate, 2)
        return 0

    def complete_rental(self):
        self.endTime = timezone.now()
        self.save()
        amount = self.calculateCharges()
        payment, created = Payment.objects.get_or_create(
            rental=self,
            defaults={'amount': amount, 'is_paid': False}
        )
        if not created:
            payment.amount = amount
            payment.save()

        return payment

    def __str__(self):
        return f'Rental {self.rentalID} - {self.vehicle} rented by {self.customer}'



    def update_vehicle_status(rental):
        vehicle = rental.vehicle
        battery_drain_rate = 1 if vehicle.type == 'e_bike' else 5
        range_drain_rate = battery_drain_rate * 5

        interval = 1

        def update():
            nonlocal interval
            while True:
                current_time = timezone.now()
                elapsed_time = (current_time - rental.startTime).total_seconds()


                if rental.endTime or vehicle.batteryStatus <= 0:
                    break

                vehicle.batteryStatus = max(0, vehicle.batteryStatus - battery_drain_rate)
                vehicle.range = max(0, vehicle.range - range_drain_rate)
                vehicle.save()

                time.sleep(interval)

        thread = threading.Thread(target=update)
        thread.start()
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

class Payment(models.Model):
    paymentID = models.AutoField(primary_key=True)
    rental = models.OneToOneField(Rental, on_delete=models.CASCADE)
    cardNumber = models.CharField(max_length=16)
    expiryDate = models.CharField(max_length=5)
    amount = models.DecimalField(max_digits=6, decimal_places=2)
    is_paid = models.BooleanField(default=False)

    def save(self, *args, **kwargs):

        if len(self.cardNumber) == 16:
            self.cardNumber = self.cardNumber[-4:]
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Payment {self.paymentID} for Rental {self.rental.rentalID}'