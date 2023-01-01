from base64 import urlsafe_b64encode
from django.shortcuts import render
from django.views.generic import View
from .models import Booking, User, Banner, Movie, ScreenMovie
from .serializers import BookingSerializer,RegisterSerializer, MovieSerializer, ScreenMovieSerializer
from rest_framework.permissions import AllowAny
from rest_framework import generics
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.permissions import AllowAny,IsAuthenticated
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.views.generic import View
from django.views.decorators.csrf import csrf_exempt
from .utils import get_data_for_booking, create_screens_slots,check_and_set_new_user_password
from .choices import LANGAUGE_CHOICES, GENDER_CHOICES, GENRE_CHOICES
from django.forms.models import model_to_dict
from core.settings import STRIPE_SECRET_KEY
import stripe
import datetime
import time
stripe.api_key = STRIPE_SECRET_KEY

class MoviesApi(viewsets.ModelViewSet):
    permission_classes = [AllowAny,]
    serializer_class = MovieSerializer

    def get_queryset(self):
        return Movie.objects.all()
    

    def create(self, request):
        ajax_data = request.data.dict()
        ajax_data.pop("csrfmiddlewaretoken")
        print(ajax_data)
        serializer = MovieSerializer(data={"poster": self.request.data.get("photograph", None),
                                           "title": self.request.data.get("title", None),
                                           "description": self.request.data.get("desc", None),
                                           "duration": self.request.data.get("time", None),
                                           "release_date": self.request.data.get("date", None),
                                           "language": self.request.data.get("langauge", None),
                                           "genre": self.request.data.get("genre", None)
                                           }
                                     )

        if not serializer.is_valid():
            print(serializer.errors)
            return Response({"msg": "error"})

        print(serializer.save())
        movie_id = (serializer.save()).id
        create_screens_slots(ajax_data, movie_id)
        return Response({"message": "success"})


class ChoicesApi(APIView):

    def get(self, request):
        return Response({"langauge": LANGAUGE_CHOICES, "genre": GENRE_CHOICES})


class ScreenMovieApi(viewsets.ModelViewSet):
    serializer_class = ScreenMovieSerializer
    queryset = ScreenMovie.objects.all()

    def get_queryset(self, *args, **kwargs):
        return self.queryset

    def list(self, *args, **kwargs):
        movie_id = self.request.query_params.get('id', None)
        return Response(get_data_for_booking(movie_id=movie_id))
        # show_times = self.queryset.filter(movie=movie_id).values_list("cinema__name")


class BookingApi(viewsets.ModelViewSet):
    
    permission_classes = [IsAuthenticated]
    
    serializer_class = BookingSerializer
    queryset = Booking.objects.all()

    def get_queryset(self, *args, **kwargs):
        return self.queryset

    def list(self, *args, **kwargs):
        screen_movie_id = self.request.query_params.get('id', None)
        response_data = ScreenMovie.objects.get(id=screen_movie_id)
        return Response({'availableSeats': int(response_data.total_seats_capacity)})

    def create(self, request):
        seat_count = int(request.data.get('seat_count'))
        screen_movie_id = int(request.data.get('screen_movie'))
        print(request.user)
        available_seats= ScreenMovie.objects.get(id=screen_movie_id).total_seats_capacity
        print(available_seats,'????')
        obj = ScreenMovie.objects.get(id=screen_movie_id)
        obj.total_seats_capacity = (obj.total_seats_capacity - seat_count)
        obj.save()
        total = (obj.seat_price*seat_count)
        if available_seats <= 0:
            return Response({"status":"ran out of seats"})
        
        serializer = BookingSerializer(data={"booked_seats":seat_count,"user":request.user.id,"show_movie":screen_movie_id,"total":total})
        
        if not serializer.is_valid():
            print(serializer.errors)
            return Response({"msg": "error"})
        booking_obj = serializer.save()
        creation_time_of_booking = booking_obj.created_at
        time_change = datetime.timedelta(minutes=1)
        new_time = creation_time_of_booking + time_change
        booking_obj.seat_block_duration = new_time
        booking_obj.save()
        print(booking_obj.total,'total')
        return Response({"status":"booked","details":[{"bookingId":booking_obj.id,"total":booking_obj.total,}]})

   
class ChatBotApi(APIView):
    
    def get(self,request):
        
        return Response({""})


    def post(self,request):
        time.sleep(2)
        print(request.POST)
        return Response({"message":"hello"})
    
    
class ResetPasswordApi(APIView):
    
    permission_classes = [IsAuthenticated]

    def get(self,request):
        print(request,'req')
        return Response({"message":"success"})
    
    def post(self,request):
        print(dict(request.data))
        return Response(check_and_set_new_user_password(request.user,(dict(request.data)).get("oldPassOfUser"),(dict(request.data)).get("NewPassOfUser"))
)
    
        
