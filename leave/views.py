import datetime
from django.shortcuts import render, get_object_or_404, HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .forms import LeaveRequestForm
from .models import LeaveRequest, LeaveType, LeavesAllottedTotal, ApprovedLeaves
from Employee.models import Employee,LeaveApprover
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.views import View
from calendar import monthrange

# import generic FormView
from django.views.generic import (
    FormView,
    CreateView,
    UpdateView,
    ListView,
    DetailView,
)

class LeaveRequestCreateView(CreateView):
    ONE = 1
    TWO =2
    THREE =3
    FIVE = 5
    # specify the Form you want to use
    form_class = LeaveRequestForm
    # sepcify name of template
    template_name = "leave/leave_create.html"
    def get_success_url(self):
        return reverse('leave:leave-detail',args=(self.object.id,))

    def get_context_data(self,**kwargs):
        context = super(LeaveRequestCreateView,self).get_context_data(**kwargs)
        user = self.request.user
        employee = Employee.objects.get(user=user)
        context['employee']=employee
        return context

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        login_user = self.request.user
        employee = self.get_employee()
        form.instance.employee = employee
        form.instance.created_by = login_user
        emp_dept = employee.department
        approvers = LeaveApprover.objects.filter(department=emp_dept)
        loginuser_approve_pos = 0
        approver1 = None
        approver2 =None
        approver3 = None 
        #GOT ALL APPROVERS, NEED TO USE THIS VALUE
        approvers_dict = {}
        for a in approvers:
            approvers_dict[a.position]=a
            if a.position==self.ONE:
                approver1=a.approver
            if a.position==self.TWO:
                approver2=a.approver
            if a.position==self.THREE:
                approver3=a.approver
            if login_user==a.approver.user:
                loginuser_approve_pos = a.position # Login user is a leave approver and position of approval is a.position

        #print(a)
        leaves_exists_in = self.leave_entry_exists(form)
        if leaves_exists_in:
            form.add_error(None,"Leaves applied are overlapping with previously applied leave entries. Kindly check !")
            return super().form_invalid(form)

        leave_days_td = form.instance.leavetill-form.instance.leavefrom
        leave_days = leave_days_td.days+1
        print(leave_days)
        #return
        if leave_days == self.ONE: # Only 1 line manager approval is neede for 1 day leave
            form.instance.second_approver_status = LeaveRequest.NA 
            form.instance.third_approver_status = LeaveRequest.NA 
        elif leave_days < self.FIVE: # Only 2 line manager approval is neede for 1 day leave
            form.instance.third_approver_status = LeaveRequest.NA #
        #Leave request created by ownself and is a first level approver
        if employee.user == login_user:
            if employee == approver1:
                form.instance.first_approver_status = LeaveRequest.NA
                form.instance.second_approver_status = LeaveRequest.PENDING
                form.instance.first_approver_remark = form.instance.comments
            elif employee == approver2:
                form.instance.first_approver_status = LeaveRequest.NA
                form.instance.second_approver_status = LeaveRequest.NA
                form.instance.third_approver_status = LeaveRequest.PENDING
                form.instance.second_approver_remark = form.instance.comments 
            elif employee == approver3:
                form.instance.first_approver_status = LeaveRequest.NA
                form.instance.second_approver_status = LeaveRequest.NA
                form.instance.third_approver_status = LeaveRequest.APPROVED
                form.instance.third_approver_remark = form.instance.comments 
                form.instance.leave_state=LeaveRequest.APPROVED
            else:
                if leave_days==self.ONE:
                    form.instance.first_approver_status = LeaveRequest.PENDING
                    form.instance.first_approver_remark = form.instance.comments
                elif leave_days < self.FIVE:
                    form.instance.first_approver_status = LeaveRequest.PENDING
                    form.instance.second_approver_status = LeaveRequest.PENDING
                else:
                    form.instance.first_approver_status = LeaveRequest.PENDING
                    form.instance.second_approver_status = LeaveRequest.PENDING
                    form.instance.third_approver_status = LeaveRequest.PENDING
        #If Line manager is applying leave for his/her staff
        elif login_user==approver1.user:
            form.instance.first_approver_status = LeaveRequest.APPROVED
            form.instance.first_approver_remark = form.instance.comments
            if leave_days == self.ONE:
                form.instance.leave_state=LeaveRequest.APPROVED
        elif login_user==approver2.user:
            form.instance.first_approver_status = LeaveRequest.NA
            form.instance.second_approver_status = LeaveRequest.APPROVED
            form.instance.second_approver_remark = form.instance.comments 
            if leave_days < self.FIVE:
                form.instance.leave_state=LeaveRequest.APPROVED   
        elif login_user==approver3.user:
            form.instance.second_approver_status = LeaveRequest.NA
            form.instance.third_approver_status = LeaveRequest.APPROVED
            form.instance.third_approver_remark = form.instance.comments  
            form.instance.leave_state =  LeaveRequest.APPROVED
        else:
            form.add_error(None,"You are not an authorised person to apply leave. Please contact your Line Manager !")
            return super().form_invalid(form)
        # perform a action here
        print(form.cleaned_data)
        is_leave_approved = False
        if form.instance.leave_state == LeaveRequest.APPROVED:
            is_leave_approved = True
        self.object = form.save(commit=False)
        #Save all
        is_sick = form.cleaned_data['is_sick']
        form = self.object.save()
        #ret = distribute_leaves(form, leave_days, is_sick)

        cl_leaves_consumed = None
        el_leaves_consumed = None
        if is_sick == 'YES':
            make_sickleave()
        else:
            if is_leave_approved:
                self.manage_leaves(employee,leave_days,self.object)
                cl_type = LeaveType.objects.getLeaveTypeOnCode('CL')
                el_type = LeaveType.objects.getLeaveTypeOnCode('EL')
                cl_leaves_consumed = ApprovedLeaves.objects.getTotalSpecificLeave(cl_type,employee)
                el_leaves_consumed = ApprovedLeaves.objects.getTotalSpecificLeave(el_type,employee)
            
        #return HttpResponseRedirect(self.get_success_url())

        context = {'id':self.object.pk ,'CL': cl_leaves_consumed, 'EL': el_leaves_consumed,}
        print(context)
        return HttpResponseRedirect(reverse('leave:leave-detail',
                                        args=(self.object.pk,)))
        #return render(self.request, 'leave/leave_detail.html', context=context)

    def manage_leaves(self,employee,leave_demanded,form):
        leave_left = leave_demanded
        today = datetime.date.today()
        this_month = today.month
        cl_apply = 0
        el_apply =0
        lop_apply = 0
        cl_type = LeaveType.objects.getLeaveTypeOnCode('CL')
        el_type = LeaveType.objects.getLeaveTypeOnCode('EL')
        lop_type = LeaveType.objects.getLeaveTypeOnCode('LOP')
        #
        cl_yearly_allotted = LeavesAllottedTotal.objects.total(employee,cl_type)#.filter(leave_type=cl_type).first()
        cl_leaves_consumed = ApprovedLeaves.objects.getTotalSpecificLeave(cl_type,employee)
        el_yearly_allotted = LeavesAllottedTotal.objects.total(employee,el_type)
        el_leaves_consumed = ApprovedLeaves.objects.getTotalSpecificLeave(el_type,employee)
        #
        cl_inhand = cl_yearly_allotted.total_leaves - cl_leaves_consumed
        el_inhand = el_yearly_allotted.total_leaves - el_leaves_consumed
        #
        cl_can = this_month-cl_leaves_consumed

        if cl_can > 0:
            if cl_can <= leave_left:
                cl_apply = cl_can
                leave_left = leave_left - cl_can
            else:
                cl_apply = leave_left
                leave_left = 0

        if el_inhand > 0: # EL leaves are available
            if el_inhand >= leave_left:
                el_apply = leave_left
                leave_left = 0
            else:
                el_apply = el_inhand
                leave_left = leave_left - el_inhand
                if cl_inhand <= leave_left:
                    cl_apply = cl_apply + cl_inhand
                    leave_left = leave_left - cl_inhand
                else:
                    cl_apply = cl_apply + leave_left
                    leave_left = 0

        if leave_left > 0:
            lop_apply = leave_left 
            
        
        print('CL:' + str(cl_apply))
        print('EL:' + str(el_apply))
        print('LOP:' + str(leave_left))
        if cl_apply > 0:
            ApprovedLeaves.objects.create_me(employee,cl_type,cl_apply,form)
        if el_apply > 0:
            ApprovedLeaves.objects.create_me(employee,el_type,el_apply,form)
        if lop_apply > 0:
            ApprovedLeaves.objects.create_me(employee,lop_type,lop_apply,form)
        return

    def make_sickleave():
        pass

    def get_employee(self):
        id_ = self.kwargs.get("id")
        return get_object_or_404(Employee, id=id_)
    
    def leave_entry_exists(self, form):
        login_user = self.request.user
        employee = self.get_employee()
        leavefrom = form.instance.leavefrom
        leavetill = form.instance.leavetill
        if leavefrom and leavetill and employee:
            query = Q(employee=employee)
            query.add(Q(leavetill__gte=leavefrom), Q.AND)
            query.add(Q(leavefrom__lte=leavetill), Q.AND)
            lreq = LeaveRequest.objects.filter(query)
           # print('leavefrom:'+leavefrom+': leavetill:'+leavetill+' : empid:'+employee)
            print(lreq.exists())
            data =False
            if lreq.exists():
                return True
                #entries exists
        return False


