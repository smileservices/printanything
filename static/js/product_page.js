

$(document).ready(function(){

    var supports = {
        'data_by_id': {},
        'rendered_by_id': {},
        'get_stock_url': function(id) {
            return '/products/get_support/'+id;
        },
        'select': function(id) {
            var self = this;
            if (!self.rendered_by_id[id]) {
                var data = self.data_by_id[id];
                var colours_rendered = self.render_colours(data);
                var sizes_rendered = self.render_sizes(data);
                first_colour = Object.keys(data)[0]
                $('#support_section').template({
                    'colours': colours_rendered,
                    'sizes': sizes_rendered[first_colour],
                }, '#sup_sec_tmpl');
                self.rendered_by_id[id] = $('#support_section').html();
            } else {
                $('#support_section').html(self.rendered_by_id[id]);
            }
        },
        'render_colours': function(data) {
            var rendered = $('<div id="available_colours"></div>');
            $.each(data, function(key, val){
                rendered.template({
                    'colour_lower': key.toLowerCase(),
                    'colour': key
                }, '#sup_sec_tmpl_colours', true)
            })
            return rendered.html();
        },
        'render_sizes': function(data) {
            var sizes_by_colours = {};
            $.each(data, function(key, sizes){
                var rendered = $('<div id="available_sizes"></div>');
                $.each(sizes, function(key, size){
                    rendered.template({
                        'size': size.size
                    }, '#sup_sec_tmpl_size', true)
                })
                sizes_by_colours[key] = rendered.html();
            })
            return sizes_by_colours;
        },
        'trigger_select': function(support_id, self_elem) {
            var self = this;
            ajax_object.retrieve(self.get_stock_url(support_id),
                done=function(data){
                    supports.data_by_id[support_id] = data;},
                before=function() {
                    $('.support-types').removeClass('selected');
                    self_elem.addClass('selected');},
                after=function() {
                    supports.select(support_id);
                }
            )
        }
    }

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

    // get support options
    $('.support-types').click(function(){
        var self_elem = $(this);
        if (!self_elem.hasClass('selected')) {
            support_id = self_elem.attr('data-id');
            supports.trigger_select(support_id, self_elem);
        }
    })
})
