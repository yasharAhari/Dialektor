
$(document).ready(function(){
 var collections = "";
 var alreadyClicked = false;
    $.ajaxSetup({
         beforeSend: function(xhr, settings) {
             function getCookie(name) {
                 var cookieValue = null;
                 if (document.cookie && document.cookie != '') {
                     var cookies = document.cookie.split(';');
                     for (var i = 0; i < cookies.length; i++) {
                         var cookie = jQuery.trim(cookies[i]);
                         // Does this cookie string begin with the name we want?
                         if (cookie.substring(0, name.length + 1) == (name + '=')) {
                             cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                             break;
                         }
                     }
                 }
                 return cookieValue;
             }
             if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
                 // Only send the token to relative URLs i.e. locally.
                 xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
             }
        }
    });
    $.ajax({
        url: 'collections',
        type: 'POST',
        contentType: false,
        processData: false,
    }).done(function(data) {
        collections = data;
        collections = collections.slice(0,-2);
        console.log("User collections: " + collections);
        collections = collections.split(",")
    });
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
    $("#data").css('display', 'flex');
    //$("#pic-box").show();
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
    if(!alreadyClicked)
    {
        button_press(user_requests.SAVE);
        $("#save").attr("value", "Saving...");
    }
    alreadyClicked = true;

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
      $("#pic-box").hide();
    }
  });

    var name = '';
    $('#collection').keyup(function(e) {
      var val = $(this).val();
      if(val == '') {
        $('#autocomplete').text('');
        return;
      }

      if (e.which === 37 || e.which === 13) {
        e.preventDefault();
        $('#collection').val(name);
        $('#autocomplete').text('');
        return;
      }

      var find = false;
      for (var i = 0; i < collections.length; i++) {
        name = collections[i].trim();
        if(name.indexOf(val) === 0) {
          find = true;
          break;
        } else {
          name = '';
        }
      }
      if(find === true) {
        $('#autocomplete').text(name);
        $("#add-collection").hide();
        $("#pic-box").hide();
      } else {
        $("#add-collection").show();
        $('#autocomplete').text('');
        $('#pic-box').show();
      }
    })
    $('#collection').keyup(function(e) {
      if($("#collection").val() == "")
      {
        $("#add-collection").hide();
      }
    });


    let readURL = function(input) {
        if (input.files && input.files[0]) {
            let reader = new FileReader();

            reader.onload = function (e) {
               $('#collection-pic').attr('src', e.target.result);
            };

            reader.readAsDataURL(input.files[0]);
        }
    };


    $("#image-upload").change(function(){
        readURL(this);
    });

    $("#pic-box").on('click', function() {
       $("#image-upload").click();
    });

$('img').on('load', function(){
    var css;
    var ratio=$(this).width() / $(this).height();
    var pratio=$(this).parent().width() / $(this).parent().height();
    if (ratio<pratio) css={width:'auto', height:'100%'};
    else css={width :'100%', height:'100%'};
    $(this).css(css);

});
});
