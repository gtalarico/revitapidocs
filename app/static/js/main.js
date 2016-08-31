$(".alert").delay(8000).fadeOut(300, function() {
    $(this).alert('close');
});

// OLD MENU JS
// $('ul.CollapsibleList li').on('click', function () {
//     $(this).siblings('ul').toggle(); // Hides sister ULs
//     $(this).toggleClass("open closed"); // Togles class of li
// });
//
//
// $( document ).ready(function() {
//     $('ul.CollapsibleList ul:not(:has(> ul))').children('li').addClass('childless'); // Adds closed to all
//
//     $('#menu-loading').animate({opacity: 0},250);
//     $('#menu-loading').remove();
//
//     $('ul.CollapsibleList').animate({opacity: 1},500);
//
// });
