$(".alert").delay(2500).fadeOut(500, function() {
    $(this).alert('close');
});

// $('li').click(function() {
//         // $(this).parent().find('ul').toggle();
//         // $(this).children().find('ul').toggle();
//
//         console.log($(this).find('ul'));
//     });

$('ul.CollapsibleList li').on('click', function () {
    $(this).siblings('ul').toggle();
    $(this).toggleClass("open closed");
    console.log('clicked');
});


$( document ).ready(function() {
    $('ul.CollapsibleList li').addClass('closed');
    $('ul.CollapsibleList').animate({opacity: 1},1000);
    $('span.loading').animate({opacity: 0},250);

    $('ul.CollapsibleList > ul').toggle();
    $('ul.CollapsibleList > ul').toggleClass("open closed");
    // $('li:not(:has(ul))').addClass('closed');
});
