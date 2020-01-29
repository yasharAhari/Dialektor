$(document).ready(function(){
  
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
    button_press(user_requests.PAUSE_RECORDING);
  });

  $("#smallRec").click(function(){
    $("#smallRec").css({"background":"#fff"});
    $("#stop").hide();
    $("#pause").show();
    button_press(user_requests.RESUME_RECORDING);
  });
  
  $("#stop").click(function(){
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
    
});
