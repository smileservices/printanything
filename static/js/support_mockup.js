/*
* All classes related to handling the support image overlayed with art image
*
*
* */

var support_image = {
    canvas_width: 675,
    canvas_height: 675,
    stage: null,
    layer: null,
    layer_art: null,
    layer_print_area: null,
    current_print_area: null,
    current_color: null,
    current_imgUrl: null,
    konva_art_image: null,
    init: function(imgUrl, color, printArea) {
        var self = this;
        self.current_color = color;
        self.current_print_area = printArea;
        self.current_imgUrl = imgUrl;

        self.stage = new Konva.Stage({
            container: 'product_canvas',
            width: self.canvas_width,
            height: self.canvas_height
        });
        self.layer = new Konva.Layer();
        self.layer_art = new Konva.Layer();
        self.layer_print_area = new Konva.Layer();
        self.stage.add(self.layer);
        self.stage.add(self.layer_print_area);
        self.stage.add(self.layer_art);
    },

    render: function(imgUrl=null, color=null, printArea=null) {
        var self = this;
        if (imgUrl && color && printArea) {
            self.init(imgUrl, color, printArea);
        }
        var background = new Konva.Rect({
            x: 0,
            y: 0,
            width: self.canvas_width,
            height: self.canvas_height,
            fill: self.current_color
        });
        self.layer.add(background);
        var mockup_image = new Konva.Image({
            x: 0,
            y: 0,
            width: self.canvas_width,
            height: self.canvas_height,
            name: 'mockup_image'
        });

        self.layer.add(mockup_image);
        var imgSupport = new Image();
        imgSupport.onload = function() {
            mockup_image.image(imgSupport);
            self.layer.draw();
            self.__render_print_area(false);
            self.__render_art();
        };
        imgSupport.src = self.current_imgUrl
    },

    __handle_click: function (e) {
        var stage = this;
        var layer_print_area = stage.getLayers()[1];
        var layer = stage.getLayers()[2];
        var print_area_rect = layer_print_area.children[0];
        // do nothing if clicked NOT on our stage
        if (!e.target.hasName('art_image')) {
            stage.find('Transformer').destroy();
            layer.draw();
            layer_print_area.hide();
            return;
        }
        // create new transformer
        var tr = new Konva.Transformer({
            rotateEnabled: false,
            boundBoxFunc: function (oldBoundBox, newBoundBox) {
                if (newBoundBox.width > print_area_rect.width()) newBoundBox.width = print_area_rect.width();
                if (newBoundBox.height > print_area_rect.height()) newBoundBox.height = print_area_rect.height();
                return newBoundBox;
            }
        });
        layer.add(tr);
        tr.attachTo(e.target);
        layer.draw();
    },

    __render_print_area: function() {
        var self = this;
        var print_area_rect = new Konva.Rect({
            x: self.current_print_area.x,
            y: self.current_print_area.y,
            width: self.current_print_area.width,
            height: self.current_print_area.height,
            fill: '#1db7a8',
            opacity: 0.4,
            name: 'print_area'
        });
        self.layer_print_area.add(print_area_rect);
        self.layer_print_area.draw();
        self.layer_print_area.hide();
    },

    __render_art: function() {
        var self = this;
        self.konva_art_image = new Konva.Image({
            x: self.current_print_area.x,
            y: self.current_print_area.y,
            width: self.current_print_area.width,
            height: self.current_print_area.height,
            name: 'art_image',
            draggable: true,
            dragBoundFunc: function (pos) {
                var handled_pos = {x:pos.x,y:pos.y};
                var art_dims = {
                    width: parseInt(self.konva_art_image.width()*self.konva_art_image.scaleX()),
                    height: parseInt(self.konva_art_image.height()*self.konva_art_image.scaleY())
                };
                //limit the movement inside the printing area
                if (pos.x <= self.current_print_area.x) handled_pos.x = self.current_print_area.x;
                if (pos.y <= self.current_print_area.y) handled_pos.y = self.current_print_area.y;
                if (pos.x+art_dims.width >= self.current_print_area.x+self.current_print_area.width) handled_pos.x = self.current_print_area.x+self.current_print_area.width-art_dims.width;
                if (pos.y+art_dims.height >= self.current_print_area.y+self.current_print_area.height) handled_pos.y = self.current_print_area.y+self.current_print_area.height-art_dims.height;
                return handled_pos
            }
        });
        self.layer_art.add(self.konva_art_image);
        var image = new Image();
        image.onload = function () {
            self.konva_art_image.image(image);
            self.layer_art.draw();
        };
        image.src = placeable_art;

        self.stage.on('click tap', self.__handle_click);
        self.konva_art_image.on('dragmove', function () {
            self.layer_print_area.show();
        })
        self.konva_art_image.on('transform', function () {
            self.layer_print_area.show();
        })
    }
};
