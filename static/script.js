$(document).ready(function(){
  
  $("#rec").click(function(){
    $("#rec").hide();
    $("#pause").show();
    $("#time").show();
  });
  
  $("#pause").click(function(){
    $("#pause").hide();
    $("#stop").show();
    $("#smallRec").css({"background":"#cd0000"});
  });

  $("#smallRec").click(function(){
    $("#smallRec").css({"background":"#fff"});
    $("#stop").hide();
    $("#pause").show();
  });
  
  $("#stop").click(function(){
    $("#stop").hide();
    $("#start").show();
    $("#smallRec").hide();
    $("#data").show();
    $("#bar").show();
    $("#progress").show();
  });


});
