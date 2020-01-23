$(document).ready(function(){
  
  $("#rec").click(function(){
    $("#rec").hide();
    $("#pause").show();
    $("#time").show();
  });
  
  $("#pause").click(function(){
    $("#pause").hide();
    $("#stop").show();
    $("#smallRec").show();
  });

  $("#smallRec").click(function(){
    $("#smallRec").hide();
    $("#stop").hide();
    $("#pause").show();
  });
  
  $("#stop").click(function(){
    $("#stop").hide();
    $("#start").show();
    $("#smallRec").hide();
  });


});
