from django.shortcuts import get_object_or_404, render
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from datetime import date

from .forms import BookingForm, RegisterForm
from .models import Booking, Match, Team


def home(request):
    return render(request, "index.html")


def register(request):
    form = RegisterForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, "Account created. Welcome!")
        return redirect("home")
    return render(request, "register.html", {"form": form})


def matches(request):
    upcoming = Match.objects.filter(date__gte=date.today()).select_related("home_team", "away_team")
    return render(request, "viewmatches.html", {"matches": upcoming})


def fixtures(request):
    all_matches = Match.objects.select_related("home_team", "away_team")
    return render(request, "fixtures.html", {"matches": all_matches, "teams": Team.objects.all()})


def teams(request):
    return render(request, "teams.html", {"teams": Team.objects.order_by("name")})


@login_required
def book_tickets(request):
    initial = {}
    if request.GET.get("match"):
        initial["match"] = request.GET["match"]
    form = BookingForm(request.POST or None, initial=initial)
    if request.method == "POST" and form.is_valid():
        booking = form.save(commit=False)
        booking.user = request.user
        booking.save()
        messages.success(request, "Ticket booked!")
        return redirect("my_tickets")
    return render(request, "booktickets.html", {"form": form})


@login_required
def my_tickets(request):
    bookings = request.user.bookings.select_related("match__home_team", "match__away_team")
    return render(request, "ticket_view.html", {"bookings": bookings})


@login_required
def payment_history(request):
    bookings = request.user.bookings.select_related("match__home_team", "match__away_team")
    return render(request, "payment_history.html", {"bookings": bookings})

@login_required
def pay_booking(request, pk):
    # user=request.user -> a user can only pay for their own bookings
    booking = get_object_or_404(Booking, pk=pk, user=request.user)

    if booking.status == "Completed":
        messages.info(request, "This booking is already paid.")
        return redirect("payments")

    if request.method == "POST":
        booking.status = "Completed"
        booking.save()
        messages.success(request, "Payment completed. Your ticket is now active!")
        return redirect("payments")

    return render(request, "pay.html", {"booking": booking})
