page=1;

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

function loadOthers() {
    $("#fseemore").html('<i class="fa fa-spinner fa-pulse purple-text m-auto"></i>');
    datas=[
        {
            'id_cat': 'cat3',
            'title_cat': 'cat1',
            'opp_cat':[
                {
                    'id_opp': 'opp8',
                    'name_opp': 'opp1',
                    'location': 'Yaounde, Biyem Assi',
                    'mean': '3.4',
                    'seelater': true
                },
                {
                    'id_opp': 'opp9',
                    'name_opp': 'opp2',
                    'location': 'Yaounde, Biyem Assi',
                    'mean': '3.5',
                    'seelater': false
                }
            ]
        },
        {
            'id_cat': 'cat7',
            'title_cat': 'cat2',
            'opp_cat': [
                {
                    'id_opp': 'opp10',
                    'name_opp': 'opp3',
                    'location': 'Yaounde, Biyem Assi',
                    'mean': '3.4',
                    'seelater': false
                },
                {
                    'id_opp': 'opp11',
                    'name_opp': 'opp4',
                    'location': 'Yaounde, Biyem Assi',
                    'mean': '3.5',
                    'seelater': true
                }
            ]
        }
    ]
    setTimeout(function () {
        for(i=0;i<datas.length;i++){
            $('.container').append('<h2><a href="/category/'+datas[i].id_cat+'">'+datas[i].title_cat+'</a></h2>' +
                '            <hr />' +
                '            <!-- Card deck -->' +
                '            <div class="card-deck" id="'+datas[i].id_cat+'">' +
                '            </div>');
            for (j=0;j<datas[i].opp_cat.length;j++){
                $('#'+datas[i].id_cat).append('<div class="card mt-3" id="'+datas[i].opp_cat[j].id_opp+'">' +
                    '                        <!--Card image-->' +
                    '                        <div class="view overlay img_opp">' +
                    '                            <img class="card-img-top" src="/static/Web/img/back-sign-1.jpg" alt="Card image cap" height="150">' +
                    '                            <a href="/opportunity/'+datas[i].opp_cat[j].id_opp+'">' +
                    '                                <div class="mask rgba-white-slight"></div>' +
                    '                            </a>' +
                    '                        </div>' +
                    '                        <!--Card content-->' +
                    '                        <div class="card-body">' +
                    '                            <!--Title-->' +
                    '                            <h4 class="card-title mt-0">'+datas[i].opp_cat[j].name_opp+'</h4>' +
                    '                            <!--Text-->' +
                    '                            <p class="card-text">'+datas[i].opp_cat[j].location+' &nbsp;&nbsp; | &nbsp;&nbsp; '+datas[i].opp_cat[j].mean+'</p>' +
                    '                            <!-- Provides extra visual weight and identifies the primary action in a set of buttons -->' +
                    '                        </div>' +
                    '                    </div>');

                if ($('#blabla').attr('value')!=''){
                    if(datas[i].opp_cat[j].seelater){
                        $('#'+datas[i].opp_cat[j].id_opp+' .card-body').append('<div class="dropdown">' +
                        '                                    <button class="btn btn-md more" type="button" data-toggle="dropdown">' +
                        '                                        <i class="fa fa-ellipsis-h rotate-icon"></i>' +
                        '                                    </button>' +
                        '                                    <ul class="dropdown-menu options-opp">' +
                        '                                        <li>' +
                        '                                            <a onclick="removeseelater(\''+datas[i].opp_cat[j].id_opp+'\')">Remove from see later</a>' +
                        '                                        </li>'+
                        '                                        <li>' +
                        '                                            <a>Pas intéressé</a>' +
                        '                                        </li>' +
                        '                                        <li>' +
                        '                                            <a>Signaler</a>' +
                        '                                        </li>' +
                        '                                    </ul>' +
                        '                                </div>');
                    }
                    else{
                        $('#'+datas[i].opp_cat[j].id_opp+' .card-body').append('<div class="dropdown">' +
                        '                                    <button class="btn btn-md more" type="button" data-toggle="dropdown">' +
                        '                                        <i class="fa fa-ellipsis-h rotate-icon"></i>' +
                        '                                    </button>' +
                        '                                    <ul class="dropdown-menu options-opp">' +
                        '                                        <li>' +
                        '                                            <a onclick="addseelater(\''+datas[i].opp_cat[j].id_opp+'\')">See later</a>' +
                        '                                        </li>' +
                        '                                        <li>' +
                        '                                            <a>Pas intéressé</a>' +
                        '                                        </li>' +
                        '                                        <li>' +
                        '                                            <a>Signaler</a>' +
                        '                                        </li>' +
                        '                                    </ul>' +
                        '                                </div>')
                    }
                }
            } 
        }
        $('#fseemore').html('<button class="btn btn-deep-purple col-10 m-auto font-weight-bold" id="seemore" onclick="loadOthers()">See More</button>');
    },3000);
}

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

function notinterested(id_opp) {
    console.log("ajax pour non intéressé");
}

function signal(id_opp) {
    console.log("ajax pour signaler");
}


