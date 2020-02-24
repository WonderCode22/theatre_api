from rest_framework import serializers
from .models import Movie, Room, Ticket, Customer, RoomBooking


class CustomerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Customer
        exclude = ['created_at', 'updated_at']

    def create(self, validated_data):
        return Customer.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.save()
        return instance


class MovieSerializer(serializers.ModelSerializer):

    class Meta:
        model = Movie
        exclude = ['created_at', 'updated_at']

    def create(self, validated_data):
        return Movie.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.start_at = validated_data.get('title', instance.start_at)
        instance.screen_time = validated_data.get('title', instance.screen_time)
        instance.save()
        return instance


class RoomSerializer(serializers.ModelSerializer):

    class Meta:
        model = Room
        fields = ['id', 'name', 'capacity']


    def create(self, validated_data):
        return Room.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.capacity = validated_data.get('capacity', instance.capacity)
        instance.save()
        return instance


class RoomBookingListSerializer(serializers.ModelSerializer):
    movie_title = serializers.ReadOnlyField(source='movie.title')
    start_at = serializers.ReadOnlyField(source='movie.start_at')
    room_name = serializers.ReadOnlyField(source='room.name')

    class Meta:
        model = RoomBooking
        fields = ['id', 'movie_title', 'start_at', 'room_name', 'booked_at']


class RoomBookingSerializer(serializers.ModelSerializer):
    room_id = serializers.IntegerField(required=True)
    movie_id = serializers.IntegerField(required=True)

    class Meta:
        model = RoomBooking
        fields = ['id', 'movie_id', 'room_id', 'booked_at']

    def create(self, validated_data):
        return RoomBooking.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.movie_id = validated_data.get('movie_id', instance.movie_id)
        instance.room_id = validated_data.get('room_id', instance.room_id)
        instance.booked_at = validated_data.get('booked_at', instance.booked_at)
        instance.save()
        return instance

    def validate(self, data):
        room_id = data.get('room_id', 0)
        movie_id = data.get('movie_id', 0)

        room = Room.objects.get(pk=room_id)
        if not room:
            raise Exception("Room is invalid!")

        movie = Movie.objects.get(pk=movie_id)
        if not movie:
            raise Exception("Movie is invalid!")

        if not self.instance:
            existed_booking = RoomBooking.objects.existed_room_booking(room_id, movie_id, data['booked_at'])
            if existed_booking:
                self.instance = existed_booking
        return data


class TicketSerializer(serializers.ModelSerializer):
    customer_id = serializers.IntegerField(required=True)
    room_booking_id = serializers.IntegerField(required=True)

    class Meta:
        model = Ticket
        fields = ['id', 'ticket_no', 'seat_no', 'customer_id', 'room_booking_id']

    def create(self, validated_data):
        return Ticket.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.ticket_no = validated_data.get('ticket_no', instance.ticket_no)
        instance.seat_no = validated_data.get('seat_no', instance.seat_no)
        instance.customer_id = validated_data.get('customer_id', instance.customer_id)
        instance.room_booking_id = validated_data.get('room_booking_id', instance.room_booking_id)
        instance.save()
        return instance

    def validate(self, data):
        room_booking_id = data.get('room_booking_id')
        invalid_booking = False
        room_booking = RoomBooking.objects.get(pk=room_booking_id)

        if not room_booking:
            invalid_booking = True
        if not invalid_booking:
            room = Room.objects.get(pk=room_booking.room_id)
            if not room:
                invalid_booking = True
        if invalid_booking:
            raise Exception("The movie plan is cancelled!")

        seat_number = data.get('seat_no')
        customer_id = self.instance.id if self.instance else 0
        if not Ticket.objects.is_ticket_available(room_booking_id, seat_number, customer_id=customer_id):
            raise Exception("The seat number is already booked!")
        return data