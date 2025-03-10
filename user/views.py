from django.http import HttpResponse
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.models import User, Group
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.db.models import Prefetch
from .form import CustomRegistrationForm, AssignRoleForm, CreateGroupForm, LoginForm,CustomUserChangeForm, CustomPasswordChangeForm, CustomPasswordResetConfirmForm
from event.models import Event, RSVP
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.views.generic import TemplateView, View, ListView,UpdateView
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordResetView, PasswordResetDoneView,PasswordResetConfirmView
from django.urls import reverse_lazy
from .form import CustomUserChangeForm, CustomPasswordChangeForm, CustomPasswordResetForm
from django.contrib.auth import get_user_model
User = get_user_model()


def admin_check(user):
    return user.is_active and (user.is_superuser or user.groups.filter(name='Admin').exists())

def is_organizer(user):
    return user.groups.filter(name='Organizer').exists()


def sign_up(request):
    if request.method == 'POST':
        forms = CustomRegistrationForm(request.POST,request.FILES)
        if forms.is_valid():
            user = forms.save(commit=False)
            user.set_password(forms.cleaned_data.get('password1'))
            user.is_active = False  
            user.save()

            default_group, created = Group.objects.get_or_create(name='Default Group')
            user.groups.add(default_group)  

            messages.success(request, "A confirmation email has been sent. Please check your email.")
            return redirect('sign-in')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        forms = CustomRegistrationForm()

    return render(request, "registration/register.html", {"forms": forms})

class SignInView(LoginView):
    form_class = LoginForm
    template_name = 'registration/login.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        user = form.get_user()
        if user.is_active:
            return super().form_valid(form)
        messages.error(self.request, "Please activate your account first.")
        return redirect(self.get_success_url())
    

class CustomLogoutView(LoginRequiredMixin, LogoutView):
    next_page = reverse_lazy('sign-in') 

class AdminDashboardView(UserPassesTestMixin, TemplateView):
    template_name = 'admin/admin-dashboard.html'
    login_url = 'no-permission'

    def test_func(self):
        return admin_check(self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        users = User.objects.prefetch_related(
            Prefetch('groups', queryset=Group.objects.all(), to_attr='all_groups')
        ).all()
        
        for user in users:
            user.group_name = user.all_groups[0].name if user.all_groups else 'No Group Assigned'
        
        context['users'] = users
        return context

@user_passes_test(admin_check, login_url='sign-in')
def assign_role(request, user_id):
    try:
        user = User.objects.get(id=user_id)
        if request.method == 'POST':
            form = AssignRoleForm(request.POST)
            if form.is_valid():
                role = form.cleaned_data['role']
                user.groups.clear()
                user.groups.add(role)
                messages.success(request, f"User {user.username} has been assigned to the {role.name} role.")
                return redirect('admin-dashboard')
        else:
            form = AssignRoleForm()
        return render(request, 'admin/assign_role.html', {"form": form, "user": user})
    except User.DoesNotExist:
        messages.error(request, "User not found.")
        return redirect('admin-dashboard')

@user_passes_test(admin_check, login_url='no-permission')
def create_group(request):
    if request.method == 'POST':
        form = CreateGroupForm(request.POST)
        if form.is_valid():
            group = form.save()
            messages.success(request, f"Group {group.name} has been created successfully.")
            return redirect('group-list')
    else:
        form = CreateGroupForm()
    return render(request, "admin/create_group.html", {'form': form})

def group_list(request):
    groups = Group.objects.prefetch_related('permissions').all()
    return render(request, 'admin/group_list.html', {'groups': groups})


class ParticipantDashboardView(LoginRequiredMixin, View):
    template_name = 'participant_dashboard.html'

    def get(self, request):
        user_rsvps = RSVP.objects.filter(user=request.user).select_related('event')
        return render(request, self.template_name, {'user_rsvps': user_rsvps})

    def post(self, request):
        user_rsvps = RSVP.objects.filter(user=request.user).select_related('event')
        event_id = request.POST.get('event_id')

        if not event_id:
            return self.render_with_error(user_rsvps, 'Invalid event ID')

        try:
            event = Event.objects.get(id=event_id)
        except Event.DoesNotExist:
            return self.render_with_error(user_rsvps, 'Event does not exist')

        if RSVP.objects.filter(user=request.user, event=event).exists():
            return self.render_with_error(user_rsvps, 'You have already RSVP\'d to this event')

        RSVP.objects.create(user=request.user, event=event)
        return redirect('participant-dashboard')

    def render_with_error(self, rsvps, error):
        return render(self.request, self.template_name, {
            'user_rsvps': rsvps,
            'error': error
        })

class ParticipantsListView(UserPassesTestMixin, ListView):
    template_name = 'admin/participants_list.html'
    context_object_name = 'rsvps'
    login_url = reverse_lazy('no-permission')  
    def test_func(self):
        user = self.request.user
        return user.is_active and (user.is_superuser or user.groups.filter(name='Admin').exists())
    def get_queryset(self):
        return RSVP.objects.select_related('user', 'event').all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


@user_passes_test(admin_check, login_url='no-permission')
def delete_rsvp(request, rsvp_id):
    if request.method == 'POST':
        rsvp = get_object_or_404(RSVP, id=rsvp_id)
        rsvp.delete()
        messages.success(request, "RSVP deleted successfully!")
    return redirect('participants-list')

def no_permission(request):
    return render(request,'no_permission.html')

def activate_user(request, user_id, token):
    user = get_object_or_404(User, id=user_id)
    print(f"[DEBUG] Validating token for User {user.id}: is_active={user.is_active}, token={token}")
    if user.is_active:
        return HttpResponse("User already active.")
    
    is_valid = default_token_generator.check_token(user, token)
    print(f"[DEBUG] Token valid: {is_valid}")
    if is_valid:
        user.is_active = True
        user.save()
        return redirect('sign-in')
    else:
        return HttpResponse("Invalid activation link.")
    


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'users/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context

class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = CustomUserChangeForm
    template_name = 'users/edit_profile.html'
    success_url = reverse_lazy('profile')

    def get_object(self):
        return self.request.user

    def form_valid(self, form):
        messages.success(self.request, "Profile updated successfully!")
        return super().form_valid(form)

class CustomPasswordChangeView(PasswordChangeView):
    form_class = CustomPasswordChangeForm
    success_url = reverse_lazy('profile')
    template_name = 'users/change_password.html'

    def form_valid(self, form):
        messages.success(self.request, "Password changed successfully!")
        return super().form_valid(form)

class CustomPasswordResetView(PasswordResetView):
    form_class = CustomPasswordResetForm
    template_name = 'users/password_reset.html'
    html_email_template_name = 'users/password_reset_email.html' 
    success_url = reverse_lazy('sign-in')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['protocol'] = 'https' if self.request.is_secure() else 'http'
        context['domain'] = self.request.get_host()
        return context

    def form_valid(self, form):
        messages.success(
            self.request, 'A Reset meail sent. Please check your mail'
        )
        return super().form_valid(form)

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    form_class = CustomPasswordResetConfirmForm
    template_name = 'users/password_reset.html'
    success_url = reverse_lazy('sign-in')

    def form_valid(self, form):
        messages.success(
            self.request, 'Password Reset Successful'
        )
        return super().form_valid(form)
