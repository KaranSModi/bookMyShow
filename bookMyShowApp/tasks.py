from celery import shared_task
from .models import Booking,ErrorLog
from datetime import datetime
import pytz
import json


@shared_task(name='revert_seats_func')
def test_func():
    print("121212121")
    utc = pytz.UTC
    bookings = list(Booking.objects.all().values("id","created_at","seat_block_duration"))
    date_time_current = datetime.now()
    date_time_current = date_time_current.replace(tzinfo=utc)
    checking_list = []
    for i in range(len(bookings)):
        booking_obj = bookings[i]
        obj = ErrorLog.objects.create()
        json_field = obj.error_data
        json_field["error"]="True"
        json_field["currentime"]=f"{date_time_current}"
        json_field["expiretime"]=str(booking_obj.get("seat_block_duration"))
        obj.save()
        
        if date_time_current > booking_obj.get("seat_block_duration"):
            obj = Booking.objects.get(id=booking_obj.get("id"))
            if obj.payment_status != True:
                obj.delete()
                
                return True
    return False