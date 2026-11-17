from django.db import models
from django.conf import settings
from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    contact = models.CharField(max_length=30)
    location = models.CharField(max_length=100)

    def __str__(self):
        return self.user.username


class Team(models.Model):
    name = models.CharField(max_length=100, unique=True)
    city = models.CharField(max_length=100)
    coach = models.CharField(max_length=100)
    points = models.PositiveIntegerField(default=0)
    played = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["-points", "name"]

    def __str__(self):
        return self.name


class Match(models.Model):
    home_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="home_matches")
    away_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="away_matches")
    date = models.DateField()
    time = models.TimeField()
    venue = models.CharField(max_length=150, default="Namboole Stadium")

    class Meta:
        ordering = ["date", "time"]
        verbose_name_plural = "matches"

    def __str__(self):
        return f"{self.home_team} vs {self.away_team}"


class Booking(models.Model):
    SEAT_CHOICES = [("front_row", "Front Row"), ("middle_row", "Middle Row"), ("back_row", "Back Row")]
    TYPE_CHOICES = [("regular", "Regular"), ("VIP", "VIP"), ("premium", "Premium")]
    PAYMENT_CHOICES = [("credit_card", "Credit Card"), ("mobile_money", "Mobile Money"), ("paypal", "PayPal")]
    STATUS_CHOICES = [("Pending", "Pending"), ("Completed", "Completed")]
    PRICES = {"regular": 10000, "VIP": 25000, "premium": 50000}
    SEAT_PREFIX = {"front_row": "A", "middle_row": "M", "back_row": "Z"}

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="bookings")
    match = models.ForeignKey(Match, on_delete=models.CASCADE, related_name="bookings")
    tickets = models.PositiveIntegerField()
    seat = models.CharField(max_length=20, choices=SEAT_CHOICES)
    ticket_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_CHOICES)
    total_price = models.PositiveIntegerField(editable=False)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Pending")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def save(self, *args, **kwargs):
        self.total_price = self.tickets * self.PRICES[self.ticket_type]
        super().save(*args, **kwargs)

    def ticket_id(self):
        return f"{self.pk:03d}"

    def seat_number(self):
        prefix = self.SEAT_PREFIX[self.seat]
        return ", ".join(f"{prefix}{self.pk * 10 + i}" for i in range(1, self.tickets + 1))

    def __str__(self):
        return f"#{self.ticket_id()} {self.user} - {self.match}"

