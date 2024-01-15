from django.contrib.auth import views as authentication_views
from django.contrib import admin
from django.urls import path
from .import views

urlpatterns = [
    path('', views.index, name='home'),
    path('contact_us/', views.contact, name='contact'),
    path('about_us/', views.about, name='about'),

    path('ongoing/', views.ongoing, name='ongoing'),
    path('requests/',views.requests,name='requests'),
    path('history/',views.history,name='history'),

    path('analytics/',views.analytics,name='analytics'),
    path('generate_pdf/',views.generate_pdf, name='generate_pdf'),

    path('request/<str:id>/', views.details_reported, name='details_reported'),
    path('ongoing/<str:id>/', views.details_ongoing, name='details_ongoing'),

    path('update_status_ongoing/<str:id>/', views.status_ongoing, name='status_ongoing'),
    path('update_status_ended/<str:id>/', views.status_ended, name='status_ended'),
    path('delete/<str:id>/', views.delete_report, name='delete_report'),
    path('delete_history/<str:id>/', views.delete_history, name='delete_history'),

    path('add_incident/', views.save_to_firebase, name='save_to_firebase'),
    path('update_ongoing_incidentdata/<str:id>/', views.update_ongoing_incident, name='update_ongoing_incident'),
    path('update_reported_incidentdata/<str:id>/', views.update_reported_incident, name='update_reported_incident'),

    path('sign_in/',authentication_views.LoginView.as_view(template_name='reports/sign_in.html'), name='sign_in'),
    path('logout/',authentication_views.LogoutView.as_view(template_name='reports/sign_out.html'), name='logout'),
]