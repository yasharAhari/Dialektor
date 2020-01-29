const record_modes = {
  READY: 0,     // The recorder and encoder is loaded and ready to record
  RECORDING: 1, // The recorder is in progress
  PAUSED: 2,    // The user paused the record
  FINISHED: 3,  // The user ended the recording
  ERROR: 4      // There is an error occurred somewhere
};

const user_requests = {
    START_RECORDING: 0,
    PAUSE_RECORDING: 1,
    RESUME_RECORDING: 2,
    STOP_RECORDING: 3,
    PLAY_RECORDED: 4,
    PAUSE_RECORDED: 5,
    RESUME_PLAYING: 6
}



let mode;       // The current mode: recordMode

// Recording info variables
let recording = false;
let context_time = 0;

// Recorder instance variables
let timer;

let input;
let recorder;

let file;

let recordedAudio;

// other html elements
const timer_text = document.getElementById("time");
const progress = document.getElementById("progress");

recorder_initial_load();

/**
 * This function to be called once on loading the page. It initializes the recorder.
 */
function recorder_initial_load() {



    console.log("The Recorder Loaded");

    // get the audio stream
    navigator.mediaDevices.getUserMedia({audio: true, video: false}).then(function (stream) {
        recorder = RecordRTC(stream, {
            type: 'audio',
           // mimeType: 'audio/webm',
            recorderType: MediaStreamRecorder
        });
        mode = record_modes.READY;
        console.log('Recorder is ready!');
    });


}

/**
 * This functions is receives button inputs and dose the recording functionality appropriately
 * @param user_request the user request from user_requests
 */
function button_press(user_request) {
    if(user_request === user_requests.START_RECORDING || user_request === user_requests.RESUME_RECORDING)
    {
        if(mode === record_modes.READY)
        {
            // change the mode first
            mode = record_modes.RECORDING;



            // start the timer
            timer_text.innerText = "00:00";
            timer_text.style.color = "";
            timer = window.setInterval(record_tick,1000);

            // start the recorder
            recorder.startRecording();
        }
        else if(mode === record_modes.PAUSED)
        {
            // change mode
            mode = record_modes.RECORDING;



            // resume recording
            recorder.resumeRecording();

            // start the interval
            timer = window.setInterval(record_tick,1000);

        }
    }
    else if(user_request === user_requests.PAUSE_RECORDING)
    {
        if(mode === record_modes.RECORDING)
        {
            //change the mode first
            mode = record_modes.PAUSED;



            recorder.pauseRecording();

            window.clearInterval(timer);

        }
    }
    else if(user_request === user_requests.STOP_RECORDING)
    {
        if(mode === record_modes.RECORDING || mode === record_modes.PAUSED)
        {
            // change the mode first
            mode = record_modes.FINISHED;

            // TODO: Change style if needed
            window.clearInterval(timer);
            // finish the recording
            recorder.stopRecording(function () {
                let blob = recorder.getBlob();
                let url = URL.createObjectURL(blob);
                recordedAudio = new Audio(url);
                console.log("TOTAL TIME:" + recordedAudio.duration);
                recordedAudio.load();
                timer_text.innerText = "00:00/" + get_minute_second(context_time);
                progress.style.width = "0";
            });




        }

    }
    else if(user_request === user_requests.PLAY_RECORDED)
    {
        recordedAudio.play();
        // time interval is much shorter because of progress bar
        timer = window.setInterval(playback_tick,250);

    }
    else if(user_request === user_requests.PAUSE_RECORDED)
    {
        recordedAudio.pause();
        window.clearInterval(timer);
    }

}





/**
 * The function tick to be used with a interval of one second when recording. It increase the recorded time by one
 * and updates the proper html element that meant to show the time.
 */
function record_tick()
{
    // get the recorded time from recorder
    context_time = context_time + 1;



    // Add both in one format of 00:00 and show it
    timer_text.innerText = get_minute_second(context_time);
}

/**
 * This is like recording_tick but for when playing back the recorded piece.
 */
function playback_tick() {
    // set the timing stuff
    let current_time = recordedAudio.currentTime;
    let total_time = context_time;
    timer_text.innerText = get_minute_second(current_time) + "/" + get_minute_second(total_time);

    // set the progress bar
    if(current_time<= total_time)
    {
        progress.style.width = (current_time / total_time) * 100 + "%";
    }
    else
    {
        progress.style.width = "100%";
    }

    if(recordedAudio.ended)
    {
        // play finished, cleanup
        window.clearInterval(timer);
        $("#playPause").hide();
        $("#start").show();
    }
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