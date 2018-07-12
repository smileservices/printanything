$(document).ready(function(){

    var update_cart = {
        'qty': {},
        'shipping': {},
        'remove': []
    };


    // change price when modifyig qty
    $('input.qty-text').bind('input', function(event){
        var item_id = $(this).attr('data-id');
        var qty = $(this).val();
        update_cart['qty'][item_id] = qty;
        var unit_price = parseFloat($('tr#item_'+item_id+' .price .number').text());
        //update item total price
        $('tr#item_'+item_id+' .total_price .number').text((unit_price*qty).toFixed(2))
        //update total price
        refresh_total_price()
    });

    //remove item
    $('a.remove_item').click(function(e){
        e.preventDefault();
        var item_id = $(this).attr('data-id');
        var vendor_id = $(this).attr('data-vendor');
        update_cart['remove'].push(item_id);
        $('tr#item_'+item_id).remove();
        //check if only item from vendor and remove if so
        if ($('tr[data-vendor="'+vendor_id+'"]').length === 0) {
            $('tr[data-shipping="'+vendor_id+'"]').remove();
        }
        refresh_total_price();
    });

    $('#update_cart').click(function(e){
        e.preventDefault();
        var self = this;
        alert_box.hide();
        alert_box.show_message('#cart_alert_box', 'alert-info', 'Updating cart, please wait ...', true)
        $.post($(self).attr('data-update-url'), {
                'qty': JSON.stringify(update_cart['qty']),
                'shipping': JSON.stringify(update_cart['shipping']),
                'remove': JSON.stringify(update_cart['remove']),
                'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val()
        }, function(data){
            //show result
            alert_box.hide()
            alert_box.show_message('#cart_alert_box', 'alert-info', data['result'])
            cart.refresh();
            window.location.replace($(self).attr('href'));
        })
    });

    $('input.shipping[type="radio"]').change(function(){
        refresh_total_price();
    });

    function refresh_total_price() {
        var all_rows_totals = $('.total_price .number');
        var new_total = 0;
        $.each(all_rows_totals, function(k, row_tot){
            new_total += parseFloat($(row_tot).text());
        });
        //update shipping info
        update_cart['shipping'] = {};
        var all_shipping = $('input.shipping[type="radio"]:checked');
        $.each(all_shipping, function(k, item){
            new_total += parseFloat($(item).attr('data-cost'));
            update_cart['shipping'][$(item).attr('data-vendor')] = $(item).val();
        });
        $('tr#total .number').text(new_total.toFixed(2));
    }

    refresh_total_price();

})
