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
