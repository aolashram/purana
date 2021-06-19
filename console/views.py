from django.shortcuts import render
from accounts.models import Role
from Employee.models import Employee, LeaveApprover
from leave.models import LeaveRequest, LeaveType, LeavesAllottedTotal,ApprovedLeaves
from django.db.models import Q
from django.db.models.query import QuerySet
from datetime import date
from django.contrib.auth.decorators import login_required
from eattendance.models.backengine import Devicelogs42021,Devicelogs

@login_required(login_url='/login/')
def dashboard_view(request):
    a = set_leaveallottedtotal(request)
    emp_list = get_today_leaves(request)
    pending_list = get_pending_leaves(request)
    taken_leaves = get_taken_leaves(request)
    leave_totals = get_total_leaves(request)
    dvlog = Devicelogs42021.objects.using('second').filter(deviceid__gte=1)
    print("dvlog==")
    print(dvlog)
    user = request.user
    userroles = user.roles.all()
    r = (r.pk for r in userroles)
    roles = list(r)
    #print(list(roles))
    hod = hrexcec = hrhead = cao = emp = admofficer = False
    if Role.HOD in roles:
        hod = True
    if Role.HREXEC in roles:
        hrexcec = True
    if Role.HRHEAD in roles:
        hrhead = True
    if Role.ADMIN_OFFICER in roles:
        admofficer = True
    if Role.CAO in roles:
        cao = True    
    if Role.EMPLOYEE in roles:
        emp = True  
    #print(Role.EMPLOYEE in roles)
    roledict = {'hod':hod,'hrexcec':hrexcec,'hrhead':hrhead,'admofficer':admofficer,'cao':cao,'employee':emp}   
    #print(roledict)  
    employee = Employee.objects.get(user=user)
    #print(employee)
    context = {'today_leave_emp': emp_list, 'pending_leave_list': pending_list,'leave_totals':leave_totals,
                    'employee':employee,'taken_leaves':taken_leaves,'roles':roledict,}
    return render(request, 'console/dashboard.html', context=context)


def get_total_leaves(request):
    leavetypeset = {}
    if request:
        user = request.user
        employee = Employee.objects.get(user=user)
        yr = date.today().strftime('%Y')
        leavetypes = LeaveType.objects.filter(can_apply=LeaveType.YES)
        for lt in leavetypes:
            la = LeavesAllottedTotal.objects.total(employee,lt)
            if la:
                leavetypeset[lt.code]= la.total_leaves

    return leavetypeset

def get_taken_leaves(request):
    if request:
        user = request.user
        employee = Employee.objects.get(user=user)
        leavetypes = LeaveType.objects.filter(can_apply=LeaveType.YES)
        leavetypeset = {}
        if leavetypes.exists():
            for lt in leavetypes:
                ap = ApprovedLeaves.objects.getTotalSpecificLeave(lt,employee)
                leavetypeset[lt.code]= ap
        return leavetypeset

def get_pending_leaves(request):
    ONE = 1
    TWO = 2
    THREE = 3
    dept = ''
    if request:
        user = request.user
        employee = Employee.objects.get(user=user)
        try:
            approvers = LeaveApprover.objects.filter(approver=employee)
            reqs = set()
            for apr in approvers:
                level = apr.position
                val = LeaveRequest.objects.get_by_department(apr.department).filter(leave_state=LeaveRequest.PENDING)

                if ONE == level:
                    val = LeaveRequest.objects.filter(leave_state='Pending', first_approver_status='Pending')
                elif TWO == level:
                    val = LeaveRequest.objects.filter(leave_state='Pending', second_approver_status='Pending')
                elif THREE == level:
                    val = LeaveRequest.objects.filter(leave_state='Pending', third_approver_status='Pending')
                if val.exists():
                    for v in val:
                        reqs.add(v)
            return reqs
        except LeaveApprover.DoesNotExist:
            return None
    return None       


def get_today_leaves(request):
    user = request.user
    employee = None
    try:
        employee = Employee.objects.get(user=user)
    except Employee.DoesNotExist:
        return None
    approver = LeaveApprover.objects.filter(approver=employee)
    departments = set()
    req = set()
    if approver.exists:
        for ap in approver:
            val = LeaveRequest.objects.get_by_department(ap.department).filter(leave_state='Approved')
            for v in val:
                if v.is_leave_today:
                    req.add(v)
    print("Inside get_today_leaves")
    #print(req)
    return req

def get_user_departments(request):
    login_user = request.user
    logined_employee = Employee.objects.filter(user=login_user).first()
    f_appr = LeaveApprover.objects.filter(approver=logined_employee)
    dep_set = set()
    for appr in f_appr:
        dep_set.add(appr.department)
    return dep_set


def set_leaveallottedtotal(request):
    return
    leavetypes = LeaveType.objects.all()
    employee = Employee.objects.all()
    print(leavetypes)
    for e in employee:
        for l in leavetypes:
            mx = str(l.maximum_leaves)
            a = LeavesAllottedTotal(year='2021',leave_type=l,employee=e,total_leaves=mx)
            print(a)
            a.save()