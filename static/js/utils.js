var ajax_object = {
    'ajax_calls': {},
    'retrieve': function(url, done, before, after, fail) {
        var self = this;
        if (!self.ajax_calls[url]) {
            if (Boolean(before)) {
                before();
            }
            self.ajax_calls[url] = $.get(url, done)
            if (Boolean(after)) {
                self.ajax_calls[url].done(after);
            }
            if (Boolean(fail)) {
                self.ajax_calls[url].fail(fail);
            }
        } else {
            if (before) {
                before();
            }
            self.ajax_calls[url].then(after);
        }
    }
}

var alert_box = {
//    '__default_classes': 'alert alert-dismissible fade ',
    'show_message': function(alert_box_id, alert_type, message, loading=false) {
        var self = this;
        var alert_container = $(alert_box_id);
        alert_container.template({'alert_text': message}, '#alert-template');
        if (loading) {
            var loader = $('#spinner-holder').html();
            alert_container.find('.alert')
                .append(loader)
                .addClass(alert_type)
                .addClass('show')
        }
        alert_container.find('.alert')
            .addClass(alert_type)
            .addClass('show')
    },
    'hide': function(alert_box_id) {
        $(alert_box_id).find('.alert').alert('close');
    }
}

var cart = {
    'add_product': function(url, formDataObj, before, success, complete) {
        before();
        $.ajax({
            method: 'POST',
            url: url,
            dataType: 'json',
            contentType: false,
            processData: false,
            data: formDataObj,
            success: success,
            complete: complete
        })
    },
    'get_cart_content': function(before, success){
        before()
        $.get('/cart/retrieve', success)
    },
    'refresh': function(){
        var self = this
        self.get_cart_content(function(){
            $('header .cart').empty();
            $('header .cart').append($('<ul class="cart-list animated fadeInUp">Please wait </ul>').append($('#spinner-holder').html()));
        }, function(data) {
            var products = $('<ul></ul>');
            data['total_qty'] === 0 ? $('header .cart').hide() : $('header .cart').show();
            $.each(data['items'], function(key, item) {
                products.template(item, '#top_cart_product', true)
            })
            $('header .cart')
                .template({
                    'products': products.html(),
                    'total': data['total'],
                    'total_qty': data['total_qty'],
                }, '#top_cart');

            //add remove listeners
            $('header .dropdown-product-remove a').click(function(e){
                e.preventDefault();
                cart.remove_item($(this).attr('data-id'));
            })
        })
    },
    'remove_item': function(id){
        var self = this
        $.get('/cart/remove/'+id, function(data){
            self.refresh();
        })
    }
}
