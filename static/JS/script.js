$(document).ready(function () {
    // languages
    $('#page-language-select').on('change', function () {
        $(this).parents('form').submit();
    });

    // registration & login
    $('.sign-in-register-block .sign-in').on('click', function (){
        $(this).addClass('site-color');
        $('.sign-in-register-block .register').removeClass('site-color');
        $('.login-form').removeClass('d-none');
        $('.register-form').addClass('d-none');
    })
    $('.sign-in-register-block .register').on('click', function (){
        $(this).addClass('site-color');
        $('.sign-in-register-block .sign-in').removeClass('site-color');
        $('.register-form').removeClass('d-none');
        $('.login-form').addClass('d-none');
    });
})

