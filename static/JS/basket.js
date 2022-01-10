$(document).ready(function () {
    const dec_btn = $('.product-content .btn-dec');
    const inc_btn = $('.product-content .btn-inc');
    const input = $('.product-content .add-to-basket-block input');
    const basket_dec_btn = $('.basket-content .btn-dec');
    const basket_inc_btn = $('.basket-content .btn-inc');
    const basket_input = $('.basket-content .add-to-basket-block input');
    const delete_btn = $('.basket-content .delete-btn');
    const add_to_basket = $('.product-content .add-to-basket-btn');
    const food_name = $('.product-content .food-info #food-name');
    const food_price = $('.product-content .food-info #food-price');
    const INPUT_MIN = 1;
    const INPUT_MAX = 99;
    let basket = {
        food_info: []
    }

    function saveInLocalStorage(myObject) {
        if (JSON.parse(localStorage.getItem('Ecommerce_Basket'))) {
            basket = (JSON.parse(localStorage.getItem('Ecommerce_Basket')));
            let it = 0;

            for (let food of basket.food_info) {
                if (food.foodName === myObject.foodName) {
                    basket.food_info[it] = myObject;
                    break;
                } else if (it === basket.food_info.length - 1) {
                    basket.food_info.push(myObject);
                }
                it++;
            }

        } else {
            basket.food_info.push(myObject);
        }

        let serialObj = JSON.stringify(basket);
        localStorage.setItem('Ecommerce_Basket', serialObj);
    }

    function deleteFromLocalStorage(i) {
        let dataOfStrorage = getFromLocalStorage().food_info;
        localStorage.removeItem('Ecommerce_Basket');
        delete dataOfStrorage[i];

        dataOfStrorage.forEach((el) => {
            const myObject = {
                foodName: el.foodName,
                foodQuantity: el.foodQuantity,
                foodPrice: el.foodPrice,
                totalPrice: el.totalPrice
            }
            saveInLocalStorage(myObject);
        })

        is_basket_empty();
        document.location.reload();
    }

    function inputHandler() {
        let number = '';
        for (const letter of this.value) {
            if ('0123456789'.includes(letter)) {
                number += letter;
            }
        }

        number = parseInt(number);
        number = keep_range(number);
        this.value = number;
    }

    function keep_range(digit) {
        if (digit < INPUT_MIN || isNaN(digit)) {
            digit = INPUT_MIN;
        } else if (digit > INPUT_MAX){
            digit = INPUT_MAX;
        }
        return digit;
    }

    function dec_inc(input_field, i, sign) {
        let input_value = parseInt(input_field[i].value);
        input_value += sign;
        input_value = keep_range(input_value);
        input_field[i].value = input_value;
    }

    function changeQuantity(i) {
        const foodName = $('table td .food-name')[i].innerText;
        const foodPrice = parseInt($('table td .food-price')[i].innerText);
        const foodQuantity = parseInt($('table .quantity input')[i].value);
        $('table td .total-price')[i].innerText = foodPrice * foodQuantity;
        const totalPrice = parseInt($('table td .total-price')[i].innerText);

        const myObject = {
            foodName,
            foodQuantity,
            foodPrice,
            totalPrice
        }

        saveInLocalStorage(myObject);
    }

    function is_basket_empty() {
        if ($('.table tbody').children().length === 0) {
            $('.table').addClass('d-none');
            $('.basket-content .header-block').append('<h3 class="site-color py-5">Your Basket is Empty!</h3>');
            return true;
        }
        return false;
    }

    function count_total_price() {
        const shipping_price = 2000;
        $('.basket-content .shipping-price .price')[0].innerText = shipping_price;
        const all_prod_price = $('.basket-content .products-price .products-total-price');
        const totalPrices = $('table td .total-price');
        let total = 0;

        $(totalPrices).each((l) => {
            total += parseInt($('table td .total-price')[l].innerText);
        });

        if (total === 0) {
            total -= shipping_price;
        }

        try {
            $(all_prod_price)[0].innerText = total + shipping_price;
        } catch (e) {
            e.message;
        }
    }

    function quantity_in_basket() {
        const product_quantity = getFromLocalStorage().food_info
        const navbar_product_quantity = $('.navbar .product-quantity')

        if (product_quantity !== undefined && product_quantity !== null) {
            $(navbar_product_quantity)[0].innerText = $(product_quantity).length;
            $(navbar_product_quantity).removeClass('d-none')
        } else {
            $(navbar_product_quantity)[0].innerText = '0';
            $(navbar_product_quantity).addClass('d-none')
        }
    }

    try {
        count_total_price();
    } catch (e) {
        e.message;
    }

    quantity_in_basket();
    is_basket_empty();
    $(input).on('input', inputHandler);
    $(basket_input).on('input', inputHandler);
    $(basket_input).each((i, el) => {
        $(el).on('input', () => {
            changeQuantity(i);
            count_total_price();
            document.location.reload();
        })
    });

    $(dec_btn).each((i, el) => {
        $(el).on('click', () => {
            dec_inc(input, i, -1);
        })
    })

    $(inc_btn).each((i, el) => {
        $(el).on('click', () => {
            dec_inc(input, i, 1);
        })
    })

    $(add_to_basket).on('click', () => {
        const foodQuantity = parseInt($(input).val());
        const foodName = $(food_name)[0].innerText;
        const foodPrice = parseInt($(food_price)[0].innerText);
        const totalPrice = foodPrice * foodQuantity;

        const myObject = {
            foodName,
            foodQuantity,
            foodPrice,
            totalPrice
        }

        saveInLocalStorage(myObject);
        quantity_in_basket();
    })

    $(basket_dec_btn).each((i, el) => {
        $(el).on('click', () => {
            dec_inc(basket_input, i, -1);
            changeQuantity(i);
            count_total_price();
            document.location.reload();
        })
    })

    $(basket_inc_btn).each((i, el) => {
        $(el).on('click', () => {
            dec_inc(basket_input, i, 1);
            changeQuantity(i);
            count_total_price();
            document.location.reload();
        })
    })

    $(delete_btn).each((i, el) => {
        $(el).on('click', () => {
            deleteFromLocalStorage(i)
        })
    })

})

