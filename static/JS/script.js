$(document).ready(function () {

    $('.js-btn-inc').on('click', function () {
        const input = $(this).parent().find('.product-quantity');
        input.val(parseFloat(`${input.val()}`.replaceAll(',', '.')))
        let q = parseFloat(`${input.data('change-size')}`.replaceAll(',', '.'))
        input.val(+input.val() + q);
    });

    $('.js-btn-dec').on('click', function () {
        const input = $(this).parent().find('.product-quantity');
        input.val(parseFloat(`${input.val()}`.replaceAll(',', '.')))
        let q = parseFloat(`${input.data('change-size')}`.replaceAll(',', '.'))
        if (+input.val() === q) return
        input.val(+input.val() - q);
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

    if (span) {

        span.onclick = function () {
            modal.style.display = "none";
        }
    }

});

// languages
// $('#page-language-select').select2();
$('#page-language-select').on('change', function () {
    $(this).parents('form').submit();
});

// Language dropdown
function updateflags(id)  {
    $('.flags .flag').removeClass('display')
    $('#'+id).addClass('display')
}

const onLanguageChange = (event) => {
    localStorage.setItem('lang', event.target.value);
};

$('#page-language-select').on('change', onLanguageChange)

function updateLanguage() {
    const currentLanguage = $('#page-language-select').val()
    const lang = localStorage.getItem('lang');
    $('#page-language-select').val(lang || currentLanguage)
    updateflags(lang || currentLanguage)
    localStorage.setItem('lang', 'hy');
}

updateLanguage();
