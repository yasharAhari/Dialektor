
$(document).ready(function(){
  $("#smallRec").css("pointer-events","none");    // disable click events to be registered.
  $("#rec").click(function(){
    $("#rec").hide();
    $("#pause").show();
    $("#time").show();
    button_press(user_requests.START_RECORDING);
  });
  
  $("#pause").click(function(){
    $("#pause").hide();
    $("#stop").show();
    $("#smallRec").css({"background":"#cd0000"});
    $("#smallRec").css("pointer-events","auto");
    button_press(user_requests.PAUSE_RECORDING);
  });

  $("#smallRec").click(function(){
    $("#smallRec").css({"background":"#fff"});
    $("#smallRec").css("pointer-events","none");
    $("#stop").hide();
    $("#pause").show();
    button_press(user_requests.RESUME_RECORDING);
  });
  
  $("#stop").click(function(){
    $("#length").val($("#time").html());
    $("#stop").hide();
    $("#start").show();
    $("#smallRec").hide();
    $("#data").show();
    $("#bar").show();
    $("#progress").show();
    button_press(user_requests.STOP_RECORDING);
  });

  $("#start").click(function(){
    $("#start").hide();
    $("#playPause").show();
    button_press(user_requests.PLAY_RECORDED);
  });
  
  $("#playPause").click(function(){
    $("#playPause").hide();
    $("#start").show();
    button_press(user_requests.PAUSE_RECORDED);
  });
  
  $("#save").click(function () {
    button_press(user_requests.SAVE);
  });
  
  $("#discard").click(function () {
    let review = confirm("Your recording will be lost! Are you sure?");
    if(review === true)
    {
      button_press(user_requests.DISCARD);
      $("#rec").show();
      $("#smallRec").show();
      $("#data").hide();
      $("#bar").hide();
      $("#progress").hide();
      $("#pause").hide();
      $("#start").hide();
      $("#time").hide();
      $("#playPause").hide();
      $("#smallRec").css("pointer-events","none");
      $("#smallRec").css({"background":"#fff"});
    }
  });
    
});
