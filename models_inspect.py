# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class DjangoAdminLog(models.Model):
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey('AuthUser', models.DO_NOTHING)
    action_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    name = models.CharField(max_length=100)
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class MyappCustomer(models.Model):
    customerid = models.AutoField(db_column='customerID', primary_key=True)  # Field name made lowercase.
    name = models.CharField(max_length=100)
    accountbalance = models.FloatField(db_column='accountBalance')  # Field name made lowercase.
    activerental = models.OneToOneField('MyappRental', models.DO_NOTHING, db_column='activeRental_id', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'myapp_customer'


class MyappLocation(models.Model):
    locationid = models.AutoField(db_column='locationID', primary_key=True)  # Field name made lowercase.
    address = models.CharField(max_length=255)
    coordinates = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'myapp_location'


class MyappManager(models.Model):
    managerid = models.AutoField(db_column='managerID', primary_key=True)  # Field name made lowercase.
    name = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'myapp_manager'


class MyappOperator(models.Model):
    operatorid = models.AutoField(db_column='operatorID', primary_key=True)  # Field name made lowercase.
    name = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'myapp_operator'


class MyappRental(models.Model):
    rentalid = models.AutoField(db_column='rentalID', primary_key=True)  # Field name made lowercase.
    starttime = models.DateTimeField(db_column='startTime')  # Field name made lowercase.
    endtime = models.DateTimeField(db_column='endTime', blank=True, null=True)  # Field name made lowercase.
    customer = models.ForeignKey(MyappCustomer, models.DO_NOTHING)
    vehicle = models.ForeignKey('MyappVehicle', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'myapp_rental'


class MyappReport(models.Model):
    reportid = models.AutoField(db_column='reportID', primary_key=True)  # Field name made lowercase.
    startdate = models.DateField(db_column='startDate')  # Field name made lowercase.
    enddate = models.DateField(db_column='endDate')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'myapp_report'


class MyappReportActivities(models.Model):
    report = models.ForeignKey(MyappReport, models.DO_NOTHING)
    vehicleactivity = models.ForeignKey('MyappVehicleactivity', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'myapp_report_activities'
        unique_together = (('report', 'vehicleactivity'),)


class MyappVehicle(models.Model):
    vehicleid = models.AutoField(db_column='vehicleID', primary_key=True)  # Field name made lowercase.
    type = models.CharField(max_length=50)
    batterystatus = models.FloatField(db_column='batteryStatus')  # Field name made lowercase.
    isdefective = models.BooleanField(db_column='isDefective')  # Field name made lowercase.
    location = models.ForeignKey(MyappLocation, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'myapp_vehicle'


class MyappVehicleactivity(models.Model):
    activityid = models.AutoField(db_column='activityID', primary_key=True)  # Field name made lowercase.
    activitytype = models.CharField(db_column='activityType', max_length=100)  # Field name made lowercase.
    timestamp = models.DateTimeField()
    vehicle = models.ForeignKey(MyappVehicle, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'myapp_vehicleactivity'


class CustomerLogin(models.Model):
    email = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    name = models.CharField(max_length=100)

    class Meta:
        db_table = 'user'
        managed = False

    def __str__(self):
        return self.email

    def check_password(self, raw_password):

        return self.password == raw_password
