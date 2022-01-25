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
    };

    // Language dropdown

    $(".selectlang").click(function() {
        let is_open = $(this).hasClass("open");
        if (is_open) {
            $(this).removeClass("open");
        } else {
            $(this).addClass("open");
        }
    });

    $(".selectlang li").click(function() {

        let selected_value = $(this).html();
        let first_li = $(".selectlang li:first-child").html();

        $(".selectlang li:first-child").html(selected_value);
        $(this).html(first_li);

    });

    $(document).mouseup(function(event) {

        let target = event.target;
        let selectlang = $(".selectlang");

        if (!selectlang.is(target) && selectlang.has(target).length === 0) {
            selectlang.removeClass("open");
        }

    });


})

