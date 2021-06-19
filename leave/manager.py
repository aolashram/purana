from django.db import models

class ApprovedLeavesQuerySet(models.QuerySet):
    def total_leaves_type(self,leave_type,employee):
        return self.filter(leavetype=leave_type, employee=employee)
    
    def all_leaves_total(self, employee):
        return self.filter(employee=employee)

class ApprovedLeavesManager(models.Manager):
    def get_queryset(self):
        return ApprovedLeavesQuerySet(self.model, using=self._db)  # Important!
    
    def getAllLeavesTotal(self, employee):
        return self.get_queryset().all_leaves_total(employee)


    def getTotalSpecificLeave(self, leave_type, employee):
        leaves = self.get_queryset().total_leaves_type(leave_type, employee)
        tot = 0
        for lv in leaves:
            tot += lv.leaves_taken
        return tot

    def create_me(self, employee,leavetype,leavetaken,leaverequest):
        alm = self.create(employee=employee, leavetype=leavetype, leaves_taken=leavetaken, leaverequest=leaverequest)
        return alm

class LeaveTypeQuerySet(models.QuerySet):
    def leavetype_on_codes(self,code):
        return self.filter(code=code).first()
    
    def types(self):
        return self.all()

class LeaveTypeManager(models.Manager):
    def get_queryset(self):
        return LeaveTypeQuerySet(self.model, using=self._db)  # Important!
        
    def getLeaveTypeOnCode(self,code):
        return self.get_queryset().leavetype_on_codes(code)

    def getLeaveTypes(self):
        return self.get_queryset()

class LeavesAllottedTotalQuerySet(models.QuerySet):
    def get_total_leaves(self,employee,leave_type):
        return self.filter(leave_type=leave_type, employee=employee).first()
         
class LeavesAllottedTotalManager(models.Manager):
    def get_queryset(self):
        return LeavesAllottedTotalQuerySet(self.model, using=self._db)  # Important!

    def total(self,employee,leave_type):
        return self.get_queryset().get_total_leaves(employee,leave_type)

class LeaveRequestQuerySet(models.QuerySet):
    def get_pending_leave_requests(self,employee):
        return self.filter(employee=employee,leave_state='Pending')
    
    def get_lr_by_dept(self,department):
        return self.filter(employee__department=department)

    #def get_by_month(self,)


class LeavesRequestManager(models.Manager):
    def get_queryset(self):
        return LeaveRequestQuerySet(self.model, using=self._db)  # Important!

    def get_pending_leave_requests(self, employee):
        return self.get_queryset().get_pending_leave_requests(employee)

    def get_by_department(self, department):
        return self.get_queryset().get_lr_by_dept(department)