from django.db import models
from django.contrib.auth.models import User,AbstractUser
from .choices import GENDER_CHOICES,LANGAUGE_CHOICES,GENRE_CHOICES
from django.db.models.signals import post_save
from django.dispatch import receiver
class User(AbstractUser):
    email = models.EmailField(unique=True)
    birth_date = models.DateField(null=True)
    gender = models.CharField(max_length=6,choices=GENDER_CHOICES,null=True,blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.username
    
class Banner(models.Model):
    banner_image = models.ImageField(upload_to='banners/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
class Movie(models.Model):
    title = models.CharField(max_length=255)
    poster = models.ImageField(upload_to='movies/posters')
    description = models.CharField(max_length=512)
    duration = models.TimeField()
    language = models.CharField(choices=LANGAUGE_CHOICES,max_length=255) 
    release_date = models.DateField()
    genre = models.CharField(choices=GENRE_CHOICES,max_length=255)
    
    def __str__(self):
        return self.title
    
class City(models.Model):
    name = models.CharField(max_length=255)
    zipcode = models.CharField(max_length=255,blank=True)
    
    def __str__(self):
        return self.name
    
class Cinema(models.Model):
    city = models.ForeignKey(City,on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    total_cinema_halls = models.PositiveIntegerField()
    
    def __str__(self):
        return self.name

class Screens(models.Model):
    cinema = models.ForeignKey(Cinema,on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    total_seats = models.PositiveIntegerField()
    
    def __str__(self):
        return self.name
    
class ScreenMovie(models.Model):
    cinema = models.ForeignKey(Cinema,on_delete=models.CASCADE)
    screen = models.ForeignKey(Screens,on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie,on_delete=models.CASCADE)
    start_duration = models.TimeField()
    end_duration = models.TimeField()
    date = models.DateField()
    total_seats_capacity = models.IntegerField(null=True,blank=True)
    seat_price = models.FloatField(null=True,blank=True) 
    
    def save(self, *args, **kwargs):
        if self.id == None:
            self.total_seats_capacity = self.screen.total_seats
            super(ScreenMovie, self).save(*args, **kwargs)
        super(ScreenMovie, self).save(*args, **kwargs)
    
        
    def __str__(self):
        return f"{self.cinema} - {self.screen} - {self.total_seats_capacity}"
    
    

    
class Booking(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    show_movie = models.ForeignKey(ScreenMovie,on_delete=models.CASCADE)
    payment_status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    total = models.FloatField(null=True,blank=True)
    booked_seats = models.IntegerField()
    seat_block_duration = models.DateTimeField(blank=True,null=True) 
    # def save(self, *args, **kwargs):
    #     self.show_movie.total_seats_capacity = self.show_movie.total_seats_capacity - self.booked_seats
    #     self.total = ((self.show_movie.seat_price)*(self.booked_seats))
    #     if self.show_movie.total_seats_capacity <= 0:
    #         self.show_movie.total_seats_capacity = 0
    #         self.show_movie.save()
    #     self.show_movie.save()
    #     if (self.booked_seats == 0):
    #         self.save()            
    #     super(Booking, self).save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.user} - {self.show_movie.movie.title} - {self.total}"
    
    
class ErrorLog(models.Model):
    error_data = models.JSONField(default={})