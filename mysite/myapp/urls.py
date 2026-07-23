from django.urls import path
from . import views

urlpatterns = [
    path('', views.builder, name='builder'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    path('dashboard/', views.dashboard, name='dashboard'),

    path('submit/', views.submit_resume, name='submit_resume'),
    path('edit/<int:resume_id>/', views.builder, name='builder_edit'),
    path('edit/<int:resume_id>/submit/', views.submit_resume, name='submit_resume_edit'),

    path('download/<int:resume_id>/', views.download_resume, name='download_resume'),
    path('delete/<int:resume_id>/', views.delete_resume, name='delete_resume'),
]
