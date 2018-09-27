/*
* All classes related to handling the support image overlayed with art image
*
*
* */

var support_image = {
    canvas: null,
    canvasCtxt: null,
    current_print_area: null,
    current_color: null,
    current_imgUrl: null,

    init: function() {
        var self = this;
        self.canvas = document.getElementById('product_canvas');
        self.canvasCtxt = self.canvas.getContext('2d');
    },

    clear_canvas: function() {
        var self = this;
        self.canvasCtxt.clearRect(0,0,self.canvas.width,self.canvas.height);
    },

    render_support: function(imgUrl, color, printArea) {
        var self = this;
        var imgFullUrl = window.location.origin + imgUrl;
        var imgSupport = new Image();

        self.current_color = color;
        self.current_print_area = printArea;
        self.current_imgUrl = imgUrl;

        imgSupport.width = self.canvas.width;
        imgSupport.height = self.canvas.height;
        imgSupport.src = imgFullUrl;

        self.clear_canvas();

        imgSupport.onload = function(){
            self.canvasCtxt.globalCompositeOperation = 'source-over';
            self.canvasCtxt.drawImage(imgSupport,
                self.canvas.width/2-imgSupport.width/2,
                self.canvas.height/2-imgSupport.height/2,
                self.canvas.width,
                self.canvas.height
            );
            //color the support
            self.canvasCtxt.globalCompositeOperation = 'destination-over';
            self.canvasCtxt.rect(0, 0, self.canvas.width, self.canvas.height);
            self.canvasCtxt.fillStyle = color;
            self.canvasCtxt.fill();
        };
    },

    show_print_area: function() {
        var self = this;
        // self.canvasCtxt.beginPath();
        self.render_support(self.current_imgUrl, self.current_color, self.current_print_area);
        self.canvasCtxt.fillStyle = '#00bcd4';
        self.canvasCtxt.globalCompositeOperation = 'lighten';
        self.canvasCtxt.globalAlpha = 0.6;
        self.canvasCtxt.fillRect(
            self.current_print_area['x'],
            self.current_print_area['y'],
            self.current_print_area['width'],
            self.current_print_area['height']
        );
        self.canvasCtxt.globalAlpha = 1;
        self.render_art();
    },

    hide_print_area: function() {
        var self = this;
        self.redraw();
    },

    redraw: function() {
        var self = this;
        self.render_support(self.current_imgUrl, self.current_color, self.current_print_area);
        self.render_art();
    },

    render_art: function() {
        var self = this;
        if (!self.current_print_area) console.log('MUST FIRST RENDER SUPPORT AND SET PRINT AREA');
        var imgArt = new Image();
        imgArt.width = self.current_print_area['width'];
        imgArt.height = self.current_print_area['height'];
        imgArt.src = window.location.origin + placeable_art;
        imgArt.onload = function(){
            self.canvasCtxt.globalCompositeOperation = 'source-over';
            self.canvasCtxt.drawImage(imgArt,
                self.current_print_area['x'],
                self.current_print_area['y'],
                imgArt.width,
                imgArt.width
            );
        };
    }
};
