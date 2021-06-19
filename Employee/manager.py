from django.db import models

class EmployeeQuerySet(models.QuerySet):
    def get_staff(self,user):
        return self.filter(line_manager__user=user.id)
    
    def get_employee_user(self,user):
        return self.filter(user=user)

class EmployeeManager(models.Manager):
    def get_queryset(self):
        return EmployeeQuerySet(self.model, using=self._db)  # Important!
    
    def get_staff(self, user):
        return self.get_queryset().get_staff(user)
    
    def get_employee_user(self, user):
        return self.get_queryset().get_employee_user(user)

class LeaveApproverQuerySet(models.QuerySet):
    def get_approver(self,department,approver):
        return self.filter(department=department, approver__in=approver)[:1]

    def get_dept_for_approver(self,approver):
        return self.filter(approver=approver)

class LeaveApproverManager(models.Manager):
    def get_queryset(self):
        return LeaveApproverQuerySet(self.model, using=self._db)  # Important!
    
    def get_approver(self,department,approver):
        return self.get_queryset().get_approver(department,approver)

    def get_departments(self,approver):
        return self.get_queryset().get_dept_for_approver(approver)