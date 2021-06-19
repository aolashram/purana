from Employee.models import LeaveApprover,Employee
import datetime
from django.shortcuts import render,HttpResponseRedirect,get_object_or_404
from ..forms import RosterCreateForm
from ..models.attendance import Roster,Shift
from django.core.exceptions import ObjectDoesNotExist

from django.views.generic import (
    FormView,
    CreateView,
    UpdateView,
    ListView,
    DetailView,
)
class RosterCreateView(CreateView):
    template_name = 'eattendance/roster_create.html'
    form_class = RosterCreateForm
    model = Roster

    def get_initial (self):
        user = self.request.user
        try:
            user_emp = Employee.objects.get(user=user)
            apprs = LeaveApprover.objects.get_departments(user_emp)
            depts = []
            for a in apprs:
                depts.append(a.department)
                print(a)
            #print(depts)
            emps = Employee.objects.filter(department__in=depts)
            print(emps.query)
            return {'employee': emps}
        except ObjectDoesNotExist:
            return None

    def get_context_data(self,**kwargs):
        context = super(RosterCreateView,self).get_context_data(**kwargs)
        user = self.request.user
        employee = Employee.objects.get(user=user)
        context['employee']=employee
        return context

    def form_valid(self, form):
        print('Inside form_valid')
        self.object = form.save(commit=False)
        self.object.created_by=self.request.user
        #print(self.request.shift_from_)
        self.object.save()
        #print(self.get_success_url())
        return HttpResponseRedirect(self.get_success_url())