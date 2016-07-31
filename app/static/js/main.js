$(".alert").delay(2500).fadeOut(500, function() {
    $(this).alert('close');
});


$('ul.CollapsibleList li').on('click', function () {
    $(this).siblings('ul').toggle(); // Hides sister ULs
    $(this).toggleClass("open closed"); // Togles class of li
});


$( document ).ready(function() {
    // $('ul.CollapsibleList li').addClass('closed'); // Adds closed to all
    $('ul.CollapsibleList ul:not(:has(> ul))').children('li').addClass('childless'); // Adds closed to all

    $('#menu-loading').animate({opacity: 0},250);
    $('#menu-loading').remove();

    $('ul.CollapsibleList').animate({opacity: 1},1000);

});
