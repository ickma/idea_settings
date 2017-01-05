$(document).ready(function () {
    $('table').attr('position', 'relactive');
    var imgs = $('.hover_zoom_img');
    var handle_in = function () {
        var url = $(this).find('img').attr('src')

        var img_html = $('<img class="zoom" src="' + url + '">');
        $(this).find('img').after(img_html);


    }
    var handle_out = function () {
        $(this).find('img.zoom').remove();

    }
    imgs.each(function () {
        $(this).hover(handle_in, handle_out);
    })

})

