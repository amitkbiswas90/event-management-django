from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
# from django.contrib.auth.decorators import login_required
from event.froms import EventForm, CategoryForm, ParticipantForm  
from event.models import Event, Participant  
from django.utils import timezone
from django.db.models import Count, Q


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


def create_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.organizer = request.user  
            event.save()
            messages.success(request, "Event created successfully!")
            return redirect('create-event')
    else:
        form = EventForm()
    return render(request, 'create_event.html', {'form': form})  

def viewall_event(request):
    events = Event.objects.all().select_related('category')
    return render(request, 'view_events.html', {'events': events})


def update_event(request, id):
    event = Event.objects.get(id=id) 

    event_from = EventForm(instance=event)
    event_category_form = CategoryForm(instance=event.category if event.category else None)

    if request.method == "POST":
        event_from = EventForm(request.POST, instance=event)
        event_category_form = CategoryForm(request.POST, instance=event.category if event.category else None)

        if event_from.is_valid() and event_category_form.is_valid():
            event = event_from.save()

            event_category_form.save()

            messages.success(request, "Event Updated Successfully")
            return redirect('organizer-dashboard')  

    context = {"event_form": event_from, "category_form": event_category_form}
    return render(request, "event_update.html", context)

def delete_event(request, id):
    if request.method == 'POST':
        event = Event.objects.get(id=id)
        event.delete()
        messages.success(request, 'Event Deleted Successfully')
        return redirect('organizer-dashboard') 
    else:
        messages.error(request, 'Somthing went wrong')
        return redirect('organizer-dashboard')
    

def create_participants(request):
    if request.method == 'POST':
        form = ParticipantForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registration successfully completed!")
            return redirect('create-participant')  
    else:
        form = ParticipantForm()
    return render(request, 'participants_register.html', {'form': form}) 


def delete_participants(request, id):
    participant = Participant.objects.get(id=id)
    if request.method == 'POST':
        participant.delete()
        messages.success(request, "Participant deleted successfully!")
        return redirect('participants_list')  
    return render(request, 'confirm_delete.html', {'participant': participant})


def organizer_dashboard(request):
    now = timezone.now()
    today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    today_end = today_start + timezone.timedelta(days=1)

    total_pat = Participant.objects.count()

    counts = Event.objects.aggregate(
        total=Count('id'),
        upcoming=Count('id', filter=Q(date__gt=now)),
        past=Count('id', filter=Q(date__lt=now)),
        today=Count('id', filter=Q(date__range=(today_start, today_end))),
    )

    today_events = Event.objects.filter(date__range=(today_start, today_end))

    event_filter = request.GET.get('filter', 'total')
    if event_filter == 'upcoming':
        events = Event.objects.filter(date__gt=now)
    elif event_filter == 'past':
        events = Event.objects.filter(date__lt=now)
    else:
        events = Event.objects.all()

    context = {
        'total_events': counts['total'],
        'upcoming_events': counts['upcoming'],
        'past_events': counts['past'],
        'today_events': today_events,
        'events': events,  
        'event_filter': event_filter, 
        'total_pat':total_pat,
    }
    return render(request, 'organizar-dashbord.html', context)