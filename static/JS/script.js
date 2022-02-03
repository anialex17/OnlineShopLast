$(document).ready(function () {
    $('.js-btn-inc').on('click', function () {
        const input = $(this).parent().find('.product-quantity');
        const q = +input.data('change-size');
        input.val(+input.val() + q);
    });

    $('.js-btn-dec').on('click', function () {
        const input = $(this).parent().find('.product-quantity');
        const q = +input.data('change-size');
        const v = +input.val();
        const val = v - q < q ? q : v - q;
        input.val(val);
    });

    // languages
    // $('#page-language-select').select2();
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

    // Footer fixed bottom
    const footer = $('.footer');
    fixedBottom();

    function fixedBottom(elHeight = 0) {
        if ($("html").height() < $(window).height() - elHeight) {
            footer.addClass('fixed-bottom');
        } else {
            footer.removeClass('fixed-bottom');
        }
    }

    $(window).resize(function() {
        fixedBottom();
    });

    // Gallery modal

    let modal = document.getElementById("galModal");
    let i;
    let search = document.getElementsByClassName("gallsearch");

    let picdiv = document.querySelectorAll(".picdiv");
    let img = document.getElementsByClassName("gallpic");
    let modalImg = document.getElementById("img01");

    picdiv.forEach((el, i) => {
        el.addEventListener('click', () => {
            modal.style.display = "block";
            modalImg.src = el.querySelector('.product-img-btn .img').src;
        })
    })

    let span = document.getElementsByClassName("modalclose")[0];

    span.onclick = function() {
        modal.style.display = "none";
    }

});

// Language dropdown

let currentLanguage = 'armenian';

const onLanguageChange = (event) => {
    let newLanguage = event.target.value;

    if (newLanguage !== currentLanguage) {
        let currentLanguageSelector = '.language-dropdown .flag[id="'+ currentLanguage +'"]';
        let newLanguageSelector = '.language-dropdown .flag[id="'+ newLanguage +'"]';

        document.querySelector(currentLanguageSelector).classList.remove('display');
        document.querySelector(newLanguageSelector).classList.add('display');
        currentLanguage = newLanguage;
    }
};

document
    .querySelector('.language-dropdown select')
    .addEventListener('change', onLanguageChange);