from rest_framework import status
from rest_framework.response import Response
from .mixins import GenericViewMixin
from .serializers import MovieSerializer, RoomSerializer, RoomBookingSerializer, RoomBookingListSerializer, \
    TicketSerializer
from .models import Movie, Room, RoomBooking, Ticket


class MovieViewSet(GenericViewMixin):
    permission_classes = ()
    view_set = "movie"
    serializer_class = MovieSerializer

    def list(self, request, *args, **kwargs):
        movies = Movie.objects.all()
        data = {
            'movies': self.get_serializer(movies, many=True).data
        }
        return Response(data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk, *args, **kwargs):
        try:
            movie = Movie.objects.get(pk=pk)
            if movie:
                serializer = self.get_serializer(movie)
                data = serializer.data
                return Response(data, status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        except Exception as ex:
            # todo: handle log
            return Response({'error': str(ex)}, status=status.HTTP_400_BAD_REQUEST)

    def create(self, request, *args, **kwargs):
        try:
            data = request.data.copy()
            serializer = self.get_serializer(data=data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as ex:
            # todo: handle log
            return Response({'error': str(ex)}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk, *args, **kwargs):
        try:
            data = request.data.copy()
            movie = Movie.objects.get(pk=pk)
            serializer = self.get_serializer(movie, data=data, partial=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as ex:
            # todo: handle log
            return Response({'error': str(ex)}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None, *args, **kwargs):
        try:
            movie = Movie.objects.get(pk=pk)
            if movie:
                Movie.objects.delete(movie)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as ex:
            # todo: handle log
            return Response({'error': str(ex)}, status=status.HTTP_400_BAD_REQUEST)


class RoomViewSet(GenericViewMixin):
    permission_classes = ()
    view_set = "room"
    serializer_class = RoomSerializer

    def list(self, request, *args, **kwargs):
        rooms = Room.objects.all()
        data = {
            'rooms': self.get_serializer(rooms, many=True).data
        }
        return Response(data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        try:
            data = request.data.copy()
            serializer = self.get_serializer(data=data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as ex:
            # todo: handle log
            return Response({'error': str(ex)}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk, *args, **kwargs):
        try:
            room = Room.objects.get(pk=pk)
            if room:
                serializer = self.get_serializer(room)
                data = serializer.data
                return Response(data, status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        except Exception as ex:
            # todo: handle log
            return Response({'error': str(ex)}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk, *args, **kwargs):
        try:
            data = request.data.copy()
            room = Room.objects.get(pk=pk)
            serializer = self.get_serializer(room, data=data, partial=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as ex:
            # todo: handle log
            return Response({'error': str(ex)}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None, *args, **kwargs):
        try:
            room = Room.objects.get(pk=pk)
            if room:
                room_in_used = RoomBooking.objects.get_all_room_booking(room_id=room.id, incoming_booking=True)
                if room_in_used:
                    return Response({'error': 'Room is already in used'}, status=status.HTTP_400_BAD_REQUEST)
                room.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as ex:
            # todo: handle log
            return Response({'error': str(ex)}, status=status.HTTP_400_BAD_REQUEST)


class RoomBookingViewSet(GenericViewMixin):
    permission_classes = ()
    view_set = "room_booking"
    
    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            return RoomBookingListSerializer
        return RoomBookingSerializer
    
    def list(self, request, *args, **kwargs):
        room_booking = RoomBooking.objects.all()
        data = {
            'room_booking': self.get_serializer(room_booking, many=True).data
        }
        return Response(data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        try:
            data = request.data.copy()
            serializer = self.get_serializer(data=data)
            print(data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as ex:
            # todo: handle log
            return Response({'error': str(ex)}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk, *args, **kwargs):
        try:
            room_booking = RoomBooking.objects.get(pk=pk)
            if room_booking:
                serializer = self.get_serializer(room_booking)
                data = serializer.data
                return Response(data, status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        except Exception as ex:
            # todo: handle log
            return Response({'error': str(ex)}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk, *args, **kwargs):
        try:
            data = request.data.copy()
            room_booking = RoomBooking.objects.get(pk=pk)
            serializer = self.get_serializer(room_booking, data=data, partial=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as ex:
            # todo: handle log
            return Response({'error': str(ex)}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None, *args, **kwargs):
        try:
            room_booking = RoomBooking.objects.get(pk=pk)
            if room_booking:
                room_booking.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as ex:
            # todo: handle log
            return Response({'error': str(ex)}, status=status.HTTP_400_BAD_REQUEST)
        
        
class TicketViewSet(GenericViewMixin):
    permission_classes = ()
    view_set = "ticket"
    serializer_class = TicketSerializer

    def list(self, request, *args, **kwargs):
        room_booking_id = request.GET.get('room_booking_id', 0)
        tickets = Ticket.objects.get_all_tickets(room_booking_id)
        data = {
            'tickets': self.get_serializer(tickets, many=True).data
        }
        return Response(data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk, *args, **kwargs):
        try:
            tiket = Ticket.objects.get(pk=pk)
            if tiket:
                serializer = self.get_serializer(tiket)
                data = serializer.data
                return Response(data, status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        except Exception as ex:
            # todo: handle log
            return Response({'error': str(ex)}, status=status.HTTP_400_BAD_REQUEST)

    def create(self, request, *args, **kwargs):
        try:
            data = request.data.copy()
            serializer = self.get_serializer(data=data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as ex:
            # todo: handle log
            return Response({'error': str(ex)}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk, *args, **kwargs):
        try:
            data = request.data.copy()
            tiket = Ticket.objects.get(pk=pk)
            serializer = self.get_serializer(tiket, data=data, partial=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as ex:
            # todo: handle log
            return Response({'error': str(ex)}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None, *args, **kwargs):
        try:
            ticket = Ticket.objects.get(pk=pk)
            if ticket:
                ticket.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as ex:
            # todo: handle log
            return Response({'error': str(ex)}, status=status.HTTP_400_BAD_REQUEST)