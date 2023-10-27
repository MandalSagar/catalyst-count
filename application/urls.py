from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('welcome/', views.welcome, name='welcome'),
    path('upload/', views.upload_csv, name='upload_csv'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('query/', views.query, name='query'),
    path('um/', views.user_management, name='um'),
    path('user/add/', views.add_user, name='add_user'),
    path('user/delete/<int:user_id>/', views.delete_user, name='delete_user'),
]