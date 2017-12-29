$(document).ready(function(){

    var update_cart = {
        'qty': {},
        'remove': []
    }

    $('input.qty-text').bind('input', function(event){
        var item_id = $(this).attr('data-id');
        var qty = $(this).val();
        update_cart['qty'][item_id] = qty;
        var unit_price = parseFloat($('tr#item_'+item_id+' .price .number').text());
        //update item total price
        $('tr#item_'+item_id+' .total_price .number').text((unit_price*qty).toFixed(2))
        //update total price
        refresh_total_price()
    })

    $('a.remove_item').click(function(e){
        e.preventDefault();
        var item_id = $(this).attr('data-id');
        update_cart['remove'].push(item_id);
        $('tr#item_'+item_id).remove();
        refresh_total_price();
    })

    $('.cart-footer a.update_cart').click(function(e){
        e.preventDefault();
        $.post($(this).attr('data-url'), function(data){
            if (data['result'] == true) {
                location.reload()
            } else {
                alert(data['result'])
            }
        })
    })

    function refresh_total_price() {
        var all_rows_totals = $('.total_price .number');
        var new_total = 0;
        $.each(all_rows_totals, function(k, row_tot){
            new_total += parseFloat($(row_tot).text());
        })
        $('tr#total .number').text(new_total.toFixed(2));
    }
})
