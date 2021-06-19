from datetime import date, timezone
from django.db import models
from django.utils.translation import ugettext as _
from accounts.models import User
from django.utils import timezone
from datetime import datetime
from django.utils import timezone
from Employee.models import Employee
from .manager import ApprovedLeavesManager,LeaveTypeManager,LeavesAllottedTotalManager,LeavesRequestManager


# Model script


class LeaveType(models.Model):
    YES='YES'
    NO='NO'
    CANAPPLY = (
        (YES,YES),
        (NO,NO),
    )
    name = models.CharField(max_length=40)
    year = models.CharField(max_length=9)
    maximum_leaves = models.IntegerField()
    can_apply = models.CharField(max_length=3, choices=CANAPPLY)
    code=models.CharField(max_length=9)
    objects = LeaveTypeManager()
    def __str__(self):
        return self.name

class LeavesAllottedTotal(models.Model):
    leave_type = models.ForeignKey(LeaveType, on_delete=models.CASCADE)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    year = models.CharField(max_length=9)
    total_leaves = models.IntegerField()
    objects = LeavesAllottedTotalManager()

    def __str__(self):
        return self.leave_type.name


class LeaveRequest(models.Model):
    APPROVED = 'Approved'
    PENDING = 'Pending'
    REJECTED = 'Rejected'
    CANCELLED = 'Cancelled'
    YES='YES'
    NO='NO'
    NA = 'NA'
    LEAVE_STATUS = (
        (APPROVED,APPROVED),
        (PENDING,PENDING),
        (REJECTED,REJECTED)
    )
    YESNO = (
        (YES,YES),
        (NO,NO)
    )
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    leavefrom = models.DateField()
    leavetill = models.DateField()
    purpose = models.CharField(max_length=100,null=True,blank=True)
    applied_date = models.DateField(default=timezone.now)
    comments = models.TextField(null=True, blank=True)
    is_sick = models.CharField(max_length=3,choices=YESNO)
    first_approver_status = models.CharField(max_length=12, choices=LEAVE_STATUS,null=True, blank=True)
    second_approver_status = models.CharField(max_length=12, choices=LEAVE_STATUS,null=True, blank=True)
    third_approver_status = models.CharField(max_length=12, choices=LEAVE_STATUS,null=True, blank=True)
    first_approver_remark = models.TextField(null=True, blank=True)
    second_approver_remark = models.TextField(null=True, blank=True)
    third_approver_remark = models.TextField(null=True, blank=True)
    #Overal state of a leave request independent of approvers
    leave_state = models.CharField(max_length=12, default=PENDING)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    objects = LeavesRequestManager()

    def __str__(self):
        return self.leave_state

    @property
    def get_next_approver(self):
        if(first_approver_status==PENDING):
            return '1'
        elif(second_approver_status==PENDING):
            return '2'
        elif(third_approver_status==PENDING):
            return '3'
        else:
            return '0'

    @property
    def is_leave_today(self):
        today = date.today()
        if (today >= self.leavefrom and today <= self.leavetill):
            return True
        return False

    @property
    def get_leave_duration(self):
        leave_days = self.leavetill-self.leavefrom
        return leave_days.days+1

class ApprovedLeaves(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    leavetype = models.ForeignKey(LeaveType, on_delete=models.CASCADE)
    leaves_taken = models.DecimalField(max_digits=3,decimal_places=1)
    leaverequest = models.ForeignKey(LeaveRequest, on_delete=models.CASCADE)
    objects = ApprovedLeavesManager()

class LeaveAudit(models.Model):
    action = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    created = models.DateTimeField(default=timezone.now)