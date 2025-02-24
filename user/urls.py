from django.urls import path
from .views import sign_up, sign_in, logout, activate_user, admin_dashboard,assign_role, create_group,group_list,participant_dashboard, participants_list, delete_rsvp, no_permission
urlpatterns = [
    path('sign-up/', sign_up, name='sign-up'),
    path('sign-in/', sign_in, name='sign-in'),
    path('logout/', logout, name='logout'),
    path('activate/<int:user_id>/<str:token>/', activate_user, name='activate-user'), 
    path('admin/dashboard/', admin_dashboard, name='admin-dashboard'),
    path('admin/<int:user_id>/assign-role/',assign_role, name='assign-role'),
    path('admin/create-group/',create_group, name='create-group'),
    path('admin/group-list/',group_list, name='group-list'),
    path('participant-dashboard/',participant_dashboard, name='participant-dashboard'),
    path('admin/participants-list/',participants_list, name='participants-list'),
    path('admin/delete-rsvp/<int:rsvp_id>/', delete_rsvp, name='delete-rsvp'),
    path('no-permission/',no_permission, name='no-permission'),
]
