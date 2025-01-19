"""
URL configuration for Djangocar project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
from . import views
from django.contrib.auth import views as auth_views  # 引入 auth_views
from django.urls import path
from .views import VehicleListView


urlpatterns = [
    path("charge_vehicle/", views.charge, name='charge'),
    path("", views.home, name='index'),
    path("index.html", views.home, name='home'),
    path("about.html", views.about, name='about'),
    path("bill.html", views.bill, name='bill'),
    path("contact_us.html", views.contact_us, name='contact_us'),
    path('login.html', views.login_view, name='login'),
    path("messages.html", views.user_messages, name='messages'),
    path("register.html", views.register_view, name='register'),
    path("vehicle.html", views.vehicle, name='vehicle'),
    path("map.html",views.map,name='map'),
    path("account.html",views.account,name='account'),
    path('logout/', views.logout_view, name='logout'),
    path('reset-password/', auth_views.PasswordResetView.as_view(template_name="reset_password.html"),
         name='reset_password'),
    path('reset-password-sent/', auth_views.PasswordResetDoneView.as_view(template_name="reset_password_sent.html"),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name="reset_password_confirm.html"),
         name='password_reset_confirm'),
    path('reset-password-complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name="reset_password_complete.html"),
         name='password_reset_complete'),
    path('moving.html', views.moving, name='moving'),
    path('return1.html', views.return1, name='return1'),
    path('pay/<int:rental_id>/', views.pay, name='pay'),
    path('start_rental/<int:vehicle_id>/', views.start_rental, name='start_rental'),  # 开始租赁
    path('end_rental/<int:rental_id>/', views.end_rental, name='end_rental'),

    path('process_payment/<int:payment_id>/', views.process_payment, name='process_payment'),

    path('rental/complete/<int:rental_id>/', views.complete_rental_view, name='complete_rental'),
    path('payment/<int:payment_id>/', views.payment_page, name='payment_page'),
    path('payment/process/<int:payment_id>/', views.process_payment, name='process_payment'),

    path('rental_detail/<int:rental_id>/', views.rental_detail_page, name='rental_detail'),
    path('manager/', views.manager_home_view, name='manager_home'),
    path('operator_login/', views.operator_login_view, name='operator_login'),
    path('operator/', views.operator_home_view, name='operator_home'),
    path('manager_login/', views.manager_login_view, name='manager_login'),
    path('api/vehicles/', VehicleListView.as_view(), name='vehicle-list'),
    path('moving/<int:rental_id>/', views.moving_view, name='moving'),


    path('api/charge_vehicle/<int:vehicle_id>/', views.charge_vehicle, name='charge_vehicle'),

    path('operator/charge_vehicle/', views.charge_vehicle_view, name='charge_vehicle'),
    path('operator/repair_vehicle/', views.repair_vehicle_view, name='repair_vehicle'),
    path('visual/', views.visual_page, name='visual_page'),
    path('E-Scooter.html', views.e_scooter, name='e_scooter'),
    path('E-Bike.html', views.e_bike, name='e_bike'),
    path('report_malfunction/<int:vehicle_id>/', views.report_malfunction, name='report_malfunction'),
    path('move_vehicles/', views.move_vehicles, name='move_vehicles'),
    path('track_vehicle/', views.track_vehicle, name='track_vehicle'),
    path('send-message/', views.contact_us, name='send_message'),
    path('repair_vehicle/', views.repair_vehicle_view, name='repair_vehicle'),
    path('repair_vehicle/<int:vehicle_id>/', views.repair_vehicle, name='repair_vehicle'),
    path('api/getVehicleActivities', views.get_vehicle_activities, name='get_vehicle_activities'),
]