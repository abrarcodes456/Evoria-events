from urllib import request

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from .models import Booking, UserProfile, ContactMessage

def is_admin(user):
    return user.is_staff

# ── 1. HOME VIEW ─────────────────────────────────────
def home(request):
    return render(request, 'home.html')

# ── 2. ABOUT VIEW ────────────────────────────────────
def about(request):
    event_types = [
        ('💒', 'Marriage Function'),
        ('🎂', 'Birthday Party'),
        ('🎓', 'College Function'),
        ('🏫', 'School Event'),
        ('💼', 'Corporate Event'),
        ('👨‍👩‍👧', 'Get-Together'),
        ('🎉', 'Social Event'),
        ('✨', 'Other Events'),
    ]
    return render(request, 'about.html', {'event_types': event_types})

# ── 3. REGISTER VIEW ─────────────────────────────────
def register_view(request):

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':

        # Get data from form
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        # Check passwords match
        if password1 != password2:
            return render(request, 'register.html', {
                'error': 'Passwords do not match!'
            })

        # Check username already exists
        if User.objects.filter(username=username).exists():
            return render(request, 'register.html', {
                'error': 'This username is already taken! Please choose another.'
            })

        # Check email already exists
        if User.objects.filter(email=email).exists():
            return render(request, 'register.html', {
                'error': 'An account with this email already exists!'
            })

        # Create the user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password1,
            first_name=first_name,
            last_name=last_name,
        )

        # Create user profile with phone
        UserProfile.objects.create(
            user=user,
            phone=phone
        )

        # Login automatically
        login(request, user)

        # Show success message
        messages.success(request, f'Welcome to EVORIA Events, {first_name}!')

        return redirect('home')

    return render(request, 'register.html')

# ── 4. LOGIN VIEW ─────────────────────────────────────
def login_view(request):

    # If already logged in → send to home
    if request.user.is_authenticated:
        return redirect('home')

    # If user submitted form
    if request.method == 'POST':

        # Get email and password from form
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Find user by email
        try:
            username = request.POST.get('username')
            auth_user = authenticate(
            request,
            username=username,
            password=password
            )
            if auth_user is not None:
                # Password correct → login!
                login(request, auth_user)

                # If admin → go to dashboard
                if auth_user.is_staff:
                    return redirect('admin_dashboard')

                # If normal user → go to home
                messages.success(request, f'Welcome back, {auth_user.first_name}!')
                return redirect('home')

            else:
                # Wrong password
                return render(request, 'login.html', {
                    'error': 'Incorrect password! Please try again.'
                })

        except User.DoesNotExist:
            if auth_user is not None:
                login(request, auth_user)
                if auth_user.is_staff:
                    return redirect('admin_dashboard')
                messages.success(request, f'Welcome back, {auth_user.first_name}!')
                return redirect('home')
            else:
                return render(request, 'login.html', {
                    'error': 'Invalid username or password!'
    })

    # GET request → show empty login form
    return render(request, 'login.html')

# ── 5. LOGOUT VIEW ────────────────────────────────────
def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out successfully!')
    return redirect('home')

