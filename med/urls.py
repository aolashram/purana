from django.urls import path
from . import views

app_name = 'med'

urlpatterns = [
    path('visit/create',views.VisitCreateView.as_view(),name='create-visit'),
    path('visit/<int:id>/', views.VisitDetailView.as_view(), name='visit-detail'),

    path('diet/create',views.DietOrderView.as_view(),name='create-diet'),
    path('<int:id>/edit',views.DietOrderUpdateView.as_view(),name='leave-update'),
    path('diet/<int:id>/',views.DietOrderDetailView.as_view(),name='dietorder-detail'),
    path('diet/list/', views.DietOrderList.as_view(), name='list-diet'),

    path('ajax/load_rooms', views.load_rooms, name='ajax_load_rooms'), 
    path('ajax/load_beds', views.load_beds, name='ajax_load_beds'), 
    path('ajax/load_livesearch_ipno', views.livesearch_ipno, name='ajax_livesearch'), 
]