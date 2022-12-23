from .models import *
from datetime import datetime,timedelta
import math
from datetime import time
from django.db.models import Q
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.sessions.backends.db import SessionStore

def get_data_for_booking(movie_id):

    queryset = ScreenMovie.objects.all()
    new_try = list(queryset.filter(movie=movie_id).values_list("cinema__id","cinema__name").distinct())
    final_list = []
    for screenss in new_try:
        data = list(ScreenMovie.objects.filter(Q(cinema=screenss[0]),Q(movie=movie_id)).values("id","start_duration","end_duration","date"))
        final_list.append({"cinema":screenss[1],"slots":data})
    return final_list


def create_screens_slots(data,movieid):

    print(data, 'data')
    cinema_id = data.pop("cinema")
    price = data.pop("price")
    screen_id = data.pop("screen")
    slot_start_at = data.pop("startTime")
    slot_ends_at = data.pop("endTime")
    duration = data.pop("time")
    date = data.pop("date")
    print(date,'date')
    show_date = datetime.strptime(slot_start_at, '%H:%M')
    screening_start_time = datetime.strptime(slot_start_at, '%H:%M')
    screening_end_time = datetime.strptime(slot_ends_at, '%H:%M')
    print(screening_start_time,screening_end_time)
    duration_of_movie = datetime.strptime(duration, '%H:%M')
    duration_hour = datetime.strptime(duration, '%H:%M').hour
    print('hour d ', duration_hour)
    mv_length = (duration_hour*60)
    print('mvoi in mins',mv_length)
    time_qouta = screening_end_time - screening_start_time
    print(time_qouta, 'timeqouta in hours')
    new_tri = time_qouta.seconds // 60
    print(new_tri, 'timeqouta in mins')
    slots_capacity_for_screen = int(time_qouta/timedelta(hours=duration_of_movie.hour,minutes=duration_of_movie.minute))
    print(slots_capacity_for_screen)
    break_time_between_shows = (slots_capacity_for_screen//new_tri)
    print('calc',(new_tri-(slots_capacity_for_screen*mv_length)))
    time_to_add = (new_tri//slots_capacity_for_screen)
    date_new = datetime.fromisoformat(date)
    for i in range(slots_capacity_for_screen):
        result_1 = screening_start_time + timedelta(hours=duration_of_movie.hour,minutes=duration_of_movie.minute)
        print('slots ---->',screening_start_time,result_1)

    
        d_1 = time(screening_start_time.hour,screening_start_time.minute,screening_start_time.second)
        d_2 = time(result_1.hour,result_1.minute,result_1.second)
        screen_movie = ScreenMovie(cinema=Cinema.objects.get(id=int(cinema_id)),screen=Screens.objects.get(id=int(screen_id)),movie=Movie.objects.get(id=movieid),
                               start_duration=d_1,end_duration=d_2,date=date_new,seat_price=float(price))
        print(screen_movie)
        screen_movie.save()
        screening_start_time=result_1


def add_screen_seat_capacity(instance):
    instance.total_seats_capacity = int(instance.screen.total_seats)
    instance.save()
    
    
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }
    