# ── 6. BOOK VIEW ─────────────────────────────────────
@login_required
def book(request):

    # Event types for dropdown
    event_types = [
        ('marriage', 'Marriage Function'),
        ('birthday', 'Birthday Party'),
        ('college', 'College Function'),
        ('school', 'School Event'),
        ('corporate', 'Corporate Event'),
        ('gathering', 'Get-Together'),
        ('social', 'Social Event'),
        ('other', 'Other Events'),
    ]

    # If user submitted form
    if request.method == 'POST':

        # Get all form data
        event_type = request.POST.get('event_type')
        event_name = request.POST.get('event_name')
        event_date = request.POST.get('event_date')
        guest_count = request.POST.get('guest_count')
        phone = request.POST.get('phone')
        catering = request.POST.get('catering')
        special_requests = request.POST.get('special_requests', '')

        # ── DATE CONFLICT CHECK ──────────────────────
        from datetime import datetime
        event_date_obj = datetime.strptime(event_date, '%Y-%m-%d').date()

        existing_booking = Booking.objects.filter(
            event_date=event_date_obj,
            status='confirmed'
        ).exists()

        if existing_booking:
            return render(request, 'book.html', {
                'event_types': event_types,
                'error': f'We sincerely regret that your preferred date — {event_date_obj.strftime("%d %B %Y")} — is currently reserved for another celebration. We kindly request you to select an alternative date. We look forward to hosting your special occasion at EVORIA Events!'
            })

        # ── CALCULATE PRICE ──────────────────────────
        base_price = 35000
        catering_price = 20000

        if catering:
            total_price = base_price + catering_price
            catering_bool = True
        else:
            total_price = base_price
            catering_bool = False

        # ── SAVE BOOKING ─────────────────────────────
        booking = Booking.objects.create(
            user=request.user,
            event_type=event_type,
            event_name=event_name,
            event_date=event_date_obj,
            guest_count=guest_count,
            phone=phone,
            catering=catering_bool,
            special_requests=special_requests,
            total_price=total_price,
            status='confirmed',
        )

        # ── SEND CONFIRMATION EMAIL ───────────────────
        catering_text = 'Yes — Included' if catering_bool else 'No — Not Included'

        subject = 'Booking Confirmed — EVORIA Events 🎉'

        message = f"""
Dear {request.user.first_name},

Thank you for choosing EVORIA Events for your special occasion!
We are delighted to confirm your booking.

Your Booking Details:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Event Name    : {event_name}
Event Type    : {dict(event_types).get(event_type)}
Event Date    : {event_date_obj.strftime('%d %B %Y')}
No. of Guests : {guest_count}
Catering      : {catering_text}
Total Amount  : ₹{total_price:,}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

For any queries please contact us:
📞 +91 63795 95388
📧 {settings.EMAIL_HOST_USER}

We look forward to hosting your celebration!

Warm regards,
EVORIA Events Team
Theni, Tamil Nadu
        """

        try:
            send_mail(
                subject,
                message,
                settings.EMAIL_HOST_USER,
                [request.user.email],
                fail_silently=False,
            )
        except Exception as e:
            # Email failed but booking still saved!
            print(f"Email error: {e}")

        # Show success message
        messages.success(
            request,
            f'Your booking for {event_name} on {event_date_obj.strftime("%d %B %Y")} has been confirmed! A confirmation email has been sent to {request.user.email}'
        )

        return redirect('my_bookings')

    # GET request → show booking form
    return render(request, 'book.html', {'event_types': event_types})

# ── 7. MY BOOKINGS VIEW ───────────────────────────────
@login_required
def my_bookings(request):

    # ── AUTO COMPLETE PAST EVENTS ─────────────────────
    today = timezone.now().date()

    Booking.objects.filter(
        user=request.user,
        status='confirmed',
        event_date__lt=today
    ).update(status='completed')

    # ── GET USER'S BOOKINGS ───────────────────────────
    bookings = Booking.objects.filter(user=request.user)

    return render(request, 'my_bookings.html', {'bookings': bookings})


# ── 8. CANCEL BOOKING VIEW ────────────────────────────
@login_required
def cancel_booking(request, booking_id):

    # Get booking — if not found show 404
    booking = get_object_or_404(
        Booking,
        id=booking_id,
        user=request.user
    )

    # Only confirmed bookings can be cancelled
    if booking.status == 'confirmed':

        # Update status to cancelled
        booking.status = 'cancelled'
        booking.save()

        # ── SEND CANCELLATION EMAIL ───────────────────
        subject = 'Booking Cancelled — EVORIA Events'

        message = f"""
Dear {request.user.first_name},

We regret to inform you that your booking has been cancelled.

Cancelled Booking Details:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Event Name  : {booking.event_name}
Event Date  : {booking.event_date.strftime('%d %B %Y')}
Total Amount: ₹{booking.total_price:,}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

We sincerely apologize for any inconvenience caused.
We hope to have the opportunity to serve you again
in the future.

For any queries please contact us:
📞 +91 63795 95388

Warm regards,
EVORIA Events Team
Theni, Tamil Nadu
        """

        try:
            send_mail(
                subject,
                message,
                settings.EMAIL_HOST_USER,
                [request.user.email],
                fail_silently=False,
            )
        except Exception as e:
            print(f"Email error: {e}")

        messages.success(
            request,
            f'Your booking for {booking.event_name} has been cancelled successfully!'
        )

    else:
        messages.error(
            request,
            'This booking cannot be cancelled!'
        )

    return redirect('my_bookings')

