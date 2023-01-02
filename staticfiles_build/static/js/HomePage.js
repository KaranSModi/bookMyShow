console.log('home');

function getAndFetchMovies() {

    get("/get/movie/", function (res) {
        console.log(res,'All Movies');
        var myDiv = document.getElementById("myCardsRow")
            res.map(function (data, indx) {
                $("#myCardsRow").append(
                    `<div class="col-sm-3">
                <div class="card">
                        <img src="${data.poster}"  onclick="movieDetails(${data.id})" class="card-img-top" alt="Hollywood Sign on The Hill">
                    <div class="card-body text-center">
                        <h5 class="card-title">${data.title}</h5>
                    </div>
                </div>
            </div>`)
            })
    })

}

getAndFetchMovies()


function movieDetails(id){
    window.location.href=`/Details/?id=${id}`;
}