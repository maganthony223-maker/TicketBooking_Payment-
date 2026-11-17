"""
URL configuration for ticketbooking_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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
from tickets import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", views.home, name="home"),
    path("register/", views.register, name="register"),
    path("login/", auth_views.LoginView.as_view(template_name="login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("matches/", views.matches, name="matches"),
    path("fixtures/", views.fixtures, name="fixtures"),
    path("teams/", views.teams, name="teams"),
    path("book/", views.book_tickets, name="book"),
    path("my-tickets/", views.my_tickets, name="my_tickets"),
    path("payments/", views.payment_history, name="payments"),
    path("pay/<int:pk>/", views.pay_booking, name="pay"),
]

