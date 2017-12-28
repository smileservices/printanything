$(document).ready(function(){

    var supports = {
        'data_by_id': {},
        'rendered_by_id': {},
        'get_stock_url': function(id) {
            return '/products/get_support/'+id;
        },
        'select_support': function(id) {
            var self = this;
            if (!self.rendered_by_id[id]) {
                var data = self.data_by_id[id];
                var colours_rendered = self.render_colours(data);
                self.sizes_rendered = self.render_sizes(data);
                first_colour = Object.keys(data)[0]
                $('#support_section').template({
                    'colours': colours_rendered,
                    'sizes': self.sizes_rendered[first_colour],
                }, '#sup_sec_tmpl');
                self.rendered_by_id[id] = $('#support_section').html();
            } else {
                $('#support_section').html(self.rendered_by_id[id]);
            }
            //change colours listener
            $('#support_section input[name="colour"]').click(function(){
                var self_elem = $(this);
                $('#support_section input[name="colour"]').removeAttr('checked');
                supports.colour_select(self_elem)
            })
            $('#support_sizes a').click(function(e){
                e.preventDefault();
                self.size_select($(this))
            })
        },
        'render_colours': function(data) {
            var rendered = $('<div id="available_colours"></div>');
            var index = 0;
            $.each(data, function(key, val){
                rendered.template({
                    'colour_lower': key.toLowerCase(),
                    'colour': key,
                    'checked': index == 0 ? 'checked="checked"' : ''
                }, '#sup_sec_tmpl_colours', true)
                index += 1;
            })
            return rendered.html();
        },
        'render_sizes': function(data) {
            var sizes_by_colours = {};
            $.each(data, function(key, sizes){
                var rendered = $('<div id="available_sizes"></div>');
                $.each(sizes, function(key, size){
                    rendered.template({
                        'size': size.size,
                        'size-id': size.id
                    }, '#sup_sec_tmpl_size', true)
                })
                sizes_by_colours[key] = rendered.html();
            })
            return sizes_by_colours;
        },
        'colour_select': function(self_elem) {
            var self = this;
            self_elem.prop("checked",true);
            $('#support_sizes ul').html(self.sizes_rendered[self_elem.val()])
            $('#support_sizes a').click(function(e){
                e.preventDefault();
                self.size_select($(this))
            })
        },
        'size_select': function(self_elem) {
            $('#support_sizes a').removeClass('selected');
            self_elem.addClass('selected');
        },
        'trigger_support_select': function(self_elem) {
            var self = this;
            var support_id = self_elem.attr('data-id');
            ajax_object.retrieve(self.get_stock_url(support_id),
                done=function(data){
                    supports.data_by_id[support_id] = data;},
                before=function() {
                    $('.support-types').removeClass('selected');
                    self_elem.addClass('selected');
                    //show alert
                    alert_box.show_message('#add_to_cart_alert_box', 'alert-primary', 'Retrieving support options', true)
                },
                after=function() {
                    alert_box.hide('#add_to_cart_alert_box');
                    supports.select_support(support_id);
                }
            )
        }
    }

    //initialize first support
    supports.trigger_support_select($('.support-types').first())

    // get support options
    $('.support-types').click(function(){
        var self_elem = $(this);
        if (!self_elem.hasClass('selected')) {
            supports.trigger_support_select(self_elem);
        }
    })

    $('.cart-submit').click(function(e){
        var button = this;
        var button_text = $(button).text()
        e.preventDefault();
        //create form
        var url = $('form#add_to_cart').attr('action');
        var csrf = $('form input[name="csrfmiddlewaretoken"]').val();
        var product_id = $('form input[name="product_id"]').val();
        var qty = $('input[name="qty"]').val();
        var stock = $('#support_sizes a.selected').attr('data-id');
        if (!stock) {
            alert_box.show_message('#add_to_cart_alert_box', 'alert-danger', 'Please select a size!')
            return false;
        }
        cart.add_product(url, csrf, {
            'product_id': product_id,
            'qty': qty,
            'stock': stock
        }, function(){
            alert_box.show_message('#add_to_cart_alert_box', 'alert-primary', 'Adding product to cart', true)
        }, function(data) {
            alert_box.hide('#add_to_cart_alert_box')
            alert_box.show_message('#add_to_cart_alert_box', 'alert-primary', data.result)
        }, function(data) {
            cart.refresh()
        })
    })
})
