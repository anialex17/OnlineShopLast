$(document).ready(function () {
    const gallery_column = document.querySelectorAll('.gallery-content .col-sm-4');
    const gallery_btn = document.querySelectorAll('.gallery-content .product-img-btn');
    const gallery_img = document.querySelectorAll('.gallery-content .product-img-btn img');
    const gallery_search_plus = document.querySelectorAll('.gallery-content .product-img-btn .search-plus');

    let transform_x = 0 + 'px';
    let transform_y = 0 + 'px';

    function getScrollBarWidth() {
        let outer = $('<div>').css({visibility: 'hidden', width: 100, overflow: 'scroll'}).appendTo('body');
        let widthWithScroll = $('<div>').css({width: '100%'}).appendTo(outer).outerWidth();
        outer.remove();
        return (100 - widthWithScroll);
    }

    function transformCount(coefficient_x = 0, coefficient_y = 1, gallery_img_width = 500) {
        transform_x = ((($('.container').width() - gallery_img_width) / 2) * coefficient_x) + 'px';
        transform_y = ($(gallery_img).height() / (-2) * coefficient_y) + 'px';
    }

    $(window).resize(function() {
        transformCount();
    });

    gallery_btn.forEach((el, i) => {
        el.addEventListener('click', () => {
            el.classList.add('bg-transparent');

            $('html body').css({
                'overflow': 'hidden',
                'padding-right': getScrollBarWidth()
            })
            $('.bg-close').addClass('absolute-div');

            gallery_img[i].classList.add('gallery-big-img');

            if ($(el).hasClass('left') && $(window).width() > 576) {
                transformCount(1);
            } else if ($(el).hasClass('right') && $(window).width() > 576) {
                if ($(window).width() < 768) {
                    transformCount(-3.5);
                } else if ($(window).width() < 992) {
                    transformCount(-3);
                } else if ($(window).width() < 1200) {
                    transformCount(-2);
                } else if ($(window).width() > 1200) {
                    transformCount(-1.5);
                } else {
                    transformCount(-2);
                }
            } else if ($(el).hasClass('center') && $(window).width() > 576) {
                if ($(window).width() < 768) {
                    transformCount(-1.75);
                } else if ($(window).width() < 992) {
                    transformCount(-1);
                } else if ($(window).width() < 1200) {
                    transformCount(-0.5);
                } else if ($(window).width() > 1200) {
                    transformCount(-0.25);
                }
            } else if ($(window).width() < 576) {
                transformCount(0, 0.5);
            }

            $(gallery_img).css('transform', `translate(${transform_x}, ${transform_y})`);
            gallery_search_plus[i].classList.add('d-none');
            gallery_column[i].style.zIndex = '1050';

            gallery_img.forEach((el, j) => {
                if (j !== i) {
                    gallery_img[j].classList.remove('gallery-big-img');
                }
            });

            gallery_column.forEach((el, k) => {
                if (k !== i) {
                    gallery_column[k].style.zIndex = '1';
                    gallery_img[k].style.transform = 'translate(0%, 0%)';
                }
            });

            $('.btn-close').css('display', 'block');
        })
    })

    $('.btn-close').on('click', () => {
        $('.bg-close').click();
        $('.btn-close').css('display', 'none');
    });

    $('.bg-close').on('click', () => {
        gallery_img.forEach((el, j) => {
            gallery_img[j].classList.remove('gallery-big-img');
        });

        gallery_column.forEach((el, k) => {
            gallery_column[k].style.zIndex = '1'
            gallery_img[k].style.transform = 'translate(0%, 0%)'
        });

        $('.bg-close').removeClass('absolute-div');
        $('.btn-close').css('display', 'none');
        $('html body').css({
            'overflow': 'visible',
            'padding-right': '0'
        })

        gallery_btn.forEach((el, i) => {
            el.classList.remove('bg-transparent');
        })
    })

})