# ── 9. ADMIN DASHBOARD VIEW ───────────────────────────
@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):

    # ── AUTO COMPLETE PAST EVENTS ─────────────────────
    today = timezone.now().date()

    Booking.objects.filter(
        status='confirmed',
        event_date__lt=today
    ).update(status='completed')

    # ── STATISTICS ────────────────────────────────────
    total_users = User.objects.filter(is_staff=False).count()
    total_bookings = Booking.objects.count()
    confirmed_bookings = Booking.objects.filter(status='confirmed').count()
    completed_bookings = Booking.objects.filter(status='completed').count()
    cancelled_bookings = Booking.objects.filter(status='cancelled').count()
    upcoming_bookings = Booking.objects.filter(
        status='confirmed',
        event_date__gte=today
    ).count()

    # ── GET ALL BOOKINGS ──────────────────────────────
    recent_bookings = Booking.objects.all()

    # ── GET ALL USERS ─────────────────────────────────
    all_users = User.objects.filter(is_staff=False)

    context = {
        'total_users': total_users,
        'total_bookings': total_bookings,
        'confirmed_bookings': confirmed_bookings,
        'completed_bookings': completed_bookings,
        'cancelled_bookings': cancelled_bookings,
        'upcoming_bookings': upcoming_bookings,
        'recent_bookings': recent_bookings,
        'all_users': all_users,
    }

    return render(request, 'admin_dashboard.html', context)


# ── 10. UPDATE STATUS VIEW ────────────────────────────
@login_required
@user_passes_test(is_admin)
def update_status(request, booking_id):

    booking = get_object_or_404(Booking, id=booking_id)

    if request.method == 'POST':
        new_status = request.POST.get('status')

        if new_status in ['confirmed', 'completed', 'cancelled']:
            booking.status = new_status
            booking.save()

            # If admin cancels → send cancellation email to user
            if new_status == 'cancelled':
                subject = 'Booking Cancelled — EVORIA Events'
                message = f"""
Dear {booking.user.first_name},

We regret to inform you that your booking
has been cancelled by our team.

Cancelled Booking Details:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Event Name  : {booking.event_name}
Event Date  : {booking.event_date.strftime('%d %B %Y')}
Total Amount: ₹{booking.total_price:,}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

We sincerely apologize for any inconvenience caused.
Please contact us for further assistance.

📞 +91 63795 95388

Warm regards,
EVORIA Events Team
Theni, Tamil Nadu
                """

                try:
                    send_mail(
                        subject,
                        message,
                        settings.EMAIL_HOST_USER,
                        [booking.user.email],
                        fail_silently=False,
                    )
                except Exception as e:
                    print(f"Email error: {e}")

            messages.success(
                request,
                f'Booking status updated to {new_status} successfully!'
            )

    return redirect('admin_dashboard')

# ── 11. CONTACT VIEW ──────────────────────────────────
def contact(request):

    if request.method == 'POST':

        # Get form data
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        # ── SAVE MESSAGE TO DATABASE ──────────────────
        ContactMessage.objects.create(
            name=name,
            email=email,
            phone=phone,
            subject=subject,
            message=message,
        )

        # ── SEND EMAIL TO USER ────────────────────────
        email_subject = 'Message Received — EVORIA Events ✅'

        email_message = f"""
Dear {name},

Thank you for reaching out to EVORIA Events!

We have successfully received your message and
our team will get back to you within 24 hours.

Your Message Details:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Subject : {subject}
Message : {message}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

For urgent queries please contact us directly:
📞 +91 63795 95388

Warm regards,
EVORIA Events Team
Theni, Tamil Nadu
        """

        try:
            send_mail(
                email_subject,
                email_message,
                settings.EMAIL_HOST_USER,
                [email],
                fail_silently=False,
            )
        except Exception as e:
            print(f"Email error: {e}")

        messages.success(
            request,
            'Thank you for contacting us! We have received your message and will get back to you within 24 hours.'
        )

        return redirect('contact')

    return render(request, 'contact.html')


# ── 12. ADMIN MESSAGES VIEW ───────────────────────────
@login_required
@user_passes_test(is_admin)
def admin_messages(request):

    # Get all messages — unread first!
    all_messages = ContactMessage.objects.all()

    # Count unread messages
    unread_count = ContactMessage.objects.filter(is_read=False).count()

    # Mark all as read when admin opens page
    ContactMessage.objects.filter(is_read=False).update(is_read=True)

    context = {
        'all_messages': all_messages,
        'unread_count': unread_count,
    }

    return render(request, 'admin_messages.html', context)