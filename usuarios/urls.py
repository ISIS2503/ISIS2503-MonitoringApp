from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('create/', views.usuario_create, name='usuarioCreate'),
    path('list/', views.usuario_list, name='usuarioList'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('user_reports/', views.user_reports, name='user_reports'),
]
