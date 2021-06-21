$(document).ready(function(){
    $("#submit-form-step-3").click(function(){
        $("#div-step-3").animate({
            opacity: '0',
        }, 300, function () {
            $("#div-step-3").css({
                'display' : 'none'
            });
            $("#div-step-4").css({
                'opacity' : '1',
                'display' : 'block'
            });
        });
    });
    $("#back-to-location").click(function(){
        $("#div-step-4").animate({
            opacity: '0',
        }, 300, function () {
            $("#div-step-4").css({
                'display' : 'none'
            });
            $("#div-step-3").css({
                'opacity' : '1',
                'display' : 'block'
            });
        });
    });
});
