const urlParams = new URLSearchParams(window.location.search);
const myParam = urlParams.get('id');

function movieDetails(id) {
    get(`/get/movie/${id}`, function (res) {
        console.log(res, 'detail');
        $("#descContent").html(`${res.description}`);
        $("#titleContent").html(`${res.title}`);
        $("#redirectToShowsPage").attr("href", `/Details/Shows/?id=` + res.id);
        var poster = document.getElementById("posterContent");
        poster.setAttribute("src", `${res.poster}`);
    })
}

movieDetails(parseInt(myParam))