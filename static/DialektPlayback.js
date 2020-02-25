function set_up_player()
{
    $("#start").show()
    var playbacker = document.createElement("AUDIO");

    playbacker.src = "http://127.0.0.1:8000/sounds/" + $("#sound-id").html()

    $("#start").click(function(){
        $("#start").hide();
        $("#pause").show();
        playbacker.paused = false;
    });
    $("#pause").click(function(){
        $("#pause").hide();
        $("#start").show();
        playbacker.paused = true;
    });

}
