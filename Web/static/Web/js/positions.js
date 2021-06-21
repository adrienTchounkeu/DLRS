var nbreposition=0;
var markers = [];
var locations = [];
var names = [];

function initMap() {
    var myLatLng = {lat: 3.836925, lng: 11.479410};
    var map = new google.maps.Map(document.getElementById('map-container-7'), {
        center: myLatLng,
        zoom: 10
    });
    var geocoder = new google.maps.Geocoder;

    google.maps.event.addListener(map,'click',function (event) {
        var position={lat: event.latLng.lat(), lng: event.latLng.lng()};
        geocodeLatLng(geocoder, position);
        setTimeout(function () {
            console.log('ajout de la localisation');
            console.log(names[nbreposition]);
            $("#locations-selected").append(
                '<li class="list-group-item d-flex justify-content-between align-items-center">'
                + names[nbreposition]
                + '<button type="button" class="btn btn-deep-purple btn-sm" id="' + nbreposition + '"' +
                ' onclick="deleteli(' + nbreposition + ')"><i class="fa fa-times"></i></button></li>'
            );
            var markerPosition = new google.maps.Marker({
                map: map,
                position: position,
            });
            markers.push(markerPosition);
            locations.push(position.lat + '|' + position.lng);
            nbreposition = nbreposition + 1;
        }, 2000);
    });
}

function geocodeLatLng(geocoder, latlng) {
    geocoder.geocode({'location': latlng}, function(results, status) {
        if (status === google.maps.GeocoderStatus.OK) {
            if (results[0]) {
                console.log(results[0].formatted_address);
                names.push(results[0].formatted_address);
            } else {
            }
        } else {
        }
    });
}

function deleteli(id) {
    $('#'+id).parent().remove();
    markers[id].setMap(null);
    locations[id]='del';
    names[id] = 'del';
}

$(document).ready(function () {
    // using jQuery
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

    $('#submit-form-step-4').click(function () {
        cleanedlocations='';
        i=0;
        while (i<locations.length && locations[i]=='del'){
            i++;
        }
        if (i!=locations.length){
            //cleanedlocations=names[i]+'|'+locations[i];
            cleanedlocations = 'Yaounde|' + locations[i];
            i++;
        }
        while (i<locations.length){
            if (locations[i]!='del'){
                //cleanedlocations=cleanedlocations+"-"+names[i]+'|'+locations[i];
                cleanedlocations = cleanedlocations + '-Yaounde|' + locations[i];
            }
             i++;
        }
        if (cleanedlocations.length==0){
            alert("Select almost one location");
            return;
        }
        preferences='';
        $('input:checked').each(function () {
            preferences = preferences + "-" + $(this).attr('id');
        });
        if (preferences.length==0){
            alert("Select almost one preference");
            return;
        }
        $.ajax({
            url : '/sign-up-last-step', // the endpoint
            type : "POST", // http method
            data : { 'user_locations' : cleanedlocations, 'user_preferences' : preferences, 'id_user': $('#blabla').attr('value') }, // data sent with the post request

            // handle a successful response
            success : function(result) {
                window.location.href=result
            },

            // handle a non-successful response
            error : function(xhr,errmsg,err) {

            }
        });
    });
});


