from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('tools/', views.tools_page, name='tools'),
    path('history/', views.history, name='history'),
    path('file-tools/', views.file_tools, name='file_tools'),
    path('download/text/<int:pk>/', views.download_text, name='download_text'),
    path('download/pdf/<int:pk>/', views.download_pdf, name='download_pdf'),
    path('login/', auth_views.LoginView.as_view(template_name='tools/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', views.signup, name='signup'),
]