class LeaveDetailView(DetailView):
    template_name = 'leave/leave_detail.html'
    #queryset = Article.objects.all()
    def get_context_data(self, **kwargs):
        context = super(LeaveDetailView, self).get_context_data(**kwargs)
        print('Inside Detailview-get_context_data')
        this_obj = context['object']
        leavetypeset = {}
        if this_obj:
            employee = this_obj.employee
            if employee:
                leavetypes = LeaveType.objects.filter(can_apply=LeaveType.YES)
                leavetypeset = {}
                if leavetypes.exists():
                    for lt in leavetypes:
                        ap = ApprovedLeaves.objects.getTotalSpecificLeave(lt,employee)
                        leavetypeset[lt.code]= ap
        context['leavebalance'] = leavetypeset
        print(context)
        return context

    def get_object(self):
        id_ = self.kwargs.get("id")
        print('Inside Detailview-get_object')
        #print(id_)
        return get_object_or_404(LeaveRequest, id=id_)


class LeaveRequestListView(ListView):
    ONE = 1
    TWO = 2
    THREE = 3
    models = LeaveRequest
    queryset = LeaveRequest.objects.none()

    def get_request_set(self):
        dept = ''
        if self.request:
            user = self.request.user
            employee = Employee.objects.get(user=user)
            print('inside get_request_set')
            try:
                approvers = LeaveApprover.objects.filter(approver=employee)
                reqs = set()
                for apr in approvers:
                    level = apr.position
                    val = LeaveRequest.objects.get_by_department(apr.department).filter(leave_state=LeaveRequest.PENDING)
                    if val.exists():
                        for v in val:
                            reqs.add(v)
                sorted_list = sorted(reqs,key=lambda x: x.leavefrom)
                return sorted_list
            except LeaveApprover.DoesNotExist:
                return None
    
    def get_context_data(self,**kwargs):
        context = super(LeaveRequestListView,self).get_context_data(**kwargs)
        user = self.request.user
        employee = Employee.objects.get(user=user)
        context['employee']=employee
        context['requests']=self.get_request_set()
        return context

    template_name = 'leave/leave_request_list.html'
    paginate_by = 10
    ordering = ['-leavefrom']

