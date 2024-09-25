from django.contrib import admin
from .models import Ticket, SupportTeamMember, SupportTeam

# Register your models here.

admin.site.register(Ticket)
admin.site.register(SupportTeamMember)
admin.site.register(SupportTeam)