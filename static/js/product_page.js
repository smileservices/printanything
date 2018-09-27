// $(document).ready(function () {

    /*
    * after selecting support a request is made to get back associated stock items.
    * then the templates are populated and rendered
    *
    * */
    var supports = {

        'data_by_id': {},
        'rendered_by_id': {},
        'get_stock_url': function (id) {
            return '/products/get_support/' + id;
        },
        'indexed_images': [],
        'select_support': function (id) {
            var self = this;
            var data = self.data_by_id[id];
            var supportSection = $('#support_section');
            self.gallery_rendered = self.render_gallery(data['colours']);
            self.sizes_rendered = self.render_sizes(data['colours']);
            self.shipping_rendered = self.render_shipping(data['shipping']);
            if (!self.rendered_by_id[id]) {
                var colours_rendered = self.render_colours(data['colours']);
                var first_colour = Object.keys(data['colours'])[0];
                supportSection.template({
                    'colours': colours_rendered,
                    'support_gallery': self.gallery_rendered[first_colour],
                    'sizes': self.sizes_rendered[first_colour],
                    'shipping': self.shipping_rendered
                }, '#sup_sec_tmpl');
                self.rendered_by_id[id] = supportSection.html();
            } else {
                supportSection.html(self.rendered_by_id[id]);
            }
            //change colours listener
            $('input[name="colour"]').click(function () {
                var self_elem = $(this);
                self_elem.removeAttr('checked');
                supports.colour_select(self_elem)
            });
            $('#support_sizes a').click(function (e) {
                e.preventDefault();
                self.size_select($(this))
            })
        },
        'render_colours': function (data) {
            var rendered = $('<div id="available_colours"></div>');
            var index = 0;
            $.each(data, function (key, colorData) {
                rendered.template({
                    'colour_lower': key.toLowerCase(),
                    'colour': key,
                    'checked': index == 0 ? 'checked="checked"' : ''
                }, '#sup_sec_tmpl_colours', true)
                index += 1;
            })
            return rendered.html();
        },
        'render_gallery': function (data) {
            var gallery_by_colours = {};
            $.each(data, function (key, colorData) {
                var rendered = $('<div id="support_gallery"></div>');
                $.each(colorData['gallery'], function (key, img) {
                    rendered.template({
                        'primary': img['primary'],
                        'url': img['url'],
                        'thumb_url': img['thumb'],
                    }, '#sup_sec_tmpl_colour_gallery', true)
                });
                gallery_by_colours[key] = rendered.html();
            });
            return gallery_by_colours;
        },
        'render_shipping': function (data) {
            var rendered = $('<div id="shipping"></div>');
            var index = 0;
            $.each(data, function (k, shipper) {
                rendered.template({
                    'name': shipper['name'],
                    'price': shipper['price'],
                    'description': shipper['description'],
                }, '#sup_sec_tmpl_shipping', true)
                index += 1;
            })
            return rendered.html();
        },
        'render_sizes': function (data) {
            var sizes_by_colours = {};
            $.each(data, function (key, colorData) {
                var rendered = $('<div id="available_sizes"></div>');
                $.each(colorData['sizes'].sort(function(a,b){return (a.size>b.size ? 1 : -1)}), function (key, size) {
                    rendered.template({
                        'size': size.size,
                        'size-id': size.id
                    }, '#sup_sec_tmpl_size', true)
                })
                sizes_by_colours[key] = rendered.html();
            })
            return sizes_by_colours;
        },
        'colour_select': function (self_elem) {
            var self = this;
            // this changes both sizes and support gallery
            self_elem.prop("checked", true);
            $('#support_gallery').html(self.gallery_rendered[self_elem.val()]);
            $('#support_sizes ul').html(self.sizes_rendered[self_elem.val()]);
            $('#support_sizes a').click(function (e) {
                e.preventDefault();
                self.size_select($(this))
            })
        },
        'size_select': function (self_elem) {
            $('#support_sizes a').removeClass('selected');
            self_elem.addClass('selected');
        },
        'trigger_support_select': function (self_elem) {
            var self = this;
            var support_id = self_elem.attr('data-id');
            ajax_object.retrieve(self.get_stock_url(support_id),
                done = function (data) {
                    supports.data_by_id[support_id] = data;
                    //arrange gallery of supports by primary
                    supports.indexed_images[support_id] = [];
                    $.each(data['colours'], function(colourName,colourArr){
                        $.each(colourArr['gallery'], function(i,val){
                          if (val['primary']) {
                              if (!supports.indexed_images[support_id][colourName]) supports.indexed_images[support_id][colourName] = null;
                              supports.indexed_images[support_id][colourName] = val;
                          }
                        })
                    })
                },
                before = function () {
                    $('.support-types').removeClass('selected');
                    self_elem.addClass('selected');
                    //show alert
                    alert_box.show_message('#add_to_cart_alert_box', 'alert-primary', 'Retrieving support options', true)
                },
                after = function () {
                    alert_box.hide('#add_to_cart_alert_box');
                    supports.select_support(support_id);
                    //show on canvas
                    var first_key = Object.keys(self.indexed_images[support_id])[0];
                    //must refactor after refactoring support colours
                    support_image.render_support(
                        self.indexed_images[support_id][first_key]['url'],
                        'green',
                        {
                            'width': 200,
                            'height': 250,
                            'x': 230,
                            'y': 210,
                        }
                    );
                    support_image.render_art();
                }
            )
        }
    };



    //initialize support image object
    support_image.init();
    //initialize first support
    supports.trigger_support_select($('.support-types').first())

    // get support options
    $('.support-types').click(function () {
        var self_elem = $(this);
        if (!self_elem.hasClass('selected')) {
            supports.trigger_support_select(self_elem);
        }
    })

    $('.cart-submit').click(function (e) {
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
        }, function () {
            alert_box.show_message('#add_to_cart_alert_box', 'alert-primary', 'Adding product to cart', true)
        }, function (data) {
            alert_box.hide('#add_to_cart_alert_box')
            alert_box.show_message('#add_to_cart_alert_box', 'alert-primary', data.result)
        }, function (data) {
            cart.refresh()
        })
    })
// })