class MonthwiseView(View):
    #form_class = MyForm
    initial = {'key': 'value'}
    template_name = 'leave/leave_monthly.html'

    def get(self, request, *args, **kwargs):
        mnt = int(datetime.date.today().strftime('%m'))
        monthname = datetime.date.today().strftime('%B')
        yr = int(datetime.date.today().strftime('%Y'))
        num_days = monthrange(yr, mnt)[1]

        departments = get_user_dept_staff(request)
        
        emps = Employee.objects.filter(department__in=departments)
        # query.add(Q(leavetill__gte=leavefrom), Q.AND)
        #     query.add(Q(leavefrom__lte=leavetill), Q.AND)
        m_firstday = datetime.date.today().replace(day=1)
        m_lastday = datetime.date.today().replace(day=num_days)
        leavereqests = LeaveRequest.objects.filter(
            employee__in=emps,leavetill__gte=m_firstday,leavefrom__lte=m_lastday
        )
        #print(range(1,int(num_days)))
        table = draw_table(range(1,int(num_days)+1),emps,leavereqests,mnt,num_days)

        context= { 'days':range(1,int(num_days)+1), 'monthname':monthname, 'table':table}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        context= { 'days':range(1,32) }
        # if form.is_valid():
        #     # <process form cleaned data>
        #     return HttpResponseRedirect('/success/')

        return render(request, self.template_name, context)

