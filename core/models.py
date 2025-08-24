
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

# Attendance model must be defined after Event
class Attendance(models.Model):
	event = models.ForeignKey(Event, on_delete=models.CASCADE)
	phone = models.CharField(max_length=20)
	checked_in = models.BooleanField(default=False)

	class Meta:
		unique_together = ('event', 'phone')


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

# Attendance model must be defined after Event
class Attendance(models.Model):
	event = models.ForeignKey(Event, on_delete=models.CASCADE)
	phone = models.CharField(max_length=20)
	checked_in = models.BooleanField(default=False)

	class Meta:
		unique_together = ('event', 'phone')