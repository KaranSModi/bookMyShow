function get(url, callback) {
    var token = localStorage.getItem("access-token");
    headerParams = { 'Authorization': token };
    if (token != null) {
        $.ajax({
            type: 'GET',
            headers: headerParams,
            data: {},
            url: url,

            beforeSend: function () {
                $('.spinner-border').show();
            },
            complete: function () {
                $('.spinner-border').hide();
            },
            success: function (res) {

                if (callback) {
                    callback(res)
                }
            },
            error: function (error) {
                if (error.status == 401) {
                    post("/api/token/refresh/", { "refresh": localStorage.getItem("refresh-token") }, function (res) {
                        console.log(res);
                    })
                }
                // token = localStorage.getItem('refresh-token')
                // post('/api/token/refresh/', { "refresh": localStorage.getItem("refresh-token") },
                //     function newTokenSet(res) {
                //         localStorage.setItem("access-token", `Bearer ${res.access}`);
                //         console.log('new token authorisedd');
                //         login();

                //     }
                // )

            }
        })
    }
    else {
        $.ajax({
            type: 'GET',
            data: {},
            url: url,

            beforeSend: function () {
                $('.spinner-border').show();
            },
            complete: function () {
                $('.spinner-border').hide();
            },
            success: function (res) {

                if (callback) {
                    callback(res)
                }
            },
            error: function (error) {

            }
        })
    }
}

function post(url, data, callback) {
    data = data
    var token = localStorage.getItem("access-token");
    headerParams = { 'Authorization': token };
    if (token != null) {
        $.ajax({
            type: 'POST',
            data: data,
            headers: headerParams,
            url: url,
            beforeSend: function () {

            },
            complete: function () {

            },
            success: function (res) {
                if (callback) {
                    callback(res)
                }

            },
            error: function () {
                // alert("Unauthorized")
                alert('POST REQUEST FAILED');
            }
        })
    }
    else {
        $.ajax({
            type: 'POST',
            data: data,
            url: url,
            beforeSend: function () {

            },
            complete: function () {

            },
            success: function (res) {
                if (callback) {
                    callback(res)
                }

            },
            error: function () {
                // alert("Unauthorized")

                alert('POST REQUEST FAILED');
            }
        })
    }


}

// function getNewToken() {
//     $.ajax({
//         type: 'POST',
//         data: { "refresh": localStorage.getItem("refresh-token") },
//         url: "/api/token/refresh/",
//         success: function (res) {
//             alert('new token set')
//             localStorage.setItem("access-token", `Bearer ${res.access}`);
//         },
//     })
// }


function patch(url, data, callback) {
    var token = localStorage.getItem("access-token");
    headerParams = { 'Authorization': token };
    $.ajax({
        url: url,
        headers: headerParams,
        data: JSON.stringify(data),
        type: 'PATCH',
        contentType: 'application/json',
        processData: false,
        dataType: 'json',
        success: function (res) {
            if (callback) {
                callback(res)
            }
        }
    });
}



function callUserAuthenticationHandler(thiss, e) {
    e.preventDefault();
    var dataObject = {}
    var formData = new FormData(thiss);
    for (var p of formData) {
        let name = p[0];
        let value = p[1];
        dataObject[name] = value;
        console.log(name, value)
    }
    post("/Signup/", dataObject, function (res) {
        if ((res.status) == "Signin") {
            post("/Signin/", dataObject, function (res) {
                console.log(res, '??????');
                setAuthTokensForUser(res.message);
                $("#userAuthButton").empty()
                $("#userAuthButton").html("SignOut")
                $("#userAuthButton").on("click", function () {
                    post("/Signout/", {}, function (res) {
                        console.log(res, 'res');
                    })
                })
                alert("Login Successfull");
            })
        }
    })
}



function setAuthTokensForUser(data) {
    if ((localStorage.getItem("access-token")) == null) {
        localStorage.setItem("access-token", `Bearer ${data.access}`);
        localStorage.setItem("refresh-token", `Bearer ${data.refresh}`);
    }
}


function openNav() {
    document.getElementById("mySidenav").style.width = "250px";
}

function closeNav() {
    document.getElementById("mySidenav").style.width = "0";
}