def draw_table(days,employees,leavereqests,mnt,num_days):
    table = '<table border="1" width="100%" style="border-color: rgb(199, 190, 199);">'
    table += '<thead style="background-color:rgb(236, 236, 235)">'
    table += '<tr align="center">'
    table += '<th class="p-2">Name</th>'
    for d in days:
        table += '<th>' + str(d) + '</th>'
    table += '</tr>' 
    table += '</thead>'
    table += '<tbody>'
    for emp in employees:
        lr = leavereqests.filter(employee=emp)
        start = {}
        end = {}
        if lr.exists():
            for lvr in lr:
                st = int(lvr.leavefrom.strftime('%d'))
                start[st]= st
                if int(lvr.leavefrom.strftime('%m')) < mnt:
                    start[1] = 1
                    st = 1
                ed = int(lvr.leavetill.strftime('%d'))
                end[st] = ed 
                if int(lvr.leavetill.strftime('%m')) > mnt:
                    end[st] = num_days
            #print(start)
            # lfrom =  lr[0].leavefrom
            # ltill = lr[0].leavetill
            # start = int(lfrom.strftime('%d'))
            # end = int(ltill.strftime('%d'))
            # if int(lfrom.strftime('%m')) < mnt:
            #     start = 1
            # if int(ltill.strftime('%m')) > mnt:
            #     end = num_days
        table += "<tr>"   
        table += '<td class="p-2">' + str(emp.id) + '--' + emp.get_full_name + '</td>'
        itr = False
        end_date = -1
        loop = 0
        for d in days:
            if start.get(d) and end.get(d):
                if d >= start.get(d) and d <= end.get(d):
                    itr = True
                    if end_date == -1:
                        end_date = end.get(d)     
                        print(end_date)               
            if end_date >= d and end_date != -1:
                table += '<td width=3% class="table-danger"><i style="color: red;" class="ti-close icon-green "></i></td>'
                if end_date == d:
                    end_date = -1
            else:
                table += '<td width=3% class="table-success"><i style="color: black;" class="ti-check icon-black "></i></td>'
                end_date = -1
            print(end_date)        
        table += '</tr>'   
    table += '</tbody>'
    table += '</table>'

    return table

def get_user_dept_staff(request):
    user = request.user
    employee = Employee.objects.get(user=user)
    approvers = LeaveApprover.objects.get_departments(employee)
    list = []
    for a in approvers:
        list.append(a.department.id)
    return list

@login_required(login_url='/login/')
def leave_monthly(request,**args):
    context= { 'days':range(1,32) }
    return render(request, 'leave/leave_monthly.html',context=context)

@login_required(login_url='/login/')
def reject_leave(request,**args):
    ONE = 1
    TWO = 2
    THREE = 3
    FIVE = 5

    user = request.user
    user_emp = Employee.objects.get(user=user)
    ret_obj = None
    print(user_emp.id)
    id = args.get("id")
    lr = LeaveRequest.objects.get(id=id)
    employee = lr.employee
    department = employee.department
    approver = LeaveApprover.objects.get(department=department,approver=user_emp)
    if approver.approver==user_emp:
        if approver.position == ONE:
            lr.first_approver_status = LeaveRequest.REJECTED
            if lr.get_leave_duration == ONE:
                lr.second_approver_status = LeaveRequest.NA 
                lr.third_approver_status = LeaveRequest.NA 
            lr.leave_state = lr.REJECTED
            ret_obj = lr.save()
        elif approver.position == TWO:
            lr.second_approver_status = LeaveRequest.REJECTED
            if lr.get_leave_duration < FIVE and lr.get_leave_duration > ONE:
                lr.third_approver_status = LeaveRequest.NA 
                if lr.APPROVED != lr.first_approver_status:
                    lr.first_approver_status = lr.NA
            lr.leave_state = lr.REJECTED
            ret_obj = lr.save()  
        elif approver.position == THREE:
            lr.third_approver_status = LeaveRequest.REJECTED
            lr.leave_state = lr.REJECTED
            if lr.APPROVED != lr.first_approver_status:
                    lr.first_approver_status = lr.NA
            if lr.APPROVED != lr.second_approver_status:
                    lr.first_approver_status = lr.NA
            ret_obj = lr.save()
    return HttpResponseRedirect('/leave/leaverequests')  

