from django.shortcuts import render, redirect,get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.models import User, Group
from django.contrib import messages
from django.contrib.auth import logout as auth_logout, login as auth_login
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Prefetch
from .form import CustomRegistrationForm, AssignRoleForm, CreateGroupForm, LoginForm
from event.models import Event, RSVP
from django.contrib.admin.views.decorators import staff_member_required

def admin_check(user):
    return user.is_active and (user.is_superuser or user.groups.filter(name='Admin').exists())

def is_organizer(user):
    return user.groups.filter(name='Organizer').exists()


def sign_up(request):
    if request.method == 'POST':
        forms = CustomRegistrationForm(request.POST)
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

def sign_in(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user.is_active:
                auth_login(request, user)
                return redirect('home')
            else:
                messages.error(request, "Please activate your account first.")
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = LoginForm()
    return render(request, "registration/login.html", {'form': form})

@login_required
def logout(request):
    auth_logout(request)
    return redirect('sign-in')

def activate_user(request, user_id, token):
    try:
        user = User.objects.get(id=user_id)
        if default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            messages.success(request, "Your account has been activated. You can now log in.")
            return redirect('sign-in')
    except User.DoesNotExist:
        return HttpResponse("User not found.")
    try:
        user = User.objects.get(id=user_id)
        if default_token_generator.check_token(user, token):
            if not user.is_active:
                user.is_active = True
                user.save()
                messages.success(request, "Your account has been activated. You can now log in.")
            else:
                messages.info(request, "Your account is already activated.")
            return redirect('sign-in')
        else:
            messages.error(request, "Invalid activation token.")
    except User.DoesNotExist:
        messages.error(request, "User not found.")
    return redirect('sign-in')

@user_passes_test(admin_check, login_url='no-permission')
def admin_dashboard(request):
    users = User.objects.prefetch_related(
        Prefetch('groups', queryset=Group.objects.all(), to_attr='all_groups')
    ).all()

    for user in users:
        user.group_name = user.all_groups[0].name if user.all_groups else 'No Group Assigned'
    
    return render(request, 'admin/admin-dashboard.html', {"users": users})


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


@login_required
def participant_dashboard(request):
    user_rsvps = RSVP.objects.filter(user=request.user).select_related('event')
    
    if request.method == 'POST':
        event_id = request.POST.get('event_id')
        
        if not event_id:
            return render(request, 'participant_dashboard.html', {
                'user_rsvps': user_rsvps,
                'error': 'Invalid event ID'
            })

        try:
            event = Event.objects.get(id=event_id)
        except Event.DoesNotExist:
            return render(request, 'participant_dashboard.html', {
                'user_rsvps': user_rsvps,
                'error': 'Event does not exist'
            })

        if RSVP.objects.filter(user=request.user, event=event).exists():
            return render(request, 'participant_dashboard.html', {
                'user_rsvps': user_rsvps,
                'error': 'You have already RSVP\'d to this event'
            })
            
        RSVP.objects.create(user=request.user, event=event)
        return redirect('participant-dashboard')
    
    return render(request, 'participant_dashboard.html', {'user_rsvps': user_rsvps})

@user_passes_test(admin_check, login_url='no-permission')
def participants_list(request):
    rsvps = RSVP.objects.select_related('user', 'event').all()
    return render(request, 'admin/participants_list.html', {'rsvps': rsvps})


@user_passes_test(admin_check, login_url='no-permission')
def delete_rsvp(request, rsvp_id):
    if request.method == 'POST':
        rsvp = get_object_or_404(RSVP, id=rsvp_id)
        rsvp.delete()
        messages.success(request, "RSVP deleted successfully!")
    return redirect('participants-list')

def no_permission(request):
    return render(request,'no_permission.html')