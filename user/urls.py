from django.urls import path
from .views import  assign_role, create_group,group_list, delete_rsvp, no_permission,activate_user,sign_up
from .views import (
    AdminDashboardView,
    SignInView,
    CustomLogoutView,
    ParticipantDashboardView,
    ParticipantsListView,
    ProfileView,
    ProfileUpdateView,
    CustomPasswordChangeView,
    CustomPasswordResetView,
    CustomPasswordResetConfirmView,
)

urlpatterns = [
    path('admin/dashboard/', AdminDashboardView.as_view(), name='admin-dashboard'),
    path('participants-list/', ParticipantsListView.as_view(), name='participants-list'),
    path('sign-up/', sign_up, name='sign-up'),
    path('sign-in/', SignInView.as_view(), name='sign-in'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('dashboard/', ParticipantDashboardView.as_view(), name='participant-dashboard'),
    path('activate/<int:user_id>/<str:token>/', activate_user, name='activate-user'), 
    path('admin/<int:user_id>/assign-role/', assign_role, name='assign-role'),
    path('admin/create-group/',create_group, name='create-group'),
    path('admin/group-list/',group_list, name='group-list'),
    path('admin/delete-rsvp/<int:rsvp_id>/', delete_rsvp, name='delete-rsvp'),
    path('no-permission/',no_permission, name='no-permission'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('profile/edit/', ProfileUpdateView.as_view(), name='edit_profile'),
    path('password/change/', CustomPasswordChangeView.as_view(), name='password_change'),
    path('password/reset/', CustomPasswordResetView.as_view(), name='password_reset'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('profile/edit/', ProfileUpdateView.as_view(), name='edit-profile'),
    path('password/change/', CustomPasswordChangeView.as_view(), name='change-password'),
    path('password/reset/', CustomPasswordResetView.as_view(), name='password-reset'),
    path('password/confirm/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm')
]


