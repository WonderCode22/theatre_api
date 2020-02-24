from rest_framework import routers
from .views import MovieViewSet, RoomViewSet, RoomBookingViewSet, TicketViewSet

router = routers.SimpleRouter(trailing_slash=False)
router.register('movie', MovieViewSet, basename="movie")
router.register('room', RoomViewSet, basename="room")
router.register('room_booking', RoomBookingViewSet, basename="room_booking")
router.register(r'ticket', TicketViewSet, basename="ticket")