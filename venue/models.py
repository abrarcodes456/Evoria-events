from django.db import models
from django.contrib.auth.models import User  

# Create your models here. django.db import models


# ── EVENT TYPE CHOICES ──────────────────────────────
EVENT_TYPES = [
    ('marriage', 'Marriage Function'),
    ('birthday', 'Birthday Party'),
    ('college', 'College Function'),
    ('school', 'School Event'),
    ('corporate', 'Corporate Event'),
    ('gathering', 'Get-Together'),
    ('social', 'Social Event'),
    ('other', 'Other Events'),
]

# ── BOOKING STATUS CHOICES ───────────────────────────
STATUS_CHOICES = [
    ('confirmed', 'Confirmed'),
    ('completed', 'Completed'),
    ('cancelled', 'Cancelled'),
]
# ── USER PROFILE MODEL ───────────────────────────────
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15)

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.phone}"

# ── BOOKING MODEL ────────────────────────────────────
class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event_type = models.CharField(max_length=50, choices=EVENT_TYPES)
    event_name = models.CharField(max_length=200)
    event_date = models.DateField()
    guest_count = models.IntegerField()
    phone = models.CharField(max_length=15)
    catering = models.BooleanField(default=False)
    special_requests = models.TextField(blank=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.event_name} - {self.user.get_full_name()}"

    class Meta:
        ordering = ['-created_at']

# ── CONTACT MESSAGE MODEL ────────────────────────────
class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} - {self.subject}"

    class Meta:
        ordering = ['-created_at']