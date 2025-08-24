# Landing page with links to create/join event
def landing(request):
    return render(request, 'landing.html')
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Attendance
# Check-In view for admins to see participant list
def check_in(request, event_id):
    event = get_object_or_404(Event, event_id=event_id)
    role = request.GET.get('role', 'participant')
    phone = request.GET.get('phone', '')
    # Only allow admins
    if role.lower() != 'admin':
        return HttpResponseForbidden('Check-In access restricted to admins.')
    # Assume event.participant_phone_numbers is a comma-separated string
    participant_numbers = [n.strip() for n in (event.participant_phone_numbers or '').split(',') if n.strip()]
    # Ensure Attendance objects exist for all participants
    for p in participant_numbers:
        Attendance.objects.get_or_create(event=event, phone=p)
    attendance_map = {a.phone: a.checked_in for a in Attendance.objects.filter(event=event)}
    return render(request, 'check_in.html', {
        'event': event,
        'role': role,
        'phone': phone,
        'participants': participant_numbers,
        'attendance_map': attendance_map,
    })

# AJAX endpoint to mark attendance
@csrf_exempt
def mark_attendance(request):
    if request.method == 'POST':
        event_id = request.POST.get('event_id')
        phone = request.POST.get('phone')
        checked_in = request.POST.get('checked_in') == 'true'
        event = Event.objects.get(event_id=event_id)
        att, _ = Attendance.objects.get_or_create(event=event, phone=phone)
        att.checked_in = checked_in
        att.save()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False}, status=400)


from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseForbidden
import json
from .models import Event

def create_event(request):
    error_message = None
    if request.method == 'POST':
        # Get form data from POST request
        event_name = request.POST.get('event_name')
        event_description = request.POST.get('event_description')
        event_id = request.POST.get('event_id')
        participant_phone_numbers = request.POST.get('participant_phone_numbers', '')
        volunteer_phone_numbers = request.POST.get('volunteer_phone_numbers', '')

        # Check for duplicate Event ID
        if Event.objects.filter(event_id=event_id).exists():
            error_message = "An event with this Event ID already exists. Please choose a different Event ID."
        else:
            event = Event.objects.create(
                event_name=event_name,
                event_description=event_description,
                event_id=event_id,
                participant_phone_numbers=participant_phone_numbers,
                volunteer_phone_numbers=volunteer_phone_numbers
            )
            return redirect('event_dashboard', event_id=event.event_id)

    return render(request, 'create_event.html', {'error_message': error_message})

def join_event(request):
    from django.urls import reverse
    from django.http import HttpResponseRedirect
    message = ''
    if request.method == 'POST':
        event_id = request.POST.get('event_id')
        phone_number = request.POST.get('phone_number')
        try:
            event = Event.objects.get(event_id=event_id)
            participant_numbers = [num.strip() for num in event.participant_phone_numbers.split(',') if num.strip()]
            volunteer_numbers = [num.strip() for num in event.volunteer_phone_numbers.split(',') if num.strip()]
            if phone_number in volunteer_numbers:
                # Admin access
                url = reverse('event_dashboard', args=[event_id]) + f'?role=admin&phone={phone_number}'
                return HttpResponseRedirect(url)
            elif phone_number in participant_numbers:
                # Participant access
                url = reverse('event_dashboard', args=[event_id]) + f'?role=participant&phone={phone_number}'
                return HttpResponseRedirect(url)
            else:
                message = 'Phone number not allowed for this event.'
        except Event.DoesNotExist:
            message = 'Event ID not found.' 
    return render(request, 'join_event.html', {'message': message})

# Event dashboard view
def event_dashboard(request, event_id):
    # Get role and phone from query params
    role = request.GET.get('role', 'participant')
    phone = request.GET.get('phone', '')
    event = get_object_or_404(Event, event_id=event_id)
    return render(request, 'event_dashboard.html', {'event': event, 'role': role, 'phone': phone})

