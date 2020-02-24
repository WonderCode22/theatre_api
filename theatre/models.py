from django.db import models
from django.utils import timezone
from .managers import RoomBookingManager, TicketManager

# Create your models here.

class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    class Meta:
        abstract = True


class Customer(TimeStampedModel):
    name = models.CharField(max_length=255, default='')
    # More fields here, just keep simple for now

    class Meta:
        db_table = 'customers'

    def __str__(self):
        return self.name


class Movie(TimeStampedModel):
    title = models.CharField(max_length=255)
    screen_time = models.PositiveIntegerField(default=0)
    start_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'movies'

    def __str__(self):
        return self.title


class Room(models.Model):
    name = models.CharField(max_length=50, unique=True)
    capacity = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = 'rooms'

    def __str__(self):
        return self.name


class RoomBooking(TimeStampedModel):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, db_index=True)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, db_index=True)
    booked_at = models.DateTimeField(default=timezone.now, null=False)

    objects = RoomBookingManager()

    class Meta:
        db_table = 'room_booking'
        unique_together = ['room_id', 'movie_id', 'booked_at']


class Ticket(TimeStampedModel):
    ticket_no = models.CharField(max_length=50, unique=True)
    seat_no = models.CharField(max_length=50)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    room_booking = models.ForeignKey(RoomBooking, on_delete=models.CASCADE)

    objects = TicketManager()

    class Meta:
        db_table = 'tickets'
        unique_together = ['seat_no', 'room_booking_id']

    def __str__(self):
        return self.ticket_no