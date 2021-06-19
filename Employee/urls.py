from django.urls import path
from .views import (
    EmployeeAddView,
    EmployeeListView,
    EmployeeUpdateView,
    EmployeeDetailView,
)

app_name = 'Employee'

urlpatterns = [
    path('create',EmployeeAddView.as_view(),name='create-employee'),
    path('emplist',EmployeeListView.as_view(),name='employee-list'),
    path('<int:id>/update/', EmployeeUpdateView.as_view(), name='employee-update'),
    path('<int:id>/', EmployeeDetailView.as_view(), name='employee-detail'),
]