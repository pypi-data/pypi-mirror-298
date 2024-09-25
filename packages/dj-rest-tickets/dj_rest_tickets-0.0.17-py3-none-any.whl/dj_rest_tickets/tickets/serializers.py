from rest_framework import serializers
from django.apps import apps
from django.conf import settings
from .models import (
    Ticket, 
    AbstractTicket , 
    SupportTeam , 
    SupportTeamMember,
    TicketMessage,
)
from django.utils.module_loading import import_string
from dj_rest_tickets.utils import get_settings



class BaseTicketSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Ticket
        fields = [
            'id',
            'content',
            'status',
            'creator',
            'observers',
            'support_team',
            'support_team_member',
            'created',
            'modified',
        ]

        extra_kwargs = {
            'creator': { 'read_only':True },
            'status': { 'read_only':True },
            'support_team_member': { 'read_only':True },
        }

    
    def update(self, instance: AbstractTicket, validated_data):
        if self.instance.status != Ticket.Status.PENDING:
            validated_data.pop('support_team',None)
        return super().update(instance, validated_data)
    
    def create(self, validated_data):
        validated_data['creator'] = self.context['request'].user
        return super().create(validated_data)
    
    
    def validate_observers(self, value):
        if self.context['request'].user in value:
            raise serializers.ValidationError('The creator of the ticket cannot be added as an observer')
        return value


TicketSerializer : type[BaseTicketSerializer] = import_string(get_settings().get('TicketSerializer','dj_rest_tickets.tickets.serializers.BaseTicketSerializer'))


class BaseChangeStatusTicketSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Ticket
        fields = [
            'id',
            'status',
        ]

ChangeStatusTicketSerializer : type[BaseChangeStatusTicketSerializer] = import_string(get_settings().get('ChangeStatusTicketSerializer','dj_rest_tickets.tickets.serializers.BaseChangeStatusTicketSerializer'))


class BaseAssignTeamTicketSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Ticket
        fields = [
            'id',
            'support_team',
        ]

AssignTeamTicketSerializer : type[BaseAssignTeamTicketSerializer] = import_string(get_settings().get('AssignTeamTicketSerializer','dj_rest_tickets.tickets.serializers.BaseAssignTeamTicketSerializer'))




class BaseAssignTeamMemberTicketSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Ticket
        fields = [
            'id',
            'support_team_member',
        ]
    
    def validate_support_team_member(self, value):
        if self.instance.support_team:
            if value and value.support_team != self.instance.support_team:
                raise serializers.ValidationError('Cannot assign ticket to member not exists in its support team.')
            self.instance.status = Ticket.Status.IN_PROGRESS
            return value
        
        raise serializers.ValidationError('Assign a support team firstly than assign a member.')

AssignTeamMemberTicketSerializer : type[BaseAssignTeamMemberTicketSerializer] = import_string(get_settings().get('AssignTeamMemberTicketSerializer','dj_rest_tickets.tickets.serializers.BaseAssignTeamMemberTicketSerializer'))



class BaseSupportTeamSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = SupportTeam
        fields = [
            'id',
            'name',
            'created',
            'modified',
        ]

SupportTeamSerializer : type[BaseSupportTeamSerializer] = import_string(get_settings().get('SupportTeamSerializer','dj_rest_tickets.tickets.serializers.BaseSupportTeamSerializer'))


class BaseSupportTeamMemberSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = SupportTeamMember
        fields = [
            'id',
            'user',
            'support_team',
            'is_admin',
            'created',
            'modified',
        ]

SupportTeamMemberSerializer : type[BaseSupportTeamMemberSerializer] = import_string(get_settings().get('SupportTeamMemberSerializer','dj_rest_tickets.tickets.serializers.BaseSupportTeamMemberSerializer'))


class BaseTicketMessageSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = TicketMessage
        fields = [
            'id',
            'content',
            'ticket',
            'user',
            'is_creator',
            'is_readed',
            'created',
            'modified',
        ]

        extra_kwargs = {
            'user': { 'read_only':True },
            'is_creator': { 'read_only':True },
        }

    def update(self, instance, validated_data):
        validated_data.pop('user',None)
        return super().update(instance, validated_data)
    
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

TicketMessageSerializer : type[BaseTicketMessageSerializer] = import_string(get_settings().get('TicketMessageSerializer','dj_rest_tickets.tickets.serializers.BaseTicketMessageSerializer'))

