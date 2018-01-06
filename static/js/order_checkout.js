$(document).ready(function(){
    var csrfmiddlewaretoken = $('input[name="csrfmiddlewaretoken"]').val()
    var customer_req = false

    //set up shipping cost
//    $('.checkout_details_area .alert td').text('Select shipping option!');
    var default_shipping_cost = $('.checkout_details_area .shipping input[name="shipping"]:checked').attr('data-price');
    change_shipping(parseFloat(default_shipping_cost));

    $('.checkout_details_area .shipping input[name="shipping"]').change(function(){
        var ship_price = parseFloat($(this).attr('data-price'));
        change_shipping(ship_price);
    })

    function change_shipping(price) {

        var ex_ship_price_str = $('.checkout_summary_area tfoot .shipping .number').text();
        if (ex_ship_price_str === '') {
            var ex_ship_price = 0
        } else {
            var ex_ship_price = parseFloat(ex_ship_price_str);
        }
        var total = parseFloat($('.checkout_summary_area tfoot .total .number').text());
        $('.checkout_summary_area tfoot .shipping .number').text(price);
        $('.checkout_summary_area tfoot .total .number').text(total-ex_ship_price+price);
    }


    //    check for existing email address
//    $('#email_address').on("change keyup paste", function(){
//        var email = $(this).val();
//        if (customer_req) {
//            customer_req.abort()
//        }
//        customer_req = $.post(customer_check_url, {
//            'csrfmiddlewaretoken': csrfmiddlewaretoken,
//            'email': email
//        }, function(data) {
//            console.log(data);
//        })
//    })
})