@login_required(login_url='/login/')
def approve_leave_request(request,**args):
    ONE = 1
    TWO = 2
    THREE = 3
    FIVE = 5
    user = request.user
    user_emp = Employee.objects.get(user=user)
    ret_obj = None
    print(user_emp.id)
    id = args.get("id")
    lr = LeaveRequest.objects.get(id=id)
    employee = lr.employee
    department = employee.department
    approver = LeaveApprover.objects.get(department=department,approver=user_emp)
    if approver.approver==user_emp:
        if approver.position == ONE:
            lr.first_approver_status = LeaveRequest.APPROVED
            if lr.get_leave_duration == ONE:
                lr.second_approver_status = LeaveRequest.NA 
                lr.third_approver_status = LeaveRequest.NA 
                lr.leave_state = lr.APPROVED
                distribute(employee,lr.get_leave_duration,lr)
            ret_obj = lr.save()
        elif approver.position == TWO:
            lr.second_approver_status = LeaveRequest.APPROVED
            if lr.get_leave_duration < FIVE and lr.get_leave_duration > ONE:
                lr.third_approver_status = LeaveRequest.NA 
                lr.leave_state = lr.APPROVED
                distribute(employee,lr.get_leave_duration,lr)
                if lr.APPROVED != lr.first_approver_status:
                    lr.first_approver_status = lr.NA
            ret_obj = lr.save()
        elif approver.position == THREE:
            lr.third_approver_status = LeaveRequest.APPROVED
            lr.leave_state = lr.APPROVED
            distribute(employee,lr.get_leave_duration,lr)
            if lr.APPROVED != lr.first_approver_status:
                    lr.first_approver_status = lr.NA
            if lr.APPROVED != lr.second_approver_status:
                    lr.first_approver_status = lr.NA
            ret_obj = lr.save()
    return HttpResponseRedirect('/leave/leaverequests')
    #pass   

def distribute(employee,leave_demanded,form):
        print ('inside distribute')
        leave_left = leave_demanded
        today = datetime.date.today()
        this_month = today.month
        cl_apply = 0
        el_apply =0
        lop_apply = 0
        cl_type = LeaveType.objects.getLeaveTypeOnCode('CL')
        el_type = LeaveType.objects.getLeaveTypeOnCode('EL')
        lop_type = LeaveType.objects.getLeaveTypeOnCode('LOP')
        #
        cl_yearly_allotted = LeavesAllottedTotal.objects.total(employee,cl_type)#.filter(leave_type=cl_type).first()
        cl_leaves_consumed = ApprovedLeaves.objects.getTotalSpecificLeave(cl_type,employee)
        el_yearly_allotted = LeavesAllottedTotal.objects.total(employee,el_type)
        el_leaves_consumed = ApprovedLeaves.objects.getTotalSpecificLeave(el_type,employee)
        #
        cl_inhand = cl_yearly_allotted.total_leaves - cl_leaves_consumed
        el_inhand = el_yearly_allotted.total_leaves - el_leaves_consumed
        #
        cl_can = this_month-cl_leaves_consumed

        if cl_can > 0:
            if cl_can <= leave_left:
                cl_apply = cl_can
                leave_left = leave_left - cl_can
            else:
                cl_apply = leave_left
                leave_left = 0

        if el_inhand > 0: # EL leaves are available
            if el_inhand >= leave_left:
                el_apply = leave_left
                leave_left = 0
            else:
                el_apply = el_inhand
                leave_left = leave_left - el_inhand
                if cl_inhand <= leave_left:
                    cl_apply = cl_apply + cl_inhand
                    leave_left = leave_left - cl_inhand
                else:
                    cl_apply = cl_apply + leave_left
                    leave_left = 0

        if leave_left > 0:
            lop_apply = leave_left 
            
        
        print('CL:' + str(cl_apply))
        print('EL:' + str(el_apply))
        print('LOP:' + str(leave_left))
        #return
        if cl_apply > 0:
            ApprovedLeaves.objects.create_me(employee,cl_type,cl_apply,form)
            print('updated')
        if el_apply > 0:
            ApprovedLeaves.objects.create_me(employee,el_type,el_apply,form)
        if lop_apply > 0:
            ApprovedLeaves.objects.create_me(employee,lop_type,lop_apply,form)
        return

