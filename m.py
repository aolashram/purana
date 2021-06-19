# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Devicelogs42021(models.Model):
    devicelogid = models.IntegerField(db_column='DeviceLogId')  # Field name made lowercase.
    downloaddate = models.DateTimeField(db_column='DownloadDate', blank=True, null=True)  # Field name made lowercase.
    deviceid = models.IntegerField(db_column='DeviceId', blank=True, null=True)  # Field name made lowercase.
    userid = models.CharField(db_column='UserId', max_length=50, blank=True, null=True)  # Field name made lowercase.
    logdate = models.DateTimeField(db_column='LogDate', blank=True, null=True)  # Field name made lowercase.
    direction = models.CharField(db_column='Direction', max_length=100, blank=True, null=True)  # Field name made lowercase.
    attdirection = models.CharField(db_column='AttDirection', max_length=255, blank=True, null=True)  # Field name made lowercase.
    c1 = models.CharField(db_column='C1', max_length=255, blank=True, null=True)  # Field name made lowercase.
    c2 = models.CharField(db_column='C2', max_length=255, blank=True, null=True)  # Field name made lowercase.
    c3 = models.CharField(db_column='C3', max_length=255, blank=True, null=True)  # Field name made lowercase.
    c4 = models.CharField(db_column='C4', max_length=255, blank=True, null=True)  # Field name made lowercase.
    c5 = models.CharField(db_column='C5', max_length=255, blank=True, null=True)  # Field name made lowercase.
    c6 = models.CharField(db_column='C6', max_length=255, blank=True, null=True)  # Field name made lowercase.
    c7 = models.CharField(db_column='C7', max_length=255, blank=True, null=True)  # Field name made lowercase.
    workcode = models.CharField(db_column='WorkCode', max_length=100, blank=True, null=True)  # Field name made lowercase.
    updateflag = models.IntegerField(db_column='UpdateFlag', blank=True, null=True)  # Field name made lowercase.
    isapproved = models.IntegerField(db_column='IsApproved', blank=True, null=True)  # Field name made lowercase.
    employeeimage = models.TextField(db_column='EmployeeImage', blank=True, null=True)  # Field name made lowercase.
    filename = models.CharField(db_column='FileName', max_length=255, blank=True, null=True)  # Field name made lowercase.
    longitude = models.CharField(db_column='Longitude', max_length=255, blank=True, null=True)  # Field name made lowercase.
    latitude = models.CharField(db_column='Latitude', max_length=255, blank=True, null=True)  # Field name made lowercase.
    createddate = models.DateTimeField(db_column='CreatedDate', blank=True, null=True)  # Field name made lowercase.
    lastmodifieddate = models.DateTimeField(db_column='LastModifiedDate', blank=True, null=True)  # Field name made lowercase.
    locationaddress = models.CharField(db_column='LocationAddress', max_length=4000, blank=True, null=True)  # Field name made lowercase.
    bodytemperature = models.FloatField(db_column='BodyTemperature', blank=True, null=True)  # Field name made lowercase.
    ismaskon = models.IntegerField(db_column='IsMaskOn', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'DeviceLogs_4_2021'
