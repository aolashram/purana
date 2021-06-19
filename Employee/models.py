import datetime
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from accounts.models import User
from django.utils.translation import ugettext as _
from django.urls import reverse
from .manager import EmployeeManager,LeaveApproverManager

# Create your models here.
class Department(models.Model):
    name = models.CharField(max_length=60)
    desc = models.CharField(max_length=100)
   
    def __str__(self):
        return self.name


class Designation(models.Model):
    name = models.CharField(max_length=60)
    #How many approvals needed to get a leave sanctioned
    leave_approve_level_depth = models.IntegerField()

    def __str__(self):
        return self.name

class Country(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class State(models.Model):
    name = models.CharField(max_length=100)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class District(models.Model):
    name = models.CharField(max_length=100)
    state = models.ForeignKey(State, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class City(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Address(models.Model):
    address = models.TextField()
    district = models.ForeignKey(District, on_delete=models.CASCADE)
    state = models.ForeignKey(State, on_delete=models.CASCADE)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    pincode = models.CharField(max_length=6)

    class Meta:
        abstract = True

class BankInfo(models.Model):
    bank_name = models.CharField(max_length=150, blank=True, null=True)
    branch_name = models.CharField(max_length=100, blank=True, null=True)
    ifsc_code = models.CharField(max_length=20, blank=True, null=True)
    account_no = models.CharField(max_length=40, blank=True, null=True) 

    class Meta:
        abstract = True

class Person(Address):
    SINGLE = 'SI'
    MARRIED = 'MA'
    WIDOWED = 'WI'
    DIVORCED = 'DI'
    SEPERATED = 'SE'
    MALE = 'M'
    FEMALE = 'F'
    OTHERTYPE = 'O'
    MR = '1'
    MS = '2'
    MRS = '3'
    DR = '4'

    MARITAL_STATUS = (
        (SINGLE,'Single'),
        (MARRIED,'Married'),
        (WIDOWED,'Widowed'),
        (DIVORCED,'Divorced'),
        (SEPERATED,'Seperated'),
    )
    GENDERS = (
        (MALE, 'Male'),
        (FEMALE, 'Female'),
        (OTHERTYPE, 'Other'),
    )
    TITLES = (
        (MR, 'Mr.'),
        (MRS, 'Mrs.'),
        (MS, 'Ms.'),
        (DR, 'Dr.'),
    )
    title = models.CharField(max_length=1, choices=TITLES,null=True)
    first_name = models.CharField(max_length=60)
    middle_name = models.CharField(max_length=60, null=True, blank=True)
    last_name = models.CharField(max_length=60)
    sur_name = models.CharField(max_length=50, null=True, blank=True)  
    date_of_birth = models.DateField(null=False)
    gender = models.CharField(max_length=10, choices=GENDERS)
    email = models.EmailField(null=True,blank=True)
    marital_status = models.CharField(max_length=2, choices=MARITAL_STATUS)
    phone_number = PhoneNumberField()
    aadhaar_number = models.CharField(max_length=20)
    pan_number = models.CharField(max_length=10)
    qualification = models.TextField()
    father_name = models.CharField(max_length=100)
    mother_name = models.CharField(max_length=100)
    registration_details = models.TextField()

    class Meta:
        abstract = True


class Employee(Person,BankInfo):
    CONFIRMED = 'Confirmed'
    PROBATION = 'Probation'
    TRAINING = 'Training'
    SUSPENDED = 'Suspended'
    TERMINATED = 'Terminated'
    RESIGNED = 'Resigned'
    RETIRED = 'Retired'
    EMPLOYEMENT_STATUS =(
        (CONFIRMED,'Confirmed'),
        (PROBATION,'Probation'),
        (TRAINING,'Training'),
        (SUSPENDED,'Suspended'),
        (TERMINATED,'Terminated'),
        (RESIGNED,'Resigned'),
        (RETIRED,'Retired'),
    )
    CCIM_YES = 'Y'
    CCIM_NO = 'N'
    CCIM_STATUS = (
        (CCIM_YES, 'YES'),
        (CCIM_NO, 'No')
    )
    YES_NO_CHOICES = (
        (True, 'Yes'),
        (False, 'No')
    )  
    emp_code = models.CharField(max_length=20)
    department = models.ForeignKey(Department, on_delete=models.DO_NOTHING)
    designation = models.ForeignKey(Designation, on_delete=models.CASCADE)
    ccim_employment_status = models.CharField(max_length=1, default=CCIM_NO, choices=CCIM_STATUS)
    date_of_join = models.DateField(null=False)
    date_of_confirmation = models.DateField(null=True,blank=True)
    employment_status = models.CharField(max_length=20)
    pf_number = models.CharField(max_length=20, null=True, blank=True)
    esi_number = models.CharField(max_length=20, null=True, blank=True)
    line_manager = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(verbose_name=_('Created'),auto_now_add=True)
    updated = models.DateTimeField(verbose_name=_('Updated'),auto_now=True)
    active = models.BooleanField(choices=YES_NO_CHOICES,default=True)
    objects = EmployeeManager()

    class Meta:
        verbose_name = _('Employee')
        verbose_name_plural = _('Employees')
        ordering = ['-created']

    def __str__(self):
        return self.get_full_name

    @property
    def get_full_name(self):
        fullname = ''
        first_name = self.first_name
        last_name = self.last_name
        middle_name = self.middle_name

        if (first_name and last_name) or middle_name is None:
            fullname = first_name +' '+ last_name
            return fullname
        elif middle_name:
            fullname = first_name + ' '+ last_name +' '+middle_name
            return fullname
        return

    @property
    def get_age(self):
        current_year = datetime.date.today().year
        dateofbirth_year = self.date_of_birth.year
        if dateofbirth_year:
            return current_year - dateofbirth_year
        return
    
    @property
    def birthday_today(self):
        '''
        returns True, if birthday is today else False
        '''
        return self.birthday.day == datetime.date.today().day

    def get_absolute_url(self):
        return reverse("Employee:employee-detail", kwargs={"id": self.id})

class LeaveApprover(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='depatments')
    approver = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='approvers')
    position = models.IntegerField()
    objects=LeaveApproverManager()
    # leave_approver1 = models.ForeignKey(Employee, on_delete=models.CASCADE, null=True, blank=True,related_name= 'first_approvers')
    # leave_approver2 = models.ForeignKey(Employee, on_delete=models.CASCADE, null=True, blank=True,related_name='second_approvers')
    # leave_approver3 = models.ForeignKey(Employee, on_delete=models.CASCADE, null=True, blank=True,related_name='third_approvers')

    def __str__(self):
        return self.department.name