function getFromLocalStorage() {
    if (JSON.parse(localStorage.getItem('Ecommerce_Basket'))) {
        return (JSON.parse(localStorage.getItem('Ecommerce_Basket')));
    }
    return false;
}

const storageData = getFromLocalStorage();
const basket_table = $('.basket-content .table tbody');

$(storageData.food_info).each((i, el) => {
    $(basket_table).append(
        `<tr class="py-3">
            <th scope="row">
                <div class="basket-img">
                    <img src="Images/home/food_1.jpg" alt="product" class="img">
                </div>
            </th>
            <td class="font-weight-bold">
                <span class="d-sm-none">Product name</span>
                <a href="./product.html" class="site-color food-name">${el.foodName}</a>
            </td>
            <td>
                <span class="d-sm-none font-weight-bold">Food Price</span>
                <span class="food-price">${el.foodPrice}</span>
                <span> դր</span>
            </td>
            <td class="quantity">
                <span class="d-sm-none font-weight-bold">Product Quantity</span>
                <div class="d-flex add-to-basket-block">
                    <button class="btn shadow-none btn-dec flex-center mr-2 border-0 btn-dec">
                        <i class="fas fa-minus site-color"></i>
                    </button>
                    <input type="text" value="${el.foodQuantity}" class="mr-2">
                    <button class="btn shadow-none btn-inc flex-center mr-2 border-0 btn-inc">
                        <i class="fas fa-plus site-color"></i>
                    </button>
                </div>
            </td>
            <td>
                <span class="d-sm-none font-weight-bold">Total Price</span>
                <span class="total-price">${el.totalPrice}</span>
                <span> դր</span>
            </td>
            <td>
                <span class="d-sm-none font-weight-bold">Delete</span>
                <button class="bg-transparent border-0 site-color delete-btn">
                    <i class="fas fa-times"></i>
                </button>
            </td>
        </tr>`
    )
});
