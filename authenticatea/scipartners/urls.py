from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('profile/', views.profile_view, name='profile'),
    path('logout/', views.logout_view, name='logout'),
    path('create_project/', views.create_project_view, name='create_project'),
    path('send_message/<int:receiver_id>/', views.send_message_view, name='send_message'),
    path('user_profile/<int:user_id>/', views.user_profile_view, name='user_profile'),
    path('list_projects/', views.list_projects, name='list_projects'),
    path('notification/', views.notification_view, name='notification'),
    path('feedback/<int:project_id>/', views.feedback_view, name='feedback'),
    path('privacy_settings/', views.privacy_settings_view, name='privacy_settings'),
    path('add_project_tag/<int:project_id>/', views.add_project_tag_view, name='add_project_tag'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('project_details/<int:project_id>/', views.project_details_view, name='project_details'),
    path('search_projects/', views.search_projects_view, name='search_projects'),
    path('inbox/', views.inbox_view, name='inbox'),
    path('user_settings/', views.user_settings_view, name='user_settings'),
    path('deactivate_account/', views.deactivate_account_view, name='deactivate_account'),
    path('account_deactivated/', views.account_deactivated_view, name='account_deactivated'),
    path('edit_project/<int:project_id>/', views.edit_project_view, name='edit_project'),
    path('collaborate_on_project/<int:project_id>/', views.collaborate_on_project_view, name='collaborate_on_project'),
    path('deactivate_project/<int:project_id>/', views.deactivate_project_view, name='deactivate_project'),
    path('new_project_opportunity/', views.new_project_opportunity, name='new_project_opportunity'),
    path('new_message/<str:recipient_user>/', views.new_message, name='new_message'),
    path('user_profile/<int:user_id>/', views.user_profile, name='user_profile'),
    path('collaborate_on_project/<int:project_id>/', views.collaborate_on_project, name='collaborate_on_project'),
    path('deactivate_project/<int:project_id>/', views.deactivate_project_view, name='deactivate_project'),

    
]
