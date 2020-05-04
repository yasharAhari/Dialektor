$(document).ready(function(){
    $("#searchNoOP").click(function(){
        var newData = new FormData();
        newData.append("tags", $("#researcher-tags").val());
        newData.append("category", $("#researcher-category").val());
        newData.append("after", $("#researcher-after-date").val());
        newData.append("before", $("#researcher-before-date").val());
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
            url: 'search',
            data: newData,
            type: 'POST',
            contentType: false,
            processData: false,
        }).done(function(data) {
            //window.location.replace("http://127.0.0.1:8000/sounds/" + data)
        });
    });
});