// makes sure the whole site is loaded
jQuery(window).load(function() {
    // will first fade out the loading animation
    jQuery(".status").fadeOut();
    // will fade out the whole DIV that covers the website.
    jQuery(".preloader").delay(500).fadeOut("slow");
});

/* wow animation */
wow = new WOW({
    mobile: false
});
wow.init();

// JavaScript Document
jQuery(document).ready(function($) {
    'use strict';

    //jQuery for page scrolling feature - requires jQuery Easing plugin
    $('.page-scroll').on('click', function(event) {
        var $anchor = $(this);
        $('html, body').stop().animate({
            scrollTop: $($anchor.attr('href')).offset().top
        }, 1500, 'easeInOutExpo');
        event.preventDefault();
    });

    // collapsed menu close on click
    $(document).on('click', '.navbar-collapse.in', function(e) {
        if ($(e.target).is('a')) {
            $(this).collapse('hide');
        }
        return false;
    });

    // Scroll Plugin
    $(window).scroll(function() {
        var secondFeature = $('#secondFeature').offset().top;
        var scroll = $(window).scrollTop();
        if (scroll >= 600) {
            $('.sticky-navigation').animate({ "top": '0', "opacity": '1' }, 0);
        } else {
            $('.sticky-navigation').animate({ "top": '-100', "opacity": '0' }, 0);
        }
        if (scroll >= secondFeature - 200) {
            $(".mobileScreen").css({ 'background-position': 'center top' });
        }
        return false;
    });

    /* screenshot slider */
    var owl = $("#owl-carousel-works");
    owl.owlCarousel({
        itemsCustom: [
            [0, 1],
            [450, 2],
            [600, 3],
            [700, 3],
            [1000, 4],
            [1200, 4],
            [1400, 4],
            [1600, 4]
        ],
        navigation: false
    });

    // Nivo Lightbox
    $('#screenshots a').nivoLightbox({
        effect: 'fadeScale'
    });

    // team carousel
    var owl = $("#owl-carousel-team");
    owl.owlCarousel({
        itemsCustom: [
            [0, 1],
            [450, 2],
            [600, 3],
            [700, 3],
            [1000, 4],
            [1200, 4],
            [1400, 4],
            [1600, 4]
        ],
        navigation: false
    });

    // #owl-carousel-testimonials
    $("#owl-carousel-testimonials").owlCarousel({
        autoPlay: 2000,
        stopOnHover: true,
        navigation: false,
        paginationSpeed: 1000,
        goToFirstSpeed: 2000,
        singleItem: true,
        autoHeight: true,
        transitionStyle: "fade"
    });

    // Animated Number
    $('#numbers ul').appear(function() {
        $('#number1').animateNumber({ number: 199 }, 1500);
        $('#number2').animateNumber({ number: 92 }, 1500);
        $('#number3').animateNumber({ number: 54 }, 1500);
        $('#number4').animateNumber({ number: 99 }, 1500);
        $('#number5').animateNumber({ number: 324 }, 1500);
        $('#number6').animateNumber({ number: 45 }, 1500);
    }, { accX: 0, accY: -200 });

    // top video
    //hidden it in mobile
    if (matchMedia('(min-width: 640px)').matches) {
        var videobackground = new $.backgroundVideo($('body'), {
            "align": "centerXY",
            "width": 1280,
            "height": 720,
            "path": "video/",
            "filename": "video",
            "types": ["mp4", "ogg", "webm"]
        });
    }
    // responsive Video
    $(".video-container").fitVids();

}); // end Document.ready

// Contact Form
$(document).on('submit', '#contactForm', function(e) {
    e.preventDefault();
    var name = $("#name").val();
    var email = $("#email").val();
    var message = $("#message").val();
    var dataString = 'name=' + name + '&email=' + email + '&message=' + message;

    function isValidEmail(emailAddress) {
        var pattern = new RegExp(/^((([a-z]|\d|[!#\$%&'\*\+\-\/=\?\^_`{\|}~]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])+(\.([a-z]|\d|[!#\$%&'\*\+\-\/=\?\^_`{\|}~]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])+)*)|((\x22)((((\x20|\x09)*(\x0d\x0a))?(\x20|\x09)+)?(([\x01-\x08\x0b\x0c\x0e-\x1f\x7f]|\x21|[\x23-\x5b]|[\x5d-\x7e]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(\\([\x01-\x09\x0b\x0c\x0d-\x7f]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF]))))*(((\x20|\x09)*(\x0d\x0a))?(\x20|\x09)+)?(\x22)))@((([a-z]|\d|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(([a-z]|\d|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])*([a-z]|\d|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])))\.)+(([a-z]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(([a-z]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])*([a-z]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])))\.?$/i);
        return pattern.test(emailAddress);
    };
    if (isValidEmail(email) && (message.length > 1) && (name.length > 1)) {
        $.ajax({
            type: "POST",
            url: "sendmail.php",
            data: dataString,
            success: function() {
                $('.success').fadeIn(1000);
                $('.error').fadeOut(500);
            }
        });
    } else {
        $('.error').fadeIn(1000);
        $('.success').fadeOut(500);
    }
    return false;
});