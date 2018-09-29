$(document).ready(function() {
    $('select').select2();

    var getFormListener = function(formHandler, extraFormClass, formId) {
        return function() {
            $('#' + formId + ' .' + extraFormClass+' input:file').change(function () {
                formHandler.addNewForm();
                $('select').select2();
            });
        }
    };

    var imageFormHandler = new FormHandler('images_form', 'images', '<div class="col-md-3 form-group"></div>');
    var imageFormListener = getFormListener(imageFormHandler, 'extra_record', 'images_form');
    imageFormHandler.setNewFormCallback(imageFormListener);
    imageFormHandler.init();
    imageFormListener();

    $('.set_print_area').click(function (e) {
        //open mockup image modal
        e.preventDefault();
        var link_object = this;
        var id = $(link_object).attr('data-image-id');
        var url = $(link_object).attr('data-image-url');
        var printarea = JSON.parse($(link_object).attr('data-printarea'));
        var modal = $('#set_printing_area');
        modal.find("[name=x]").val(printarea['x']);
        modal.find("[name=y]").val(printarea['y']);
        modal.find("[name=width]").val(printarea['width']);
        modal.find("[name=height]").val(printarea['height']);
        //init canvas_mockup obj
        // canvas_mockup.init(url,printarea);
        // canvas_mockup.render();
        //use konvas
        var width = 675;
        var height = 675;

        var stage = new Konva.Stage({
            container: 'canvas_container',
            width: width,
            height: height
        });

        var layer = new Konva.Layer();
        stage.add(layer);
        var imageObj = new Image();
        var mockup_image = new Konva.Image({
            x: 0,
            y: 0,
            width: width,
            height: height,
            name: 'mockup_image'
        });

        layer.add(mockup_image);

        imageObj.onload = function() {
            mockup_image.image(imageObj);
            layer.draw();
        };

        imageObj.src = url;

        var print_area_rendered = new Konva.Rect({
            x: printarea.x,
            y: printarea.y,
            width: printarea.width,
            height: printarea.height,
            fill: '#0aa89e',
            name: 'rect',
            draggable: true,
            opacity: 0.6,
            strokeWidth: 1
        });

        layer.add(print_area_rendered);
        layer.draw();

        stage.on('click tap', function (e) {
            // if click on empty area - remove all transformers
            if (e.target === mockup_image) {
                stage.find('Transformer').destroy();
                layer.draw();
                return;
            }
            // do nothing if clicked NOT on our rectangles
            if (!e.target.hasName('rect')) {
                return;
            }
            // create new transformer
            var tr = new Konva.Transformer({
                rotateEnabled: false,
            });

            layer.add(tr);
            tr.attachTo(e.target);
            layer.draw();

        });
        print_area_rendered.on('dragmove', function () {
            //add new coords to input
            printarea.x = parseInt(print_area_rendered.x());
            printarea.y = parseInt(parseInt(print_area_rendered.y()));
            modal.find("[name=x]").val(printarea.x);
            modal.find("[name=y]").val(printarea.y);
        });
        print_area_rendered.on('transform', function () {
            printarea.x = parseInt(print_area_rendered.x());
            printarea.y = parseInt(parseInt(print_area_rendered.y()));
            printarea.width = parseInt(print_area_rendered.width()*print_area_rendered.scaleX());
            printarea.height = parseInt(print_area_rendered.height()*print_area_rendered.scaleY());
            //add new coords and size to input
            modal.find("[name=x]").val(printarea.x);
            modal.find("[name=y]").val(printarea.y);
            modal.find("[name=width]").val(printarea.width);
            modal.find("[name=height]").val(printarea.height);
        });

        modal.modal('show');

        //add listener for save
        $('#printarea_save').click(function (e) {
            e.preventDefault();
            //save json string in input and link
            $(link_object).attr('data-printarea', JSON.stringify(printarea));
            //a bit hacky way to find the input for printarea
            $($(link_object).siblings('input')[0]).val(JSON.stringify(printarea));
            modal.modal('hide');
        })
    })
});


