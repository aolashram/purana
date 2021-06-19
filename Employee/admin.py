from django.contrib import admin

from Employee.models import (
    Designation,
    Department,
    Country,
    State,
    Employee,
    District,
    LeaveApprover
)

admin.site.register(Designation)
admin.site.register(Department)
admin.site.register(Country)
admin.site.register(State)
admin.site.register(Employee)
admin.site.register(District)
admin.site.register(LeaveApprover)

