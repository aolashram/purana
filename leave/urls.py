from django.urls import path
from . import views
from .views import (
    LeaveRequestCreateView,
    LeaveDetailView,
    LeaveRequestListView,
    MonthwiseView,
)

app_name = 'leave'

urlpatterns = [
    path('<int:id>/create',LeaveRequestCreateView.as_view(),name='create-leave'),
    path('leaverequests',LeaveRequestListView.as_view(),name='leave-request-list'),
    #path('<int:id>/update/', EmployeeUpdateView.as_view(), name='employee-update'),
    path('<int:id>/', LeaveDetailView.as_view(), name='leave-detail'),
    path('<int:id>/approval',views.approve_leave_request,name='leave-approve'),
    path('<int:id>/reject',views.reject_leave,name='leave-reject'),
    path('leavemonthly',MonthwiseView.as_view(), name='leave-monthly'),
]