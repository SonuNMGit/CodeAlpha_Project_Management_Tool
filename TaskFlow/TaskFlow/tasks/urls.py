from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),  
    path('login/', views.login_view, name='login'),  
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', views.signup_view, name='signup'),  
    path('password-reset/', views.password_reset, name='password_reset'), 
    path('manager-home/', views.manager_home, name='manager_home'),
    path('team-member-home/', views.team_member_home, name='team_member_home'), 
    path('create-project/', views.create_project, name='create_project'),
    path('edit-project/<int:project_id>/', views.edit_project, name='edit_project'),
    path('delete-project/<int:project_id>/', views.delete_project, name='delete_project'),
    path('assign-task/<int:project_id>/', views.assign_task, name='assign_task'),
    path('tasks/edit/<int:task_id>/', views.task_edit, name='edit_task'),
    path('tasks/delete/<int:task_id>/', views.task_delete, name='delete_task'),
    path('save_task_link/<int:task_id>/', views.save_task_link, name='save_task_link'),
    path('delete_task_link/<int:link_id>/', views.delete_task_link, name='delete_task_link'),
    path('task/<int:task_id>/add_comment/', views.add_comment, name='add_comment'),
    path('comment/<int:comment_id>/delete/', views.delete_comment, name='delete_comment'),
]
