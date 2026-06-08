from django.urls import path
from . import views

urlpatterns = [

    # ── PUBLIC URLS ───────────────────────────────────
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),

    # ── AUTH URLS ─────────────────────────────────────
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # ── USER URLS ─────────────────────────────────────
    path('book/', views.book, name='book'),
    path('my-bookings/', views.my_bookings, name='my_bookings'),
    path('cancel-booking/<int:booking_id>/', views.cancel_booking, name='cancel_booking'),

    # ── ADMIN URLS ────────────────────────────────────
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('update-status/<int:booking_id>/', views.update_status, name='update_status'),
    path('admin-messages/', views.admin_messages, name='admin_messages'),

]