from datetime import datetime, timedelta
from django.db.models import Manager
from .utils import Utils


# TODO: Implement all methods filter Room Booking here
class RoomBookingManager(Manager):

    def get_all_room_booking(self, room_id=0, incoming_booking=False):
        if incoming_booking:
            yesterday = datetime.now() - timedelta(days=1)
            yesterday_end_date = Utils.end_of_date(yesterday)
            return self.filter(room_id=room_id, booked_at__gt=yesterday_end_date)
        return self.all()

    def existed_room_booking(self, room_id, movie_id, booked_at):
        return self.filter(room_id=room_id, movie_id=movie_id, booked_at=booked_at).first()


class TicketManager(Manager):

    def get_all_tickets(self, room_booking_id=0):
        if room_booking_id:
            return self.filter(room_booking_id=room_booking_id)
        return self.all()

    def is_ticket_available(self, room_booking_id, seat_number, customer_id=0):
        filter_params = dict(
            room_booking_id=room_booking_id,
            seat_no=seat_number
        )
        exclude_params = {}
        if customer_id:
            exclude_params['customer_id'] = customer_id
        return not self.filter(**filter_params).exclude(**exclude_params).exists()