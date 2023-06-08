$(function(){
    $('.card').addClass('shadow-lg');

    var classCircle = 'rounded-circle image-fluid'; //need these classes to make it a circle
    $('#convert').click(function(){
        if($('img').hasClass(classCircle)){
            $('img.card-img-top').removeClass(classCircle);
            $('img.pin').addClass('rounded-start').removeClass('rounded-circle pin');
        }
        else{
            $('img.card-img-top').addClass(classCircle);
            $('img.rounded-start').removeClass('rounded-start').addClass('rounded-circle pin'); 
            //use pin class to spefify later
            //$('img.rounded-start') img has a little conflict: they already have class image-fluid, so we donnot need consider it.
            //$('img.rounded-start') also has class rounded-start, which can not exist simultaniously with class rounded-circle, so we have to remove it at first.
        }
    })
})