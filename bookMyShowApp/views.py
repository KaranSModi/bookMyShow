from django.shortcuts import render,HttpResponse
from django.http import JsonResponse
from django.views.generic import View
from .models import User,Banner,Cinema,Screens,Booking,ScreenMovie
from .serializers import RegisterSerializer
from rest_framework.permissions import AllowAny
from rest_framework import generics
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import permissions
from django.contrib.auth import authenticate,login,logout
from rest_framework.views import APIView
from django.views.generic import View
from django.views.decorators.csrf import csrf_exempt
from .utils import get_tokens_for_user
import stripe
import datetime



YOUR_DOMAIN = 'http://127.0.0.1:8000'

class RegisterPage(View):
    
    def get(self,request):
        return render(request,'UserRegister.html')


class LoginPage(View):
    
    def get(self,request):
        
        return render(request,'UserLogin.html')
    
class HomePage(View):

    def get(self,request):
        banners = Banner.objects.all()
        return render(request,'Home.html',{"banners":banners})
    
class MovieDetailPage(View):

    def get(self,request):
        return render(request,'MovieDetailPage.html')
    
class TheaterSelectionPage(View):

    def get(self,request):
        return render(request,'TheaterSelectionPage.html')


class UserRegisterViewSet(APIView):

    permission_classes = (permissions.AllowAny,)
    
    def post(self, request):
        if User.objects.filter(email=request.data.dict().get("Email")):
            return Response({"status":"Signin"})
        serializer = RegisterSerializer(data={"username":request.data.dict().get("Email").split("@")[0],
                                              "password":request.data.dict().get("Password"),
                                              "email":request.data.dict().get("Email"),
                                              })
        if serializer.is_valid():
            serializer.save()
            return Response({'status': 'success'})
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(APIView):

    permission_classes = (permissions.AllowAny,)
    def post(self,request):
        username = self.request.data.dict().get("Email").split("@")[0]
        password = self.request.data.dict().get("Password")
        check_existing_user = User.objects.get(username=username,email=self.request.data.dict().get("Email"))
        if check_existing_user:    
            authenticate(request)
            print(check_existing_user,'???????') 
            login(request, check_existing_user)
        return Response({'status':'success','message': get_tokens_for_user(check_existing_user)})
                       
                        

class UserLogoutView(APIView):
    def post(self,request):
        logout(request.user)
        return Response({"status":"succesfully logged out"})


    
class AddMoviePage(View):
    
    def get(self,request):
        cinema = Cinema.objects.all()
        screen = Screens.objects.all()
        return render(request,"AddMoviePage.html",{"cinema":cinema,"screen":screen})
    
    
class BookingPage(View):
    
    def get(self,request):
        screen_id = self.request.GET.get('id')
        print(screen_id)
        screen_data = ScreenMovie.objects.get(id=int(screen_id))
        print(screen_data)
        return render(request,"SeatSelectionPage.html")
    
    
class SeatSelectionPage(View):
    def get(self,request):
        return render(request,'SeatSelectionPage.html')
    
class UserBookingView(View):
    def get(self,request):
        try:
            bookings = Booking.objects.filter(user=request.user,payment_status=True)
            print(bookings,request.user)
        except:
            return HttpResponse("<h3>Please Login</h3>")
        return render(request,'UserBookings.html',{"bookings":bookings})
        

def home(request):
    return render(request,'checkout.html')

def success(request):
    paid_booking = Booking.objects.get(id=request.session['bookingId'])
    paid_booking.payment_status = True
    paid_booking.save()
    del request.session['bookingId']
    return render(request,'success.html')

def cancel(request):
    delete_booking = Booking.objects.get(id=request.session['bookingId'])
    delete_booking.delete()
    del request.session['bookingId']
    return render(request,'cancel.html')


def contact_us(request):
    return render(request,'ContactUsPage.html')

@csrf_exempt
def create_checkout_session(request):
    booking_id = request.GET.get('id')
    request.session['bookingId'] = booking_id
    user_booking = Booking.objects.get(id=booking_id)
    endpoint = stripe.WebhookEndpoint.create(
    url='https://b5d9-103-24-180-44.in.ngrok.io/webhooks/stripe/',
    enabled_events=[
    'charge.failed',
    'charge.succeeded',
    ],)
    session = stripe.checkout.Session.create(
    payment_method_types=['card'],
    line_items=[{
    'price_data': {
    'currency': 'inr',
    'product_data': {
    'name': str(user_booking.show_movie.movie.title),
    },
    'unit_amount': int((user_booking.show_movie.seat_price)*100),
    },
    
    'quantity': int(user_booking.booked_seats),
    }],
    mode='payment',
    success_url=YOUR_DOMAIN + '/success.html',
    cancel_url=YOUR_DOMAIN + '/cancel.html',
    )
    return JsonResponse({'id': session.id})

@csrf_exempt
def webhook(request):
    endpoint_secret = ''
    payload = request.body
    print(payload,'payload')
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
        payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        return HttpResponse(status=400)
    
    except stripe.error.SignatureVerificationError as e:
        return HttpResponse(status=400)
    
    print('Handled event type {}'.format(event['type']))

    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        print(session)
        line_items = stripe.checkout.Session.list_line_items(session['id'], limit=1)
        print(line_items)
        return HttpResponse(status=200)
    
    if event.type == 'charge.failed':
        payment_intent = event.data.object
        print(payment_intent)   
        return HttpResponse(status=200)
    

def AccountPage(request):
    return render(request,'AccountManagementPage.html',{"user":request.user.username})