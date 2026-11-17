from django.contrib import admin
from .models import Booking, Match, Profile, Team



class TeamAdmin(admin.ModelAdmin):
    list_display = ("name", "city", "coach", "points", "played")
admin.site.register(Team, TeamAdmin)



class MatchAdmin(admin.ModelAdmin):
    list_display = ("__str__", "date", "time", "venue")
admin.site.register(Match, MatchAdmin)



class BookingAdmin(admin.ModelAdmin):
    list_display = ("__str__", "tickets", "ticket_type", "total_price", "payment_method", "status")
    list_filter = ("status", "ticket_type", "payment_method")
    list_editable = ("status",)
admin.site.register(Booking, BookingAdmin)


admin.site.register(Profile)

