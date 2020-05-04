$(document).ready(function(){
   $(".researcher-start").click(function(){
      $(".researcher-start").each(function() {
         if($(this).css("display") == "none") //If a different sound is already playing
         {
            $(this).next().hide(); //Stop it
            $(this).show();
            $(this).parent().parent().find('.researcher-sound-audio').get(0).pause();
         }
      });
      $(this).hide();
      $(this).next().show();
      audio = $(this).parent().parent().find(".researcher-sound-audio").get(0);
      audio.loop = true;
      audio.play();
   })
   $(".researcher-pause").click(function(){
      $(this).hide();
      $(this).prev().show();
      $(this).parent().parent().find(".researcher-sound-audio").get(0).pause();
   })
   $(".researcher-sound-download").click(function(){
      window.location.assign('/download/' + $(this).parent().attr('id'));
   })
});