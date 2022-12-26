from django.urls import path
from .views import RegisterPage,LoginPage,HomePage,MovieDetailPage,TheaterSelectionPage,AddMoviePage,BookingPage,UserRegisterViewSet,UserLoginView,UserLogoutView,SeatSelectionPage,UserBookingView,create_checkout_session,success,webhook,cancel,contact_us
from .api import MoviesApi,ScreenMovieApi,ChoicesApi,BookingApi,ChatBotApi
from rest_framework import routers

router = routers.SimpleRouter()
router.register(r'get/movie',MoviesApi,basename='movies') 
router.register(r'get/screen/movie',ScreenMovieApi,basename='screenmovies')  
router.register(r'get/booking',BookingApi,basename='booking') 
urlpatterns = [
    path('Signup/',UserRegisterViewSet.as_view(),name='Register'),
    path('Signin/',UserLoginView.as_view(),name='Login'),
    path('Signout/',UserLogoutView.as_view(),name='Logout'),
    path('',HomePage.as_view(),name='HomePage'),
    path('Details/',MovieDetailPage.as_view(),name='MovieDetailPage'),
    path('Details/Shows/',TheaterSelectionPage.as_view(),name='TheaterSelectionPage'),
    path('Add/Movie/',AddMoviePage.as_view(),name='AddMoviePage'),
    path('get/all/choices/',ChoicesApi.as_view(),name='ChoicesApi'),
    path('shows/booking/',BookingPage.as_view(),name='BookingPage'),
    path('Seat/Selection/',SeatSelectionPage.as_view(),name='SeatSelectionPage'),
    path('View/Bookings/',UserBookingView.as_view(),name='UserBookingView'),
    path('create-checkout-session/', create_checkout_session, name='checkout'),
    path('success.html/', success,name='success'),
    path('cancel.html/', cancel,name='cancel'),
    path('webhooks/stripe/', webhook,name='webhook'),
    path('chatbot/api/',ChatBotApi.as_view(),name='ChatBotApi'),
    path('Contact/Us/',contact_us,name='ContactUsPage')
    # path('check_seats_revert/',check_seats_revert,name='check_seats_revert')
]

urlpatterns += router.urls

print(urlpatterns)