from django.shortcuts import render
from django.db.models import Q
from event.models import Event

def home(request):
    search_query = request.GET.get('q', '')
    events = Event.objects.all()
    
    if search_query:
        events = events.filter(
            Q(name__icontains=search_query) |
            Q(location__icontains=search_query)
        )
    
    context = {
        'events': events,
        'search_query': search_query,
        'user_groups': request.user.groups.values_list('name', flat=True) 
                      if request.user.is_authenticated 
                      else []
    }
    
    return render(request, 'search_event.html', context)


def event_view(request):
    events = Event.objects.all()
    return render(request, "eventviw.html", {"events": events})