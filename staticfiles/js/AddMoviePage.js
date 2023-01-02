var form_data = new FormData();

function choicesResponseHandler(div, data) {
    data.map((x, y) => {
        div.append($("<option>").attr('value', x[0]).text(x[0]));
    })
}

function getChoices() {
    get("/get/all/choices/", function (res) {
        Object.keys(res).forEach(function (key, index) {
            var div = $(`#${key}`);
            choicesResponseHandler(div, res[key]);
        });

    })

}

getChoices()

function changeImage(dis) {
    const file = dis.files[0];
    console.log(file);
    if (file) {
        let reader = new FileReader();
        reader.onload = function (event) {
            // console.log(event.target.result);
            form_data.append('profile_pic', file)
            $('#imgPreview').attr('src', event.target.result);
        }
        reader.readAsDataURL(file);
    }
};

$(document).ready(() => {

    // $("#drop-area").on('dragenter', function (e) {
    //     e.preventDefault();
    // });

    // $("#drop-area").on('dragover', function (e) {
    //     e.preventDefault();
    // });

    // $("#drop-area").on('drop', function (e) {
    //     e.preventDefault();
    //     var image = e.originalEvent.dataTransfer.files;
    //     createFormData(image);
    // });


});



function handleForm(e) {
    e.preventDefault();
    var csrf_token = $('input[name="csrfmiddlewaretoken"]').val();
    var title = $("#title").val()
    var desc = $("#desc").val()
    var date = $("#date").val()
    var time = $("#time").val()
    var genre = $("#genre").val()
    let image = $('#photo').val();
    var langauge = $("#langauge").val()
    form_data.append("csrfmiddlewaretoken", csrf_token);
    form_data.append("title", title);
    form_data.append("description", desc);
    form_data.append("date", date);
    form_data.append("time", time);
    form_data.append("genre", genre);
    form_data.append("langauge", langauge);
    console.log(title, desc, date, time, genre, langauge);

}



$(document).ready(function (e) {
    // Submit form data via Ajax
    $("#MovieForm").on('submit', function (e) {
        e.preventDefault();
        $.ajax({
            type: 'POST',
            url: '/get/movie/',
            data: new FormData(this),
            dataType: 'json',
            contentType: false,
            cache: false,
            processData: false,
            beforeSend: function () {
                $('.submitBtn').attr("disabled", "disabled");
                $('#fupForm').css("opacity", ".5");
            },
            success: function (response) {
                if (response.status == 1) {
                    $('#fupForm')[0].reset();
                    $('.statusMsg').html('<p class="alert alert-success">' + response.message + '</p>');
                } else {
                    $('.statusMsg').html('<p class="alert alert-danger">' + response.message + '</p>');
                }
                $('#fupForm').css("opacity", "");
                $(".submitBtn").removeAttr("disabled");
            }
        });
    });
});

