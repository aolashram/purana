from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models

class Role(models.Model):
    '''
    The Role entries are managed by the system,
    automatically created via a Django data migration.
    '''
    EMPLOYEE = 1
    SUPERVISOR = 2
    MANAGER = 3
    HREXEC = 4
    HOD = 5
    HRHEAD = 6 
    ADMIN_OFFICER = 7
    CAO = 8
    ROLE_CHOICES = (
        (EMPLOYEE, 'Employee'),
        (SUPERVISOR,'Supervisor'),
        (MANAGER, 'Manager'),
        (HREXEC, 'HR Executive'),
        (HOD, 'Hod'),
        (HRHEAD,'HR Head'),
        (ADMIN_OFFICER, 'Administraive Officer'),
        (CAO, 'CAO'),
    )

    id = models.PositiveSmallIntegerField(primary_key=True)
    #name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

class User(AbstractUser):
    roles = models.ManyToManyField(Role)

