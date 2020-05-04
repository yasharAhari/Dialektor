
$(document).ready(function(){
    set_up_player()
});


function set_up_player()
{
    var playbacker = document.createElement("AUDIO");

    playbacker.src = "/raw/" + $("#sound-id").html()
    $("#playback").append(playbacker);
    playbacker.currentTime=0;
    sleep(200);
    $("#bar").show();
    $("#progress").css("width", "0%");
    $("#progress").show();
    $("#start").show();
    $("#start").show();
    $("#start").click(function(){
        $("#start").hide();
        $("#pause").show();
        playbacker.play();
        timer = window.setInterval(function(){playback_tick(playbacker)},250);
    });
    $("#pause").click(function(){
        $("#pause").hide();
        $("#start").show();

        playbacker.pause();
        window.clearInterval(timer);
    });

}

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}



/**
 * returns a formatted string of like 00:00 based on the number of seconds provided
 * @param seconds time
 * @returns {string} mm:ss
 */
function get_minute_second(seconds) {
    // turn it to integer
    seconds = Math.floor(seconds);
    // convert it to minutes and seconds
    let minute = Math.floor(seconds/60);
    let second = seconds%60;

    // format both to double digit
    let f_minute = ('0' + minute).slice(-2);
    let f_second = ('0' + second).slice(-2);
    return f_minute + ':' + f_second;
}

/**
 * This is like recording_tick but for when playing back the recorded piece.
 */
function playback_tick(audioSource) {
    // set the timing stuff
    timer_text = document.getElementById("time");     // the timer
    progress = document.getElementById("progress");   // progress bar
    let current_time = audioSource.currentTime;
    let total_time = audioSource.duration;
    timer_text.innerText = get_minute_second(current_time) + "/" + get_minute_second(total_time);

    // update the progress bar
    if(current_time<= total_time)
    {
        progress.style.width = (current_time / total_time) * 100 + "%";
    }
    else
    {
        progress.style.width = "100%";
    }

    if(audioSource.ended)
    {
        // play finished, cleanup
        window.clearInterval(timer);
        $("#pause").hide();
        $("#start").show();
    }
}
