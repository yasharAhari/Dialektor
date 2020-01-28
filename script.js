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
    $("#stop").hide();
    $("#pause").show();
    $("smallRec").hide();
});
