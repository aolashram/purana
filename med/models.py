from django.db.models.base import Model
from django.db.models.deletion import DO_NOTHING
from django.utils import timezone
from django.db import models
from accounts.models import User

# Create your models here.
class Department(models.Model):
    name = models.CharField(max_length=25)

    def __str__(self):
        return self.name

class Doctor(models.Model):
    name = models.CharField(max_length=25)
    department = models.ForeignKey(Department,on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.name

class Area(models.Model):
    name = models.CharField(max_length=25)

    def __str__(self):
        return self.name

class Room(models.Model):
    roomno = models.CharField(max_length=10)
    area = models.ForeignKey(Area,on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.roomno

class Bed(models.Model):
    bedno = models.CharField(max_length=10)
    room = models.ForeignKey(Room, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.bedno

class Patient(models.Model):
    MALE='Male'
    FEMALE='Female'
    OTHER = 'Other'
    GENDER = (
        (MALE,MALE),
        (FEMALE,FEMALE),
        (OTHER,OTHER),
    )
    fullname = models.CharField(max_length=120)
    mrno = models.CharField(max_length=15)
    gender = models.CharField(max_length=10,choices=GENDER)
    age = models.IntegerField()
    created_by = models.ForeignKey(User, on_delete=models.DO_NOTHING,null=True,blank=True,related_name='ptcreatedusers')
    created_date = models.DateTimeField(default=timezone.now)
    updated_by = models.ForeignKey(User, on_delete=models.DO_NOTHING,null=True,blank=True,related_name='ptupdatedusers')
    updated_date = models.DateTimeField(null=True,blank=True)

    def __str__(self):
        return self.fullname

class Visit(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    ipno = models.CharField(max_length=10,unique=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    building_floor = models.ForeignKey(Area, on_delete=models.DO_NOTHING)
    room = models.ForeignKey(Room, on_delete=models.DO_NOTHING)
    bedno = models.ForeignKey(Bed, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.patient.fullname

class KitchenUnit(models.Model):
    YES_NO = (
        (True,'Yes'),
        (False,'No'),
    )
    unit = models.CharField(max_length=50)
    active = models.BooleanField(choices=YES_NO)
    description = models.CharField(max_length=300,blank=True, null=True)

    def __str__(self):
        return self.unit

class MeasurementUnit(models.Model):
    MEASUREMENT = (
        ('Milligram','Milligram'),
        ('Gram','Gram'),
        ('Kilogram','Kilogram'),
        ('Milliliter','Milliliter'),
        ('Liter','Liter'),
        ('Bowl-Small','Bowl-Small'),
        ('Bowl-Medium','Bowl-Medium'),
        ('Bowl-Large','Bowl-Large'),
    )
    measurement = models.CharField(max_length=20,choices=MEASUREMENT)
    code = models.CharField(max_length=3)

    def __str__(self):
        return self.measurement

class ItemCategory(models.Model):
    YES_NO = (
        (True,'Yes'),
        (False,'No'),
    )
    category = models.CharField(max_length=30,blank=False, null=False)
    description = models.CharField(max_length=300,blank=True, null=True)
    active = models.BooleanField(choices=YES_NO)

    def __str__(self):
        return self.category

class DietItem(models.Model):
    YES_NO = (
        (True,'Yes'),
        (False,'No'),
    )
    item_name = models.CharField(max_length=60)
    item_category = models.ForeignKey(ItemCategory, on_delete=models.DO_NOTHING)
    kitchen_unit = models.ForeignKey(KitchenUnit, on_delete=models.DO_NOTHING)
    measurement_unit = models.ForeignKey(MeasurementUnit, on_delete=DO_NOTHING)
    default_unit_value = models.IntegerField(default=1)
    rate = models.DecimalField(max_digits=5, decimal_places=2)
    active = models.BooleanField(choices=YES_NO)

    def __str__(self):
        return self.item_name + ' (' + str(self.measurement_unit) + ')'

class DietOrder(models.Model):
    DIET_SLOT = (
        ('Breakfast','Breakfast'),
        ('Lunch','Lunch'),
        ('Dinner','Dinner'),
        ('Special','Special'),
    )
    patient = models.ForeignKey(Visit,on_delete=models.DO_NOTHING)
    category = models.ForeignKey(ItemCategory,on_delete=DO_NOTHING)
    item = models.ForeignKey(DietItem, on_delete=DO_NOTHING)
    quantity = models.IntegerField(default=1)
    special_instruction = models.CharField(max_length=300,null=True,blank=True)
    slot = models.CharField(max_length=20, choices=DIET_SLOT)
    delivery_date = models.DateField()
    created_by = models.ForeignKey(User, on_delete=models.DO_NOTHING,null=True,blank=True,related_name='dtcreatedusers')
    created_date = models.DateTimeField(default=timezone.now)
    updated_by = models.ForeignKey(User, on_delete=models.DO_NOTHING,null=True,blank=True,related_name='dtupdatedusers')
    updated_date = models.DateTimeField(null=True,blank=True)