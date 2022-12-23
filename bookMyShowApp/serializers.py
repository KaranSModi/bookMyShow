from rest_framework import serializers
from .models import User,Movie,ScreenMovie,Screens,Cinema,City,Booking
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate,login

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password', 'email')

    # def validate(self, attrs):
    #     if attrs['password'] != attrs['password2']:
    #         raise serializers.ValidationError({"password": "Password fields didn't match."})
    #     return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )

        user.is_active = True
        user.set_password(validated_data['password'])
        user.save()
        return user
   

class CitySerializer(serializers.ModelSerializer):
    
    class Meta:
        
        model = City
        fields = '__all__'
    
class MovieSerializer(serializers.ModelSerializer):
    
     class Meta:
        model = Movie
        fields = (
        "id",
        "title" ,
        "poster",
        "description" ,
        "duration" ,
        "language" ,
        "release_date" ,
        "genre"
        )
        


class CinemaSerializer(serializers.ModelSerializer):
    
    # city = CitySerializer()
    city_name = serializers.CharField(source='city.name')
    
    class Meta:
        model = Cinema
        fields = ("city_name","name","total_cinema_halls")


class ScreenSerializer(serializers.ModelSerializer):
    
    cinema = CinemaSerializer()
    
    class Meta:
        model = Screens
        fields = '__all__'



class ScreenMovieSerializer(serializers.ModelSerializer):
    movie = MovieSerializer()
    screen = ScreenSerializer()
    cinema = CinemaSerializer()
    class Meta:
        model = ScreenMovie
        fields = ("movie","start_duration","screen","cinema")
        
        
class BookingSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Booking
        fields = '__all__'
        
        
    def update(self, instance, validated_data):
        demo = Booking.objects.get(pk=instance.id)
        occupied_seats = demo.booked_seats
        demo.booked_seats = 0
        demo.show_movie.total_seats_capacity +=  occupied_seats
        demo.show_movie.save()
        demo.save()
        return demo