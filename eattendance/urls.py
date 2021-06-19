from django.urls import path
from .views.shift_views import (
    ShiftCreateView,
    ShiftDetailView,
    ShiftUpdateView,
    ShiftListView,
)
from .views.roster_view import(
    RosterCreateView,
)
app_name = 'eattendance'
urlpatterns = [
    # shift urls
    path('shift/create/', ShiftCreateView.as_view(), name='shift-create'),
    path('shift/<int:pk>/', ShiftDetailView.as_view(), name='shift-detail'),
    path('shift/<int:pk>/update', ShiftUpdateView.as_view(),name='shift-update'),
    path('shifts/', ShiftListView.as_view(), name='shifts'),
    # roster urls
    path('roster/create/', RosterCreateView.as_view(), name='roster-create'),
]