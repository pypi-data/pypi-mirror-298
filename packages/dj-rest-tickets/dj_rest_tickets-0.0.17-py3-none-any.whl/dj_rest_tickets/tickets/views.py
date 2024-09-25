from django.shortcuts import render, get_object_or_404
from django.db.models import Q, Min, Max

from rest_framework import (
    viewsets, 
    permissions, 
    decorators,
    request,
    response,
    serializers,
    exceptions
)
from django_filters.rest_framework import DjangoFilterBackend

from .serializers import (
    TicketSerializer,
    SupportTeamMemberSerializer,
    SupportTeamSerializer,
    AssignTeamTicketSerializer,
    AssignTeamMemberTicketSerializer,
    ChangeStatusTicketSerializer,
    TicketMessageSerializer,
)
from .models import (
    Ticket,
    SupportTeam,
    SupportTeamMember,
    TicketMessage
)
from .permissions import (
    IsSupportAdmin, 
    IsSupportTeamMember,
    CanAccessToTicketMessages,
    CanChatTicketMessages,
)
from dj_rest_tickets.utils import CustomPageNumberPagination


class TicketViewSet(viewsets.ModelViewSet):

    permission_classes=[permissions.IsAuthenticated,IsSupportTeamMember]
    pagination_class=CustomPageNumberPagination

    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer

    def get_queryset(self):
        if self.request.user.support_team_member.is_admin:
            return super().get_queryset().filter(
                Q( support_team_member = self.request.user.support_team_member) |
                Q( support_team=self.request.user.support_team_member.support_team ) |
                Q( support_team=None )
            )
        
        return super().get_queryset().filter(support_team_member = self.request.user.support_team_member)
    
    @decorators.action(
        detail=True,
        methods=['POST'],
        permission_classes=[permissions.IsAuthenticated, IsSupportAdmin],
        serializer_class=AssignTeamTicketSerializer,
    )
    def admin_change_support_team(self,request,pk):
        return self.update(request,pk)
    
    @decorators.action(
        detail=True,
        methods=['POST'],
        permission_classes=[permissions.IsAuthenticated, IsSupportAdmin],
        serializer_class=AssignTeamMemberTicketSerializer
    )
    def admin_change_support_team_member(self,request,pk):
        return self.update(request,pk)
    
    @decorators.action(
        detail=True,
        methods=['POST'],
        permission_classes=[permissions.IsAuthenticated, IsSupportAdmin],
        serializer_class=ChangeStatusTicketSerializer
    )
    def admin_change_status(self,request,pk):
        return self.update(request,pk)


class SupportTeamMemberViewSet(viewsets.ModelViewSet):

    permission_classes=[permissions.IsAuthenticated, IsSupportAdmin]

    queryset = SupportTeamMember.objects.all()
    serializer_class = SupportTeamMemberSerializer
    pagination_class=CustomPageNumberPagination


class SupportTeamViewSet(viewsets.ModelViewSet):

    permission_classes=[permissions.IsAuthenticated, IsSupportAdmin]

    queryset = SupportTeam.objects.all()
    serializer_class = SupportTeamSerializer
    pagination_class=CustomPageNumberPagination


class TicketMessageViewSet(viewsets.ModelViewSet):
    permission_classes=[permissions.IsAuthenticated,CanAccessToTicketMessages,CanChatTicketMessages]

    queryset = TicketMessage.objects.all()
    serializer_class = TicketMessageSerializer
    pagination_class=CustomPageNumberPagination

    def initialize_request(self, request, *args, **kwargs):
        self.ticket = get_object_or_404(Ticket,pk=self.kwargs['ticket_id'])
        return super().initialize_request(request, *args, **kwargs)

    def get_queryset(self):
        return super().get_queryset().filter(ticket=self.ticket)

    @decorators.action(
        detail=True,
        methods=['GET'],
    )
    def mark_as_readed(self,request,ticket_id,pk):
        instance = self.get_object()
        # make all before messages as readed
        if request.user == self.ticket.creator:
            self.get_queryset().exclude(
                user=self.ticket.creator,created__lte=instance.created
            ).update(is_readed=True)
        else:
            self.get_queryset().filter(
                user=self.ticket.creator,created__lte=instance.created
            ).update(is_readed=True)

        return self.retrieve(request,pk)
    
    @decorators.action(
        detail=False,
        methods=['GET'],
    )
    def is_there_unreads(self,request,ticket_id):
        is_there_unreads = False
        if request.user == self.ticket.creator:
            is_there_unreads = self.get_queryset().exclude(
                user=self.ticket.creator
            ).exists()
        else:
            is_there_unreads = self.get_queryset().filter(
                user=self.ticket.creator
            ).exists()
        return response.Response({'is_there_unreads':is_there_unreads})
    