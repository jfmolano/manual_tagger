$(document).ready(function() {
    $("#submit")
    .click(function () {
        var str = "";
        $( "select option:selected" ).each(function() {
          str += $( this ).text() + "";
        });
        image_name = $( "#image_name" ).text()
        url_get = "http://localhost:8080/move/" + image_name + "/" + str
        console.log(url_get)
        $.ajax({
            type: "GET",
            url: url_get
        }).then(function() {
            console.log("Then")
            $.ajax({
                type: "GET",
                url: "http://localhost:8080/random_image"
            }).then(function(data) {
                console.log(data)
                $( "#image_name" ).text(data["image_name"])
                console.log('http://127.0.0.1:8080/images/' + data["image_name"])
                $( "#unclassified_image" ).attr("src",('http://127.0.0.1:8080/images/' + data["image_name"]));
            });
        });
      })
});