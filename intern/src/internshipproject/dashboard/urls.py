from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_view, name='dashboard_view'),
    path('applicant/<int:applicant_id>/', views.applicant_detail_view, name='applicant_detail'),
]