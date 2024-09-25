from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register('tickets',views.TicketViewSet,'tickets-viewset')
router.register('tickets/(?P<ticket_id>\d+)/messages',views.TicketMessageViewSet,'tickets-messages-viewset')
router.register('support-team',views.SupportTeamViewSet,'support-team-viewset')
router.register('support-team-member',views.SupportTeamMemberViewSet,'support-team-member-viewset')

urlpatterns = [

] + router.urls
