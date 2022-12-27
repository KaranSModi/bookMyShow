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
                localStorage.setItem("signed in", true);
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


function sendChatBotMessage(thiss, e) {
    e.preventDefault();
    var dataMessage = {};
    var formData = new FormData(thiss);
    for (var p of formData) {
        let name = p[0];
        let value = p[1];
        dataMessage[name] = value;
    }
    $('.chatbox__body').append(`<div class="chatbox__body__message chatbox__body__message--right">
    <div class="chatbox_timing">
        <ul>
            <li><a href="#"><i class="fa fa-calendar"></i> 22/11/2018</a></li>
            <li><a href="#"><i class="fa fa-clock-o"></i> 7:00 PM</a></a></li>
        </ul>
    </div>
    <img src="/static/images/chatbotLogo.png" alt="Picture">
    <div class="clearfix"></div>
    <div class="ul_section_full">
        <ul class="ul_msg">
            <li><strong>${dataMessage.message}</strong></li>
        </ul>
        <div class="clearfix"></div>
        <ul class="ul_msg2">
            <li><a href="#"><i class="fa fa-pencil"></i> </a></li>
            <li><a href="#"><i class="fa fa-trash chat-trash"></i></a></li>
        </ul>
    </div>
</div>`)
    post("/chatbot/api/", dataMessage, function (res) {
        console.log('server responded', res);

        $('.chatbox__body').append(`<div class="chatbox__body__message chatbox__body__message--left">

    <div class="chatbox_timing">
        <ul>
            <li><a href="#"><i class="fa fa-calendar"></i> 22/11/2018</a></li>
            <li><a href="#"><i class="fa fa-clock-o"></i> 7:00 PM</a></a></li>
        </ul>
    </div>
    <img src="/static/images/chatbotLogo.png" alt="Picture">
    <div class="clearfix"></div>
    <div class="ul_section_full">
        <ul class="ul_msg">
            <li><strong>${res.message}</strong></li>
        </ul>
        <div class="clearfix"></div>
        <ul class="ul_msg2">
            <li><a href="#"><i class="fa fa-pencil"></i> </a></li>
            <li><a href="#"><i class="fa fa-trash chat-trash"></i></a></li>
        </ul>
    </div>

</div>`)
    })
}