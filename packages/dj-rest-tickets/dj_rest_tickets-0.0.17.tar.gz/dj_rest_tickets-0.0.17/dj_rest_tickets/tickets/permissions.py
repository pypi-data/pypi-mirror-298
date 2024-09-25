from rest_framework import permissions

class IsSupportAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return hasattr(request.user,'support_team_member') and request.user.support_team_member.is_admin

class IsSupportTeamMember(permissions.BasePermission):
    def has_permission(self, request, view):
        return hasattr(request.user,'support_team_member')

class CanAccessToTicketMessages(permissions.BasePermission):
    # allow creator and assigned support team member and observers
    def has_permission(self, request, view):
        if request.user == view.ticket.creator:
            return True
        elif hasattr(request.user,'support_team_member'):
            return request.user.support_team_member == view.ticket.support_team_member or view.ticket.observers.contains(request.user)
        return False

class CanChatTicketMessages(permissions.BasePermission):
    # allow creator and assigned support team member just in unsafe methods and actions else alwas true
    def has_permission(self, request, view):
        
        if request.method in permissions.SAFE_METHODS:
            if view.action in ['is_there_unreads','mark_as_readed']:
                if request.user == view.ticket.creator:
                    return True
                elif hasattr(request.user,'support_team_member'):
                    return request.user.support_team_member == view.ticket.support_team_member
            return True
        
        if request.user == view.ticket.creator:
            return True
        elif hasattr(request.user,'support_team_member'):
            return request.user.support_team_member == view.ticket.support_team_member
        return False