# In-memory storage for demonstration (replace with DB models for production)
from collections import defaultdict
import datetime
announcements_store = defaultdict(list)
public_messages_store = defaultdict(list)
tickets_store = defaultdict(list)

def announcement_channel(request, event_id):
    event = Event.objects.get(event_id=event_id)
    role = request.GET.get('role', 'participant')
    phone = request.GET.get('phone', '')
    if request.method == 'POST' and role == 'admin':
        text = request.POST.get('announcement')
        if text:
            announcements_store[event_id].append({
                'text': text,
                'timestamp': datetime.datetime.now(),
            })
    announcements = announcements_store[event_id]
    return render(request, 'announcement_channel.html', {'event': event, 'role': role, 'phone': phone, 'announcements': announcements})

def public_channel(request, event_id):
    event = Event.objects.get(event_id=event_id)
    role = request.GET.get('role', 'participant')
    phone = request.GET.get('phone', '')
    if request.method == 'POST':
        text = request.POST.get('message')
        if text:
            public_messages_store[event_id].append({
                'text': text,
                'sender': phone,
                'timestamp': datetime.datetime.now(),
            })
    messages = public_messages_store[event_id]
    return render(request, 'public_channel.html', {'event': event, 'role': role, 'phone': phone, 'messages': messages})

def ticket_channel(request, event_id):
    event = Event.objects.get(event_id=event_id)
    role = request.GET.get('role', 'participant')
    phone = request.GET.get('phone', '')
    # Handle ticket creation (participants) and response (admins)
    if request.method == 'POST':
        if role != 'admin':
            text = request.POST.get('ticket')
            if text:
                tickets_store[event_id].append({
                    'text': text,
                    'sender': phone,
                    'timestamp': datetime.datetime.now(),
                    'responses': []
                })
        else:
            # Admin response to a ticket
            response_text = request.POST.get('response')
            ticket_idx = request.POST.get('respond_ticket_id')
            if response_text and ticket_idx is not None:
                try:
                    ticket_idx = int(ticket_idx)
                    ticket = tickets_store[event_id][ticket_idx]
                    if 'responses' not in ticket:
                        ticket['responses'] = []
                    ticket['responses'].append({
                        'text': response_text,
                        'timestamp': datetime.datetime.now(),
                    })
                except (IndexError, ValueError):
                    pass
    # Only show tickets to admins or the ticket creator
    all_tickets = tickets_store[event_id]
    if role == 'admin':
        tickets = all_tickets
    else:
        tickets = [t for t in all_tickets if t['sender'] == phone]
    return render(request, 'ticket_channel.html', {'event': event, 'role': role, 'phone': phone, 'tickets': tickets})

# Walkie-talkie view for volunteers using PeerJS
def walkie_talkie(request, event_id):
    """Render walkie-talkie UI for volunteers and pass peer IDs.

    Access control: only phones listed in event.volunteer_phone_numbers may view.
    """
    event = get_object_or_404(Event, event_id=event_id)
    role = request.GET.get('role', 'participant')
    phone = request.GET.get('phone', '')

    # Build sanitized volunteer list
    volunteer_numbers = [n.strip() for n in (event.volunteer_phone_numbers or '').split(',') if n.strip()]

    # Only volunteers may access the walkie-talkie
    if phone not in volunteer_numbers or role != 'admin':
        return HttpResponseForbidden('Walkie-talkie access restricted to volunteers.')

    # Construct peer IDs for volunteers (peer id = "{event_id}-{phone}")
    my_peer_id = f"{event_id}-{phone}"
    other_peers = [f"{event_id}-{p}" for p in volunteer_numbers if p != phone]

    # JSON-encode other peer IDs for safe embedding into template JS
    other_peers_json = json.dumps(other_peers)

    return render(request, 'walkie_talkie.html', {
        'event': event,
        'role': role,
        'phone': phone,
        'my_peer_id': my_peer_id,
        'other_peers_json': other_peers_json,
    })
# Create your views here.

