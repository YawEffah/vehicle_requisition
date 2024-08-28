from django.urls import path

from . import views


app_name = 'requisition'
urlpatterns = [
    path('', views.index, name='index'),
    path('staff_dashboard/', views.staff_dashboard, name='staff_dashboard'),
    path('requests_dashboard/', views.transport_officer_dashboard, name='requests_dashboard'),
    path('fleet_dashboard/', views.fleet_dashboard, name='fleet_dashboard'),
    path('change_status/<int:request_id>/', views.change_status, name='change_status'),
    path('request/edit/<int:request_id>', views.edit_request_view, name='edit_request'),
    path('request/delete/<int:request_id>', views.delete_request_view, name='delete_request'),
    path('fleet/delete/<int:pk>/', views.delete_vehicle, name='delete_vehicle'),
    path('fleet/edit/<int:pk>/', views.edit_vehicle, name='edit_vehicle'),
]
