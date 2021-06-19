from django.db import models
from med.models import Visit

class DietItemCategory(models.Model):
    name = models.CharField(models.Model)
    def __str__(self):
        retun self.name

class DietType(models.Model):
    name = models.CharField(models.Model)
    def __str__(self):
        retun self.name

class DietItem(models.Model):                
    name = models.CharField(max_length=120)
    category = models.ForeignKey(DietItemCategory, on_delete=DO_NOTHING)
    dietype= models.ForeignKey(DietType, on_delete=DO_NOTHING)
    rate = models.DecimalField(max_digits=10, decimal_places=2)

class DietChart(models.Model):
    MORNING = 'Morning'
    LUNCH = 'Lunch'
    DINNER = 'Dinner'
    SPECIAL = 'Special'
    SLOT = (
        (MORNING,MORNING),
        (LUNCH,LUNCH),
        (DINNER,DINNER),
        (SPECIAL,SPECIAL),
    )
    patient = models.ForeignKey(Visit, on_delete=CASCADE)
    diet_item = models.ForeignKey(DietItem, on_delete=CASCADE)
    slot = models.ForeignKey(models.CharField(max_length=15,choices=SLOT))
    instructions = models.TextField(null=True, blank=True)
    time=models.TimeField(null=True, blank=True)
