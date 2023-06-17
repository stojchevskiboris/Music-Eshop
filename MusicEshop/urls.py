"""
URL configuration for MusicEshop project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from shop import views
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name="index"),
    path('addToCart/<int:i_id>/', views.addToCart, name="addToCart"),
    path('cart/', views.cart, name="cart"),
    path('categories/', views.categories, name="categories"),
    path('contact/', views.contact, name="contact"),
    path('about/', views.about, name="about"),
    path('instruments/', views.instruments, name="instruments"),
    path('add/', views.add, name="add"),

    path("accounts/", include("django.contrib.auth.urls")),
    path("accounts/profile/", views.loginView, name="loginView"),
    path("logout/", views.logoutView, name="logoutView"),


    path("zicani/", views.zicani, name="zicani"),
    path("duvacki/", views.duvacki, name="duvacki"),
    path("udarni/", views.udarni, name="udarni"),
    path("klavijatura/", views.klavijatura, name="klavijatura"),

] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
