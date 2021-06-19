import datetime
from django.shortcuts import render,HttpResponseRedirect,get_object_or_404
from ..forms import ShiftCreateForm
from ..models import Shift
from Employee.models import Employee

from django.views.generic import (
    FormView,
    CreateView,
    UpdateView,
    ListView,
    DetailView,
)

class ShiftListView(ListView):
    model = Shift
    def get_context_data(self,**kwargs):
        context = super(ShiftListView,self).get_context_data(**kwargs)
        user = self.request.user
        employee = Employee.objects.get(user=user)
        context['employee']=employee
        return context

class ShiftCreateView(CreateView):
    template_name = 'eattendance/shift_create.html'
    form_class = ShiftCreateForm
    model = Shift

    def get_context_data(self,**kwargs):
        context = super(ShiftCreateForm,self).get_context_data(**kwargs)
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

class ShiftUpdateView(UpdateView):
    model = Shift
    form_class = ShiftCreateForm
    template_name = 'eattendance/shift_create.html'

    def get_object(self, *args, **kwargs):
        shift = get_object_or_404(Shift, pk=self.kwargs['pk'])
        return shift

    def get_context_data(self,**kwargs):
        context = super(ShiftUpdateView,self).get_context_data(**kwargs)
        user = self.request.user
        employee = Employee.objects.get(user=user)
        context['employee']=employee
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.updated_by=self.request.user
        self.object.updated_date = datetime.date.today()
        #print(self.request.shift_from_)
        self.object.save()
        #print(self.get_success_url())
        return HttpResponseRedirect(self.get_success_url())

    # def get_success_url(self, *args, **kwargs):
    #     return reverse("some url name")

class ShiftDetailView(DetailView):
    model = Shift

    def get_context_data(self,**kwargs):
        context = super(ShiftDetailView,self).get_context_data(**kwargs)
        user = self.request.user
        employee = Employee.objects.get(user=user)
        context['employee']=employee
        return context