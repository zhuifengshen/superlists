// window.Superlists = {};
// window.Superlists.initialize = function () {
//     $('input').on('keypress', function () {
//         $('.has-error').hide();
//     });
// };

// $('input').on('keypress', function () {
//     $('.has-error').hide()
// });

// $(document).ready(function () {
//     $('input').on('keypress', function () {
//         $('.has-error').hide();
//     });
// });

jQuery(document).ready(function ($) {
    $('input[name="text"]').on('keypress', function () {
        $('.has-error').hide();
    });
});