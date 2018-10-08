$(document).ready(function () {

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

        'current_support_id': null,
        'current_color': null,
        'current_print_area': null,

        'trigger_support_select': function (self_elem) {
            var self = this;
            self.current_support_id = self_elem.attr('data-id');
            ajax_object.retrieve(self.get_stock_url(self.current_support_id),
                done = function (data) {
                    supports.data_by_id[self.current_support_id] = data;
                    //arrange gallery of supports by primary
                    supports.indexed_images[self.current_support_id] = [];
                    $.each(data['mockup_images'], function(key,mockup_image){
                      if (mockup_image['primary']) supports.indexed_images[self.current_support_id] = mockup_image;
                    })
                },
                before = function () {
                    $('.support-types').removeClass('selected');
                    self_elem.addClass('selected');
                    //show alert
                    alert_box.show_message('#add_to_cart_alert_box', 'alert-primary', 'Retrieving support options', true)
                },
                after = function (data) {
                    alert_box.hide('#add_to_cart_alert_box');
                    self.__select_support(self.current_support_id);
                    //get first color
                    self.current_color = data['colours'][Object.keys(data['colours'])[0]];
                    self.current_print_area = JSON.parse(supports.indexed_images[self.current_support_id]['print_area']);

                    //add listeners
                    $('.color_support').click(function () {
                        supports.__colour_select($(this))
                    });
                    $('#support_sizes a').click(function (e) {
                        e.preventDefault();
                        self.__size_select($(this))
                    });

                    //trigger color select to render the mockup image
                    self.__colour_select($($('.color_support')[0]));
                }
            )
        },

        '__select_support': function (id) {
            var self = this;
            var data = self.data_by_id[id];
            var supportSection = $('#support_section');
            // self.gallery_rendered = self.__render_gallery(data['mockup_images']);
            self.sizes_rendered = self.__render_sizes(data['colours']);
            self.shipping_rendered = self.__render_shipping(data['shipping']);
            if (!self.rendered_by_id[id]) {
                var colours_rendered = self.__render_colours(data['colours']);
                var first_colour = Object.keys(data['colours'])[0];
                supportSection.template({
                    'colours': colours_rendered,
                    'sizes': self.sizes_rendered[first_colour],
                    'shipping': self.shipping_rendered
                }, '#sup_sec_tmpl');
                self.rendered_by_id[id] = supportSection.html();
            } else {
                supportSection.html(self.rendered_by_id[id]);
            }
        },

        '__render_colours': function (data) {
            var rendered = $('<div id="available_colours"></div>');
            var index = 0;
            $.each(data, function (key, colorData) {
                rendered.template({
                    'hex_code': colorData.hex_code,
                    'name': key,
                }, '#sup_sec_tmpl_colours', true)
                index += 1;
            });
            return rendered.html();
        },

        '__render_gallery': function (data) {
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

        '__render_shipping': function (data) {
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

        '__render_sizes': function (data) {
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

        '__colour_select': function (self_elem) {
            var self = this;
            $('.color_support').removeClass("selected");
            self_elem.addClass("selected");
            $('#support_sizes ul').html(self.sizes_rendered[self_elem.val()]);
            $('#support_sizes a').click(function (e) {
                e.preventDefault();
                self.__size_select($(this))
            });

            self.current_color = {
                hex_code: self_elem.css('background-color'),
                name: self_elem.attr('data-name')
            };

            support_image.render(
                self.indexed_images[self.current_support_id]['url'],
                self.current_color['hex_code'],
                self.current_print_area
            );
        },

        '__size_select': function (self_elem) {
            $('#support_sizes a').removeClass('selected');
            self_elem.addClass('selected');
        }
    };

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
        var final_product_img = support_image.stage.toDataURL();
        if (!stock) {
            alert_box.show_message('#add_to_cart_alert_box', 'alert-danger', 'Please select a size!')
            return false;
        }

        var formData = new FormData();
        formData.append('csrfmiddlewaretoken', csrf);
        formData.append('product_id', product_id);
        formData.append('qty', qty);
        formData.append('stock', stock);
        formData.append('product_img', final_product_img);

        cart.add_product(url, formData, function () {
            alert_box.show_message('#add_to_cart_alert_box', 'alert-primary', 'Adding product to cart', true)
        }, function (data) {
            alert_box.hide('#add_to_cart_alert_box')
            alert_box.show_message('#add_to_cart_alert_box', 'alert-primary', data.result)
        }, function (data) {
            cart.refresh()
        })
    })
})
