from django.db import models

class Devicelogs42021(models.Model):
    use_db = 'second'
    devicelogid = models.IntegerField(db_column='DeviceLogId',primary_key=True)  
    downloaddate = models.DateTimeField(db_column='DownloadDate', blank=True, null=True)  
    deviceid = models.IntegerField(db_column='DeviceId', blank=True, null=True)  
    userid = models.CharField(db_column='UserId', max_length=50, blank=True, null=True)  
    logdate = models.DateTimeField(db_column='LogDate', blank=True, null=True)  
    direction = models.CharField(db_column='Direction', max_length=100, blank=True, null=True)  
    attdirection = models.CharField(db_column='AttDirection', max_length=255, blank=True, null=True)  
    c1 = models.CharField(db_column='C1', max_length=255, blank=True, null=True)  
    c2 = models.CharField(db_column='C2', max_length=255, blank=True, null=True)  
    c3 = models.CharField(db_column='C3', max_length=255, blank=True, null=True)  
    c4 = models.CharField(db_column='C4', max_length=255, blank=True, null=True)  
    c5 = models.CharField(db_column='C5', max_length=255, blank=True, null=True)  
    c6 = models.CharField(db_column='C6', max_length=255, blank=True, null=True)  
    c7 = models.CharField(db_column='C7', max_length=255, blank=True, null=True)  
    workcode = models.CharField(db_column='WorkCode', max_length=100, blank=True, null=True)  
    updateflag = models.IntegerField(db_column='UpdateFlag', blank=True, null=True)  
    isapproved = models.IntegerField(db_column='IsApproved', blank=True, null=True)  
    employeeimage = models.TextField(db_column='EmployeeImage', blank=True, null=True)  
    filename = models.CharField(db_column='FileName', max_length=255, blank=True, null=True)  
    longitude = models.CharField(db_column='Longitude', max_length=255, blank=True, null=True)  
    latitude = models.CharField(db_column='Latitude', max_length=255, blank=True, null=True)  
    createddate = models.DateTimeField(db_column='CreatedDate', blank=True, null=True)  
    lastmodifieddate = models.DateTimeField(db_column='LastModifiedDate', blank=True, null=True)  
    locationaddress = models.CharField(db_column='LocationAddress', max_length=4000, blank=True, null=True)  
    bodytemperature = models.FloatField(db_column='BodyTemperature', blank=True, null=True)  
    is_maskon = models.IntegerField(db_column='IsMaskOn', blank=True, null=True)  

    def __str__(self):
        return self.userid + " : " + str(self.logdate)

    class Meta:
        managed = False
        db_table = 'DeviceLogs_4_2021'

class Ins(models.Model):
    ins = models.CharField(max_length=20)


class Devicelogs(models.Model):
    devicelogid = models.IntegerField(primary_key=True)  
    downloaddate = models.DateTimeField(blank=True, null=True)  
    deviceid = models.IntegerField(blank=True, null=True)  
    userid = models.CharField(max_length=50, blank=True, null=True)  
    logdate = models.DateTimeField(blank=True, null=True)  
    direction = models.CharField(max_length=100, blank=True, null=True)  
    attdirection = models.CharField(max_length=255, blank=True, null=True)  
    c1 = models.CharField(max_length=255, blank=True, null=True)  
    c2 = models.CharField(max_length=255, blank=True, null=True)  
    c3 = models.CharField(max_length=255, blank=True, null=True)  
    c4 = models.CharField(max_length=255, blank=True, null=True)  
    c5 = models.CharField(max_length=255, blank=True, null=True)  
    c6 = models.CharField(max_length=255, blank=True, null=True)  
    c7 = models.CharField(max_length=255, blank=True, null=True)  
    workcode = models.CharField(max_length=100, blank=True, null=True)  
    updateflag = models.IntegerField(blank=True, null=True)  
    isapproved = models.IntegerField(blank=True, null=True)  
    employeeimage = models.TextField(blank=True, null=True)  
    filename = models.CharField(max_length=255, blank=True, null=True)  
    longitude = models.CharField(max_length=255, blank=True, null=True)  
    latitude = models.CharField(max_length=255, blank=True, null=True)  
    createddate = models.DateTimeField(blank=True, null=True)  
    lastmodifieddate = models.DateTimeField(blank=True, null=True)  
    locationaddress = models.CharField(max_length=4000, blank=True, null=True)  
    bodytemperature = models.FloatField(blank=True, null=True)  
    is_maskon = models.IntegerField(blank=True, null=True)  

    def __str__(self):
        return self.userid + " : " + self.logdate