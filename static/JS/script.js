$(document).ready(function () {

    $('.js-product-quantity').each(function (_, item) {
        const numbers = $(item).html().split('.');
        if (numbers[1] && numbers[1] === '0') {
            $(item).html(numbers[0]);
        }
    });

    function updateQuantityHandler(elem, type = 'inc') {
        const input = $(elem).parent().find('.product-quantity');
        const v = parseFloat(input.val());
        const q = parseFloat(input.data('change-size'));
        const a = parseFloat(input.data('min-order-qty'));
        if (type === 'inc') {
            input.val(v + q);
        } else {
            // input.val(v - q <= q ? q : v - q);
            input.val(v - q <= a ? a : v - q);
        }
    }

    $('.js-btn-inc').on('click', function () {
        updateQuantityHandler(this)
    }).each(function (_, item) {
        updateQuantityHandler(item);
    });

    $('.js-btn-dec').on('click', function () {
        updateQuantityHandler(this, 'dec')
    }).each(function (_, item) {
        updateQuantityHandler(item, 'dec');
    });

    // $('.js-btn-inc').on('click', function () {
    //     const input = $(this).parent().find('.product-quantity');
    //     input.val(parseFloat(`${input.val()}`.replaceAll(',', '.')))
    //     let q = parseFloat(`${input.data('change-size')}`.replaceAll(',', '.'))
    //     input.val(+input.val() + q);
    // });
    //
    // $('.js-btn-dec').on('click', function () {
    //     const input = $(this).parent().find('.product-quantity');
    //     input.val(parseFloat(`${input.val()}`.replaceAll(',', '.')))
    //     let q = parseFloat(`${input.data('change-size')}`.replaceAll(',', '.'))
    //     let minWeight = q
    //     // if (+input.val() <= q) return
    //     // q = +input.val() <= q ? q : +input.val()-q
    //     if(+input.val() > minWeight ) {
    //         q = +input.val() - q
    //     } else {
    //         return
    //     }
    //     // q = +input.val() + q <= q ? q : +input.val() - q
    //     // console.log(q)
    //     // input.val(+input.val() - q);
    //     input.val(q)
    // });


    // $('.js-btn-inc').on('click', function () {
    //     const input = $(this).parent().find('.product-quantity');
    //     let q = parseFloat(input.data('change-size'));
    //     input.val(+input.val() + q);
    // });
    //
    // $('.js-btn-dec').on('click', function () {
    //     const input = $(this).parent().find('.product-quantity');
    //     let q = parseFloat(input.data('change-size'));
    //     q = +input.val() - q <= q ? q : +input.val() - q
    //     input.val(q)
    // });

    // registration & login
    $('.sign-in-register-block .sign-in').on('click', function () {
        $(this).addClass('site-color');
        $('.sign-in-register-block .register').removeClass('site-color');
        $('.login-form').removeClass('d-none');
        $('.register-form').addClass('d-none');
    })
    $('.sign-in-register-block .register').on('click', function () {
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

    $(window).resize(function () {
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
function updateflags(id) {
    $('.flags .flag').removeClass('display')
    $('#' + id).addClass('display')
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
    localStorage.setItem('lang', currentLanguage);
}

updateLanguage();


