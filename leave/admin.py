from django.contrib import admin

from leave.models import (
    LeaveType,
    LeavesAllottedTotal,
)


admin.site.register(LeaveType)
admin.site.register(LeavesAllottedTotal)
