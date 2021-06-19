import datetime
from django.db.models.fields import related
from django.utils import timezone
from django.urls import reverse
from django.db import models
from Employee.models import Employee
from accounts.models import User


class Holidays(models.Model):
    name = models.CharField(max_length=30)
    holiday = models.DateField()
    desciption = models.CharField(max_length=200,null=True,blank=True)
    created_by = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name

class Shift(models.Model):
    ENABLE_CHOICES = (
        (True, 'Enable'),
        (False, 'Disable')
    )   
    WEEKEND_CHOICES = (
        ('l','Location based'),
        ('s','Shift based'),
    )
    SHIFT_TYPES = (
        ('Flexible-day', 'Flexible(Day)'),
        ('Flexible-night', 'Flexible(Night)'),
        ('fixed-shift-time','Fixed Shift Time'),
    )
    name = models.CharField(max_length=20,null=True, blank=True)
    shift_from = models.TimeField(null=True, blank=True)
    shift_to = models.TimeField(null=True,blank=True)
    shift_margin = models.BooleanField(choices=ENABLE_CHOICES)  
    margin_before = models.TimeField(null=True,blank=True)
    margin_after = models.TimeField(null=True,blank=True)
    shift_type = models.CharField(max_length=35,choices=SHIFT_TYPES)
    created_by = models.ForeignKey(User, on_delete=models.DO_NOTHING,null=True,blank=True,related_name='createdusers')
    created_date = models.DateTimeField(default=timezone.now)
    updated_by = models.ForeignKey(User, on_delete=models.DO_NOTHING,null=True,blank=True,related_name='updatedusers')
    updated_date = models.DateTimeField(null=True,blank=True)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('eattendance:shift-detail', args=[self.id])

class Roster(models.Model):
    YES_NO_CHOICES = (
        (True, 'Yes'),
        (False, 'No')
    )   
    employee = models.ForeignKey(Employee,on_delete=models.DO_NOTHING)
    roster_date = models.DateField(null=True)
    is_weekend = models.BooleanField(choices=YES_NO_CHOICES)
    shift = models.ForeignKey(Shift,on_delete=models.DO_NOTHING)
    created_by = models.ForeignKey(User, on_delete=models.DO_NOTHING,related_name='createdrosterusers')
    created_date = models.DateTimeField(default=timezone.now)
    updated_by = models.ForeignKey(User, on_delete=models.DO_NOTHING,null=True,blank=True,related_name='updatedrosterusers')
    updated_date = models.DateTimeField(default=timezone.now,null=True,blank=True)

class DailyAttendance(models.Model):
    in_time = models.DateTimeField(null=True)
    out_time = models.DateTimeField(null=True)
    employee = models.ForeignKey(Employee,on_delete=models.DO_NOTHING)
    created_by = models.ForeignKey(User, on_delete=models.DO_NOTHING,related_name='cbdausers')
    created_date = models.DateTimeField(default=timezone.now)
    updated_by = models.ForeignKey(User, on_delete=models.DO_NOTHING,null=True,blank=True,related_name='updatedadusers')
    updated_date = models.DateTimeField(default=timezone.now,null=True,blank=True)