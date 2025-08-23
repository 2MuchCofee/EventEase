from django.db import models

# Event model to store event details in the database
class Event(models.Model):
    # Name of the event
    event_name = models.CharField(max_length=255)
    # Description of the event
    event_description = models.TextField()
    # Unique Event ID (can be used for joining the event)
    event_id = models.CharField(max_length=100, unique=True)
    # Comma-separated phone numbers of participants (to be verified later)
    participant_phone_numbers = models.TextField(help_text="Comma-separated phone numbers of participants")
    # Comma-separated phone numbers of volunteers (admin access)
    volunteer_phone_numbers = models.TextField(help_text="Comma-separated phone numbers of volunteers")

    def __str__(self):
        return f"{self.event_name} ({self.event_id})"