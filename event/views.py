from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required,user_passes_test
from event.forms import EventForm, CategoryForm
from django.contrib.auth.models import User
from event.models import Event, RSVP
from django.utils import timezone
from django.db.models import Count, Q

def is_organizer(user):
    return user.groups.filter(name='Organizer').exists()
def admin_check(user):
    return user.is_active and (user.is_superuser or user.groups.filter(name='Admin').exists())

@login_required
def create_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Category created successfully!")
            return redirect('create-category')
    else:
        form = CategoryForm()
    return render(request, 'create_category.html', {'form': form})

@login_required
def create_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            event = form.save(commit=False)
            event.organizer = request.user
            event.save()
            messages.success(request, "Event created successfully!")
            return redirect('create-event')
    else:
        form = EventForm()
    return render(request, 'create_event.html', {'form': form})

def event_list(request):
    query = request.GET.get('q', '')
    
    if query:
        events = Event.objects.filter(
            Q(name__icontains=query) | 
            Q(location__icontains=query)
        ).distinct()
    else:
        events = Event.objects.all()
    
    context = {
        'events': events,
        'search_query': query
    }
    return render(request, 'event_list.html', context)

@login_required
def update_event(request, id):
    event = get_object_or_404(Event, id=id)
    event_form = EventForm(instance=event)
    category_form = CategoryForm(instance=event.category)

    if request.method == "POST":
        event_form = EventForm(request.POST, request.FILES, instance=event)
        category_form = CategoryForm(request.POST, instance=event.category)

        if event_form.is_valid() and category_form.is_valid():
            event_form.save()
            category_form.save()
            messages.success(request, "Event Updated Successfully")
            return redirect('organizer-dashboard')

    context = {"event_form": event_form, "category_form": category_form}
    return render(request, "event_update.html", context)

@login_required
def delete_event(request, id):
    event = get_object_or_404(Event, id=id)
    if request.method == 'POST':
        event.delete()
        messages.success(request, 'Event Deleted Successfully')
    return redirect('organizer-dashboard')

@login_required
@user_passes_test(lambda u: is_organizer(u) or admin_check(u), login_url='no-permission')
def organizer_dashboard(request):
    now = timezone.now()
    today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    today_end = today_start + timezone.timedelta(days=1)
    
    event_filter = request.GET.get('filter', 'total')
    
    # For Event RSVPs (using related_name='rsvps')
    events = Event.objects.annotate(rsvp_count=Count('rsvps')).order_by('-date')
    
    if event_filter == 'upcoming':
        events = events.filter(date__gt=now)
    elif event_filter == 'past':
        events = events.filter(date__lt=now)
    
    counts = {
        'total': Event.objects.count(),
        'upcoming': Event.objects.filter(date__gt=now).count(),
        'past': Event.objects.filter(date__lt=now).count(),
        'today': Event.objects.filter(date__range=(today_start, today_end)).count(),
    }

    context = {
        'total_events': counts['total'],
        'upcoming_events': counts['upcoming'],
        'past_events': counts['past'],
        'today_events': Event.objects.filter(date__range=(today_start, today_end)),
        'events': events,
        'event_filter': event_filter,
        'total_pat': User.objects.filter(rsvp__isnull=False).distinct().count(),  
    }
    return render(request, 'organizar-dashbord.html', context)

@login_required
def rsvp_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    rsvp, created = RSVP.objects.get_or_create(
        user=request.user,
        event=event
    )

    if created:
        messages.success(request, 'RSVP successful!')
    else:
        messages.warning(request, 'You already RSVPed for this event!')

    return redirect('event-detail', event_id=event.id)

@login_required
def participant_dashboard(request):
    rsvps = RSVP.objects.filter(user=request.user).select_related('event')
    return render(request, 'participant_dashboard.html', {'rsvps': rsvps})