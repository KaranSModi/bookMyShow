const urlParams = new URLSearchParams(window.location.search);
const myParam = urlParams.get('id');
screenMovieId = "";
prevent = true;
function any() {
    get(`/get/movie/${myParam}`, function (resMovie) {
        console.log(resMovie);
        $("#movieTitle").html(`${resMovie.title}`);
        $("#movieGenres").append(`<span class="badge rounded-pill text-bg-secondary">${resMovie.genre}</span>`)
    })
    get("/get/screen/movie/?id=" + myParam, function (res) {
        console.log(res, 'res');
        res.map(function (key, index) {
            $("#divForRow").append(`<div class="row gx-5 p-1 border bg-light" style="margin-top:1rem;">
                <div class="col-lg">
                    <div style="font-size: small;color: black;font-weight: bold;">
                       ${key.cinema}
                    </div>
                </div>
                <div class="col-lg">
                <li class="list-group-item p-1 bg-light">
                        ${getButtions(key.slots)}
                    </li>
                </div>
            </div > `
            )
        });
    })
}
any()

function getCimeaName(name) {
    return `< div class="col-lg" >
                            <div style="font-size: small;color: black;font-weight: bold;">
                                ${name}
                            </div>
    </div > `
}

function getButtions(data) {
    fullstr = ""
    // setDateOfShow = $("#screenShowDate").html(`${(data[0]).date}`);
    for (i of data) {
        fullstr += `<button title="${i.start_duration} - ${i.end_duration}\n GOLD - ₹${i.seat_price}" type="button" onclick=getAvailableSeatsForScreen(${i.id}) data-bs-toggle="modal" data-bs-target="#exampleModal1"
            class="btn btn-outline-secondary" style="color: green;margin-left:5px;">${i.start_duration}</button>`
    }
    return fullstr
}

function getAvailableSeatsForScreen(id) {
    console.log('id', id);
    screenMovieId = id;
    get(`/get/booking/?id=${id}`, function (res) {
        $("#showAvailableSeats").empty();
        console.log('available seats', res.availableSeats);
        $("#showAvailableSeats").append(`Avalilabe Seats <br/>${res.availableSeats}`)
        
        for (let index = 1; index <= 8; index++) {
            let disabled = 'disabled';
            if (index <= res.availableSeats) {
                disabled = null;
            }
            $("#seatButtons").append(
                `<button onmouseenter="showVectors(event,'i${index}')" value="${index}" type="button"
            class="btn btn-md  btn-outline-danger" style="color:black"
            onclick="bookSeat(event,this)" ${disabled}>${index}
            </button>&nbsp;`
            )
        }

        // for (let index = 1; index <= 8; index++) {
        //     $("#seatButtons").append(
        //         `<button onmouseenter="showVectors(event,'i${index}')" value="${index}" type="button"
        //     class="btn btn-md  btn-outline-danger" style="color:black"
        //     onclick="bookSeat(event,this)">${index}
        //     </button>&nbsp;`
        //     )
        // }
    })
}

function renderShowRows(data) {
    nameNew = data[0].cinema.name;
    nameDiv = getCimeaName(nameNew)
    fullstr = getButtions(data, nameNew)
    $("#divForRow").append(
        `< div class="row gx-5 p-1 border bg-light" >
                            ${nameDiv}
                        <div class="col-lg">
                            <li class="list-group-item p-1 bg-light">
                                ${fullstr}
                            </li>
                        </div>
    </div > `)
}

function checkIsPaid(idForBooking) {
    console.log('timeout', idForBooking);
    patch(`/get/booking/${idForBooking}/`, { "payment_status": false }, function (res) {
        console.log(res, 'patch booking');
    })
}


function bookSeat(e, thiss) {
    e.preventDefault();
    post("/get/booking/", { "screen_movie": screenMovieId, "seat_count": thiss.value }, function (res) {
        console.log('booking success', res);
        if (res.status == "booked") {
            $("#showBookingStatusAlert").html(`
            <div id="bookAlert" class="alert alert-success" role="alert">
            Seats Booked Succefully
            </div>
            `);
            $("#showBookingStatusAlert").append(`
            <div style="text-align: center;">
            Please Make Payment....
            </div>
            <li class="list-group-item p-1 bg-light">
            Total : ${(res.details[0]).total} &#x20b9;
            </li>
            <li class="list-group-item p-1 bg-light">
            <button onclick="callCheckout(${(res.details[0]).bookingId})" id="checkout-button" type="button" class="btn btn-sm btn-info">Confirm And Pay ${(res.details[0]).total} &#x20b9;</button></a>
            </li>
            `);
            setTimeout(function (alert) {
                var alert = bootstrap.Alert.getOrCreateInstance('#bookAlert')
                alert.close()

                // var modal = $("#exampleModal1").modal('hide');
            }, 2000);
            let idForBooking = (res.details[0]).bookingId
            setCookie("bookingId", idForBooking);
            setTimeout(function () { checkIsPaid(idForBooking) }, 120000);
        }
        if (res.status == "ran out of seats") {
            $("#showBookingStatusAlert").empty();
            $("#showBookingStatusAlert").html(`
            <div id="bookAlert" class="alert alert-danger" role="alert">
            Ran Out Of Seats For This Show
            </div>
            `);
            setTimeout(function (alert) {
                var alert = bootstrap.Alert.getOrCreateInstance('#bookAlert')
                alert.close()
                var modal = $("#exampleModal1").modal('hide');
            }, 2000);
        }
    })
}


function callCheckout(id) {
    var stripe = Stripe('pk_test_51Lp4iHSHgSlrTPSRowRvGUQ1qo1lNrlvelvFe26I3acvUZlCBfKIzPL1L3qwG0HIkqet0hp7JHOx8AvnWqh3R7j4005uvhkqjN');
    var checkoutButton = document.getElementById('checkout-button');
    prevent = false;
    // Create a new Checkout Session using the server-side endpoint you
    fetch(`/create-checkout-session/?id=${id}`, {
        method: 'POST',
    })
        .then(function (response) {
            return response.json();
        })
        .then(function (session) {
            return stripe.redirectToCheckout({ sessionId: session.id });
        })
        .then(function (result) {
            // If `redirectToCheckout` fails due to a browser or network
            // error, you should display the localized error message to your
            // customer using `error.message`.
            if (result.error) {
                alert(result.error.message);
            }
        })
        .catch(function (error) {
            console.error('Error:', error);
        });
}





function setCookie(name, value, days) {
    var expires = "";
    if (days) {
        var date = new Date();
        date.setTime(date.getTime() + (10 * 60 * 1000));
        expires = "; expires=" + date.toUTCString();
    }
    document.cookie = name + "=" + (value || "") + expires + "; path=/";
}

function getCookie(name) {
    var nameEQ = name + "=";
    var ca = document.cookie.split(';');
    for (var i = 0; i < ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0) == ' ') c = c.substring(1, c.length);
        if (c.indexOf(nameEQ) == 0) return c.substring(nameEQ.length, c.length);
    }
    return null;
}