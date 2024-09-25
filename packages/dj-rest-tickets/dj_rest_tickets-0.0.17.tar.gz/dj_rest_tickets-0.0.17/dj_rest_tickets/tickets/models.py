from typing import Iterable
from django.db import models
from django.contrib.auth import get_user_model
from django.apps import apps
from django.conf import settings
from django.core.exceptions import ValidationError
from dj_rest_tickets.utils import get_settings



User = get_user_model()


class AbstractSupportTeam(models.Model):
    name = models.CharField(max_length=256)

    created = models.DateTimeField(auto_now_add=True,editable=False)
    modified = models.DateTimeField(auto_now=True,editable=False)

    class Meta:
        abstract = True
        ordering = ['created']


class DefaultSupportTeam(AbstractSupportTeam):
    pass

SupportTeam : type[AbstractSupportTeam] = apps.get_model(get_settings().get('SupportTeam','tickets.DefaultSupportTeam'),require_ready=False)


class AbstractSupportTeamMember(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='support_team_member')
    support_team = models.ForeignKey(SupportTeam, on_delete=models.PROTECT, related_name='support_team_members')
    is_admin = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

    created = models.DateTimeField(auto_now_add=True,editable=False)
    modified = models.DateTimeField(auto_now=True,editable=False)

    class Meta:
        abstract = True
        ordering = ['created']


class DefaultSupportTeamMember(AbstractSupportTeamMember):
    pass

SupportTeamMember : type[AbstractSupportTeamMember] = apps.get_model(get_settings().get('SupportTeamMember','tickets.DefaultSupportTeamMember'),require_ready=False)

class AbstractTicket(models.Model):

    class Status(models.TextChoices):
        PENDING = 'pending', 'Pending'
        IN_PROGRESS = 'in_progress', 'In Progress'
        RESOLVED = 'resolved', 'Resolved'
        REJECTED = 'rejected', 'Rejected'

    content = models.CharField(max_length=320)
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
    )
    
    observers = models.ManyToManyField(User,blank=True)

    creator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='user_creator_tickets')
    support_team = models.ForeignKey(SupportTeam, on_delete=models.SET_NULL, null=True, related_name='support_team_tickets')
    support_team_member = models.ForeignKey(SupportTeamMember, on_delete=models.SET_NULL, null=True, related_name='support_team_member_tickets')

    is_resolved = models.BooleanField(default=False,blank=True)

    def __str__(self):
        return f"{self.content} ({self.get_status_display()})"
    
    created = models.DateTimeField(auto_now_add=True,editable=False)
    modified = models.DateTimeField(auto_now=True,editable=False)

    class Meta:
        abstract = True
        ordering = ['created']
        
    

class DefaultTicket(AbstractTicket):
    pass


Ticket : type[AbstractTicket] = apps.get_model(get_settings().get('Ticket','tickets.DefaultTicket'),require_ready=False)



class AbstractTicketMessage(models.Model):
    content = models.CharField(max_length=256)

    ticket = models.ForeignKey(Ticket,on_delete=models.CASCADE,related_name='ticket_messages')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='user_ticket_messages')

    is_creator = models.BooleanField(default=False,blank=True)
    is_readed = models.BooleanField(default=False,blank=True)

    created = models.DateTimeField(auto_now_add=True,editable=False)
    modified = models.DateTimeField(auto_now=True,editable=False)

    class Meta:
        abstract = True
        ordering = ['-created']
    
    def save(self,*args,**kwargs) -> None:
        self.is_creator = self.user == self.ticket.creator
        return super().save(*args,**kwargs)


class DefaultTicketMessage(AbstractTicketMessage):
    pass

TicketMessage : type[AbstractTicketMessage] = apps.get_model(get_settings().get('TicketMessage','tickets.DefaultTicketMessage'),require_ready=False)





