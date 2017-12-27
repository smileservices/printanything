var ajax_object = {
    'ajax_calls': {},
    'retrieve': function(url, done, before=null, after=null, fail=null) {
        var self = this;
        if (!self.ajax_calls[url]) {
            if (before) {
                before();
            }
            self.ajax_calls[url] = $.get(url, done)
            if (after) {
                self.ajax_calls[url].done(after);
            }
            if (fail) {
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

var cart = {
    'add_product': function(url, csrf, product_data, before, success, complete) {
        before();
        $.ajax({
            'method': 'POST',
            'url': url,
            'dataType': 'json',
            'data': {
                'csrfmiddlewaretoken': csrf,
                'product_id': product_data['product_id'],
                'stock': product_data['stock'],
                'qty': product_data['qty']
            },
            'success': success,
            'complete': complete,
        })
    },
    'retrieve_cart': function(){
    }
}
