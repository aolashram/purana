from django.shortcuts import render, get_object_or_404
from .forms import EmployeeModelForm
from .models import Employee, LeaveApprover
# import generic FormView
from django.views.generic import (
    FormView,
    CreateView,
    UpdateView,
    ListView,
    DetailView,
)
# Create your views here.

  
  
class EmployeeAddView(CreateView):
    # specify the Form you want to use
    form_class = EmployeeModelForm
    # sepcify name of template
    template_name = "Employee/employee_add_form.html"
  
    # can specify success url
    # url to redirect after successfully
    # updating details
    success_url ="/thanks/"

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        form.instance.user = self.request.user
        # perform a action here
        print(form.cleaned_data)
        return super().form_valid(form)


class EmployeeUpdateView(UpdateView):
    template_name = "Employee/employee_add_form.html"
    form_class = EmployeeModelForm

    def get_object(self):
        id_ = self.kwargs.get("id")
        return get_object_or_404(Employee, id=id_)

    def form_valid(self, form):
        print(form.cleaned_data)
        return super().form_valid(form)

class EmployeeListView(ListView):
    def get_context_data(self,**kwargs):
        context = super(EmployeeListView,self).get_context_data(**kwargs)
        user = self.request.user
        employee = Employee.objects.get(user=user)
        context['employee']=employee
        return context

    def get_queryset(self):
        dept = ''
        if self.request.user:
            curuser =self.request.user
            print(curuser)
            emp = Employee.objects.filter(user=curuser).first()

            #get leave approver dept
            approvers = LeaveApprover.objects.filter(approver=emp)
            dep_set = set()
            for approver in approvers:
                dep_set.add(approver.department)
            print(dep_set)
            #dept = emp.department
        return Employee.objects.filter(department__in=dep_set)
    
    template_name = 'Employee/employee_list.html'
    context_object_name = 'employees'
    paginate_by = 10
    ordering = ['-created']

class EmployeeDetailView(DetailView):
    template_name = 'Employee/employee_detail.html'
    #queryset = Article.objects.all()

    def get_object(self):
        id_ = self.kwargs.get("id")
        return get_object_or_404(Employee, id=id_)