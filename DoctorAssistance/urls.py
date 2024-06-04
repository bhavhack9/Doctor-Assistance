"""DoctorAssistance URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from DoctorAssistanceApp.views import *

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', index,name='index'),
    path('login/', login,name='login'),
    path('logout/', logout,name='logout'),
    path('register/', register,name='register'),
    path('forgot_password/', forgotPassword_view, name='forgot_password'),
    path('createAccount/', createAccount,name='create_account'),
    path('loginAccount/', loginAccount,name='login_account'),
    path('backup_password/', backup_password,name='backup_password'),
    path('home_view/', home_view,name='home_view'),

    path('Admin/doctor/', admin_doctor, name='admin_doctor'),
    
    path('User/chatbot/', chatbot, name='chatbot'),
    path('predict_disease/', predict_disease, name='predict_disease'),
    path('predict_initial_disease/', predict_initial_disease, name='predict_initial_disease'),
    path('generate_pdf_view/', generate_pdf_view, name='generate_pdf_view'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)