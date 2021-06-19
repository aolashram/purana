from datetime import datetime,date
from Employee.models import LeaveApprover,Employee
from django.db.models import Count
from django.forms import forms
from django.http import request
from django.shortcuts import render,HttpResponseRedirect,get_object_or_404
from django.views.generic.base import View
from .models import Area, Department, DietItem, DietOrder, Doctor, ItemCategory, Patient, Room, Visit,Bed
from .forms import DietOrderUpdateForm, PatientCreateForm,DietOrderForm
from django.urls import reverse,reverse_lazy
# import generic FormView
from django.views.generic import (
    FormView,
    CreateView,
    UpdateView,
    ListView,
    DetailView,
)

# Create your views here.
class VisitCreateView(CreateView):
    template_name = 'med/visitor_create.html'
    form_class = PatientCreateForm
    model = Visit
    #fields = '__all__'
    success_url = reverse_lazy('visit-details')

    def get_initial (self):
        user = self.request.user
        try:
            user_emp = Employee.objects.get(user=user)
            apprs = LeaveApprover.objects.get_departments(user_emp)
            depts = []
            for a in apprs:
                depts.append(a.department)
               # print(a)
            #print(depts)
            emps = Employee.objects.filter(department__in=depts)
           # print(emps.query)
            return {'employee': emps}
        except ObjectDoesNotExist:
            return None

    def get_context_data(self,**kwargs):
        print('get_context_data')
        context = super(VisitCreateView,self).get_context_data(**kwargs)
        user = self.request.user
        employee = Employee.objects.get(user=user)
        context['employee']=employee
        return context

    def post(self, request):
        print('inside post --')
        form = PatientCreateForm(request.POST)
        print(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.created_by = request.user
            form.save()
            return HttpResponseRedirect(self.get_success_url())
        else:
            form = PatientCreateForm()
        return render(
                    request,
                    self.template_name,
                    { 'form': form})

class VisitDetailView(DetailView):
    model = Visit

    def get_context_data(self,**kwargs):
        context = super(VisitDetailView,self).get_context_data(**kwargs)
        user = self.request.user
        employee = Employee.objects.get(user=user)
        context['employee']=employee
        return context

def load_rooms(request):
    area_id = request.GET.get('area')
    rooms = Room.objects.filter(area_id=area_id).order_by('roomno')
    #print('rooms')
    return render(request, 'med/room_dropdown_list_options.html', {'rooms': rooms})

def load_beds(request):
    room_id = request.GET.get('room')
    beds = Bed.objects.filter(room_id=room_id).order_by('bedno')
    #print('rooms')
    return render(request, 'med/bed_dropdown_list_options.html', {'beds': beds})

def livesearch_ipno(request):
    if request.method == "GET":
        search_text = request.GET['q']
        if search_text is not None and search_text != u"":
            search_text = request.GET['q']
            patients = Visit.objects.filter(ipno__contains = search_text)
        else:
            patients = ['one','two','three']

        return render(request, 'med/ajax_search_ipno.html', {'patients':patients})

class DietOrderUpdateView(View):
    template_name = 'med/diet_order.html'
    form_class = DietOrderUpdateForm
    model = DietOrder
    #fields = '__all__'
    success_url = reverse_lazy('list-diet')
    
    def get(self, request,id):
        context ={}
        print('Inside get')
        print(self.kwargs)
        #id_ = self.kwargs.get("id")
        do = get_object_or_404(DietOrder, pk=id)
        fullname = do.patient.patient.fullname
        mrno = do.patient.patient.mrno
        gender = do.patient.patient.gender
        age = do.patient.patient.age
        ipno = do.patient.ipno
        department = do.patient.department
        doctor = do.patient.doctor
        building_floor = do.patient.building_floor
        room = do.patient.room
        bedno = do.patient.bedno
        slot = do.slot
        category = do.category
        item = do.item
        special_instruction = do.special_instruction
        patient =do.patient
        quantity = do.quantity
        delivery_date = do.delivery_date
        doid = do.pk
        form = DietOrderUpdateForm(initial={
            "fullname": fullname,"mrno":mrno,"gender":gender,"age":age,"ipno":ipno,"doid":doid,
            "department":department,"doctor":doctor,"building_floor":building_floor,"delivery_date":delivery_date,
            "slot":slot,"category":category,"special_instruction":special_instruction,
            "room":room,"bedno":bedno,"quantity":quantity,"patient":patient,"item":item
            })
        context['form']= form
        return render(request, self.template_name,context)
    
    def post(self, request,id):
        print('inside post')
        dietorder = DietOrder.objects.get(pk=id)
        category = request.POST.get('category')
        ic = ItemCategory.objects.get(pk=category) 
        dietorder.category = ic
        i = request.POST.get('item')
        item = DietItem.objects.get(pk=i) 
        dietorder.item = item
        dietorder.quantity = request.POST.get('quantity')
        dietorder.special_instruction = request.POST.get('special_instruction')
        dietorder.slot = request.POST.get('slot')
        dietorder.delivery_date = request.POST.get('delivery_date')
        dietorder.updated_by = request.user
        dietorder.save()
        context = {'diet':dietorder}
        # returl = reverse('med:dietorder-detail', args=(dietorder.pk,))
        # print(returl)
        return HttpResponseRedirect(reverse('med:dietorder-detail', kwargs={'id':dietorder.pk}))
        # return render(request, returl, context)

class DietOrderView(View):
    template_name = 'med/diet_order.html'
    form_class = DietOrderForm
    model = DietOrder
    success_url = reverse_lazy('list-diet')

    def get_context_data(self,**kwargs):
        context = super(DietOrderView,self).get_context_data(**kwargs)
        user = self.request.user
        employee = Employee.objects.get(user=user)
        context['employee']=employee
        return context

    def get(self, request):
        context = {}
        form = DietOrderForm()
        user = self.request.user
        employee = Employee.objects.get(user=user)
        context['employee']=employee
        context['form']= form
        return render(request, self.template_name,context)

    def post(self, request):
        ipno = request.POST.get('ipno')
        patient = Patient()
        ipvisit = Visit()
        if ipno:
            try:
                ipvisit = Visit.objects.get(ipno)
            except Visit.DoesNotExist:
                ipvisit = None
        if not ipvisit:
            patient.fullname = request.POST.get('fullname')
            patient.mrno = request.POST.get('mrno')
            patient.gender = request.POST.get('gender')
            patient.age = request.POST.get('age')
            ipvisit.ipno = request.POST.get('ipno')
            doctor = request.POST.get('doctor')
            doc = Doctor.objects.get(pk=doctor)
            dept = doc.department
            ipvisit.doctor = doc
            ipvisit.department = dept
            areaid = request.POST.get('building_floor')
            area = Area.objects.get(pk=areaid)
            ipvisit.building_floor = area
            roomid = request.POST.get('room')
            room = Room.objects.get(pk=roomid)
            ipvisit.room = room
            bedid = request.POST.get('bedno')
            bed = Bed.objects.get(pk=bedid)
            ipvisit.bedno = bed
            patient.save()
            ipvisit.patient = patient
            ipvisit.save()
        # Save DietOrder
        dietorder = DietOrder()
        dietorder.patient = ipvisit
        category = request.POST.get('category')
        ic = ItemCategory.objects.get(pk=category) 
        dietorder.category = ic
        i = request.POST.get('item')
        item = DietItem.objects.get(pk=i) 
        dietorder.item = item
        dietorder.quantity = request.POST.get('quantity')
        dietorder.special_instruction = request.POST.get('special_instruction')
        dietorder.slot = request.POST.get('slot')
        dietorder.delivery_date = request.POST.get('delivery_date')
        dietorder.created_by = request.user
        dietorder.save()
        #context = {'diet':dietorder}
        return HttpResponseRedirect(reverse('med:dietorder-detail', kwargs={'id':dietorder.pk}))

class DietOrderDetailView(DetailView):
    model = DietOrder
    template_name = 'med/dietorder_detail.html'

    def get_context_data(self,**kwargs):
        context = super(DietOrderDetailView,self).get_context_data(**kwargs)
        user = self.request.user
        employee = Employee.objects.get(user=user)
        context['employee']=employee
        return context

    def get_object(self):
        id_ = self.kwargs.get("id")
        print('Inside Detailview-get_object')
        print(id_)
        return get_object_or_404(DietOrder, id=id_)

class DietOrderList(ListView):
    model = DietOrder
    template_name = 'med/dietorder_list.html'
    context_object_name = 'dietorders'  # Default: object_list
    paginate_by = 5
    #queryset = DietOrder.objects.get_queryset().order_by('delivery_date')  # Default: Model.objects.all()

    def get_queryset(self):
        query = self.request.GET.get('q')
        reqdate = None
        if query:
            reqdate = datetime.strptime(query, "%d/%m/%Y")
            object_list = self.model.objects.filter(delivery_date=reqdate).order_by('delivery_date')
        else:
            today = date.today()
            object_list = self.model.objects.filter(delivery_date=today).order_by('delivery_date')
        return object_list

    def get_context_data(self,**kwargs):
        context = super(DietOrderList,self).get_context_data(**kwargs)
        user = self.request.user
        employee = Employee.objects.get(user=user)
        context['employee']=employee
        query = self.request.GET.get('q')
        if query:
            reqdate = datetime.strptime(query, "%d/%m/%Y")
            totals = self.model.objects.values('item__item_name').annotate(total=Count('item')).\
                filter(delivery_date=reqdate).order_by('total')
        else:
            today = date.today()
            totals = self.model.objects.values('item').annotate(total=Count('item')).\
                filter(delivery_date=today).order_by('total')
        context['totals']=totals
        print(totals)
        return context