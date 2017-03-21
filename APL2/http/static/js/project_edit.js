$(function () {
    $(window).on('load', function () {
        if ($('.container-fluid').height() > $(window).height()) {
            var w = $('.container-fluid').width();
            var h = $('.container-fluid').height();
            $('.mark').width(w);
            $('.mark').height(h);
        } else {
            var w = $(window).width();
            var h = $(window).height();
            $('.mark').width(w);
            $('.mark').height(h);
        }
    })
    $(window).on('resize', function () {
        if ($('.container-fluid').height() > $(window).height()) {
            var w = $('.container-fluid').width();
            var h = $('.container-fluid').height();
            $('.mark').width(w);
            $('.mark').height(h);
        } else {
            var w = $(window).width();
            var h = $(window).height();
            $('.mark').width(w);
            $('.mark').height(h);
        }
    })
    $('.things').on('click', function () {
        $('.mark').show();
        var h = $('.tck').height() / 2;
        $('.tck').css('marginTop', -h + 'px');
        var uid = $(this).attr('data_id');
        $('#' + uid).show();

    })
    $('.close').on('click', function () {
        var num = $(this).attr('data_id');
        $('.mark').hide();
        $('#' + num).hide();
    })
})
