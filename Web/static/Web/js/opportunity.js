$(document).ready(function () {

    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    var csrftoken = getCookie('csrftoken');

    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });
});

function addseelater(id_opp) {
    console.log("ajax vers le serveur pour ajouter dans le see_later");
    $.ajax({
        url : '/add-see-later', // the endpoint
        type : "POST", // http method
        data : { 'id_opp': id_opp }, // data sent with the post request

        // handle a successful response
        success : function(result) {
            $("#"+id_opp+" li:first-child").html('<a onclick="removeseelater(\''+id_opp+'\')">Remove from see later</a>');
        },

        // handle a non-successful response
        error : function(xhr,errmsg,err) {

        }
    });
}

function removeseelater(id_opp) {
    console.log("ajax vers le serveur pour retirer de see_later");
    $.ajax({
        url : '/remove-see-later', // the endpoint
        type : "POST", // http method
        data : { 'id_opp': id_opp }, // data sent with the post request

        // handle a successful response
        success : function(result) {
            $("#"+id_opp+" li:first-child").html('<a onclick="addseelater(\''+id_opp+'\')">See later</a>');
        },

        // handle a non-successful response
        error : function(xhr,errmsg,err) {

        }
    });
}
