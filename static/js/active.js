(function ($) {
    'use strict';

    // Welcome Slider Active Code
    if ($.fn.owlCarousel) {
        $(".welcome_slides").owlCarousel({
            items: 1,
            margin: 0,
            loop: true,
            nav: false,
            dots: true,
            autoplay: true,
            autoplayTimeout: 5000,
            smartSpeed: 800,
            autoplayHoverPause: false
        });
    }

    var wel_slides = $('.welcome_slides');
    wel_slides.owlCarousel();
    wel_slides.on('translate.owl.carousel', function (event) {
        $('.owl-item .single_slide .welcome_slide_text .table .table_cell p, .owl-item .single_slide .welcome_slide_text p').removeClass('animated').hide();
        $('.owl-item .single_slide .welcome_slide_text .table .table_cell h2, .owl-item .single_slide .welcome_slide_text h2').removeClass('animated').hide();
        $('.owl-item .single_slide .welcome_slide_text .table .table_cell h4, .owl-item .single_slide .welcome_slide_text h4').removeClass('animated').hide();
        $('.owl-item .single_slide .welcome_slide_text .table .table_cell .btn, .owl-item .single_slide .welcome_slide_text .btn').removeClass('animated').hide();
        $('.owl-item .single_slide .welcome_slide_image .discount_badge').removeClass('animated').hide();
    })
    wel_slides.on('translated.owl.carousel', function (event) {
        $('.owl-item.active .single_slide .welcome_slide_text .table .table_cell p, .owl-item.active .single_slide .welcome_slide_text p').addClass('animated fadeIn').show();
        $('.owl-item.active .single_slide .welcome_slide_text .table .table_cell h2, .owl-item.active .single_slide .welcome_slide_text h2').addClass('animated fadeIn').show();
        $('.owl-item.active .single_slide .welcome_slide_text .table .table_cell h4, .owl-item.active .single_slide .welcome_slide_text h4').addClass('animated fadeIn').show();
        $('.owl-item.active .single_slide .welcome_slide_text .table .table_cell .btn, .owl-item.active .single_slide .welcome_slide_text .btn').addClass('animated fadeInUp').show();
        $('.owl-item .single_slide .welcome_slide_image .discount_badge').addClass('animated bounceInDown').show();
    })

    if ($.fn.owlCarousel) {
        $(".new_arrivals_slides, .you_make_like_slider").owlCarousel({
            items: 4,
            margin: 30,
            loop: true,
            nav: true,
            navText: ['<i class="fa fa-angle-left" aria-hidden="true"></i>', '<i class="fa fa-angle-right" aria-hidden="true"></i>'],
            dots: false,
            autoplay: true,
            smartSpeed: 1500,
            autoplayTimeout: 7000,
            autoplayHoverPause: true,
            responsive: {
                320: {
                    items: 1
                },
                576: {
                    items: 2
                },
                992: {
                    items: 3
                },
                1200: {
                    items: 4
                }
            }
        });
        $(".featured_product_slides").owlCarousel({
            items: 2,
            margin: 30,
            loop: true,
            nav: true,
            navText: ['<i class="fa fa-angle-left" aria-hidden="true"></i>', '<i class="fa fa-angle-right" aria-hidden="true"></i>'],
            dots: false,
            autoplay: true,
            smartSpeed: 1500,
            autoplayTimeout: 7000,
            autoplayHoverPause: true,
            responsive: {
                0: {
                    items: 1
                },
                576: {
                    items: 2
                }
            }
        });
        $(".popular_items_slides").owlCarousel({
            items: 4,
            margin: 30,
            loop: true,
            nav: false,
            dots: false,
            autoplay: true,
            smartSpeed: 1500,
            autoplayTimeout: 7000,
            autoplayHoverPause: true,
            responsive: {
                0: {
                    items: 1
                },
                768: {
                    items: 3
                },
                992: {
                    items: 4
                }
            }
        });
        $(".popular_brands_slide").owlCarousel({
            items: 6,
            margin: 30,
            loop: true,
            nav: false,
            dots: false,
            center: false,
            autoplay: true,
            smartSpeed: 800,
            responsive: {
                0: {
                    items: 2
                },
                480: {
                    items: 3
                },
                768: {
                    items: 4
                },
                992: {
                    items: 6
                }
            }
        });
        $(".testimonials_slides").owlCarousel({
            items: 1,
            margin: 0,
            loop: true,
            dots: true,
            autoplay: true,
            smartSpeed: 1200
        });
    }

    // Navigation Active Code
    if ($.fn.navigation) {
        $("#navigation1").navigation();
    }

    // Magnific-popup Video Active Code
    if ($.fn.magnificPopup) {
        $('.video_btn').magnificPopup({
            disableOn: 0,
            type: 'iframe',
            mainClass: 'mfp-fade',
            removalDelay: 160,
            preloader: true,
            fixedContentPos: false
        });
        $('.gallery_img').magnificPopup({
            type: 'image',
            gallery: {
                enabled: true
            }
        });
        $('.size_guide_img').magnificPopup({
            type: 'image',
            gallery: {
                enabled: true
            }
        });
    }

    // ScrollUp Active Code
    if ($.fn.scrollUp) {
        $.scrollUp({
            scrollSpeed: 1000,
            easingType: 'easeInOutQuart',
            scrollText: '<i class="pe-7s-angle-up" aria-hidden="true"></i>'
        });
    }

    // Counterup Active Code
    if ($.fn.counterUp) {
        $('.counter').counterUp({
            delay: 10,
            time: 2000
        });
    }

    // Countdown Active Code
    $('[data-countdown]').each(function () {
        var $this = $(this),
            finalDate = $(this).data('countdown');
        $this.countdown(finalDate, function (event) {
            $(this).find(".days").html(event.strftime("%D"));
            $(this).find(".hours").html(event.strftime("%H"));
            $(this).find(".minutes").html(event.strftime("%M"));
            $(this).find(".seconds").html(event.strftime("%S"));
        });
    });

    // Masonary Gallery Active Code
    $('.gallery_full_width_images_area, .portfolio-column, .blog-masonary').imagesLoaded(function () {
        // filter items on button click
        $('.portfolio-menu').on('click', 'button', function () {
            var filterValue = $(this).attr('data-filter');
            $grid.isotope({
                filter: filterValue
            });
        });
        // init Isotope
        var $grid = $('.gallery_full_width_images_area, .portfolio-column, .blog-masonary').isotope({
            itemSelector: '.single_gallery_item, .column_single_gallery_item, .sb_masonary_item',
            percentPosition: true,
            masonry: {
                columnWidth: '.single_gallery_item, .column_single_gallery_item, .sb_masonary_item'
            }
        });
    });

    // Jarallax active js
    if ($.fn.jarallax) {
        $('.jarallax').jarallax({
            speed: 0.2
        });
    }

    $(function () {
        $('[data-toggle="popover"]').popover({
            html: true,
            trigger: 'hover',
            content: function () {
                return '<img src="' + $(this).data('img') + '" />';
            }
        })
    })

    // YouTube Video Active Code
    if ($.fn.mb_YTPlayer) {
        $('.player').mb_YTPlayer();
    }

    // MatchHeight Active Code
    if ($.fn.matchHeight) {
        $('.item').matchHeight();
    }

    $('.slider-range-price').each(function () {
        var min = jQuery(this).data('min');
        var max = jQuery(this).data('max');
        var unit = jQuery(this).data('unit');
        var value_min = jQuery(this).data('value-min');
        var value_max = jQuery(this).data('value-max');
        var label_result = jQuery(this).data('label-result');
        var t = $(this);
        $(this).slider({
            range: true,
            min: min,
            max: max,
            values: [value_min, value_max],
            slide: function (event, ui) {
                var result = label_result + " " + unit + ui.values[0] + ' - ' + unit + ui.values[1];
                console.log(t);
                t.closest('.slider-range').find('.range-price').html(result);
            }
        });
    })

    // PreventDefault a Click
    $("a[href='#']").on('click', function ($) {
        $.preventDefault();
    });

    var $window = $(window);

    // Sticky Active Code
    $window.on('scroll', function () {
        if ($window.scrollTop() > 200) {
            $('.header_area').addClass('sticky');
            $('.header_area .sticky .mainmenu_area').fadeIn('slow');
        } else {
           $('.header_area').removeClass('sticky');
            $('.header_area .sticky .mainmenu_area').fadeOut('slow');
        }
    });

    // Fullscreen Active Code
    $window.on('resizeEnd', function () {
        $(".full_height").height($window.height());
    });

    $window.on('resize', function () {
        if (this.resizeTO) clearTimeout(this.resizeTO);
        this.resizeTO = setTimeout(function () {
            $(this).trigger('resizeEnd');
        }, 300);
    }).trigger("resize");

    // wow Active Code
    if ($window.width() > 767) {
        new WOW().init();
    }

})(jQuery);