from django.contrib import admin
from .models import (
    Visit,Department,Room,Bed,Area,
    ItemCategory,KitchenUnit,DietItem,
    MeasurementUnit,Doctor
)

admin.site.register(Visit)
admin.site.register(Department)
admin.site.register(Area)
admin.site.register(Room)
admin.site.register(Bed)
admin.site.register(ItemCategory)
admin.site.register(KitchenUnit)
admin.site.register(DietItem)
admin.site.register(MeasurementUnit)
admin.site.register(Doctor)
