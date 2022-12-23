from celery import shared_task
from .models import Booking
from datetime import datetime
import pytz



@shared_task(name='revert_seats_func')
def test_func():
    utc = pytz.UTC
    bookings = list(Booking.objects.all().values("id","created_at","seat_block_duration"))
    date_time_current = datetime.now()
    date_time_current = date_time_current.replace(tzinfo=utc)
    checking_list = []
    for i in range(len(bookings)):
        booking_obj = bookings[i]
        if date_time_current > booking_obj.get("seat_block_duration"):
            obj = Booking.objects.get(id=booking_obj.get("id"))
            obj.delete()
            return True
    return False