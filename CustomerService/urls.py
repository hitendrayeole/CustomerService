"""
URL configuration for CustomerService project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from CustomerService import views
from . import views

urlpatterns = [

    path('logout/', views.logout_view, name='logout'), 
    path('admin/', admin.site.urls),
    path('',views.home),
    path('about/',views.about),
    path('signup/',views.signup),
    path('signin/',views.signin),
    path('contact/',views.contact),

    path('book/<int:unique>/', views.submit_booking, name='book_service'),
    path('servicebooked/',views.servicebooked),
    path('aadmin/',views.aadmin),
    path('addemp/',views.addemp),
    path('userinfo/', views.userinfo, name='userinfo'),
    path('employeeservicebooked/',views.employeeservicebooked),

    path("employeeinfo/", views.employeeinfo, name="employeeinfo"),
  
    path('ticketraised/',views.ticketraised),
  path("employeeinfocommon/<int:employee_id>/", views.employeeinfocommon, name="employeeinfocommon"),
    path("delete_employee/<int:employee_id>/", views.delete_employee, name="delete_employee"),
path('toggle_favorite/<int:employee_id>/', views.toggle_favorite, name='toggle_favorite'),

   path('favorites/', views.favorites, name='favorites'),
    path('bookservice/', views.bookservice, name='bookservice'),
    path('raiseticket/',views.raiseticket),
path('servicehistory/', views.servicehistory, name='servicehistory'),
    path('usercommon/<int:unique>',views.usercommon,name='usercommon'),
]
