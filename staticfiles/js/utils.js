setTimeout(function checkIsPaid() {
    console.log('timeout', idForBooking);
    patch(`/get/booking/${idForBooking}/`, { "payment_status": false }, function (res) {
        console.log(res, 'patch booking');
    })
}, 60000);