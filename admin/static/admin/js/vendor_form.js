$(document).ready(function() {
    $('select').select2();

    var getFormListener = function(formHandler, extraFormClass, formId) {
        return function() {
            $('#' + formId + ' .' + extraFormClass).change(function () {
                formHandler.addNewForm();
            });
        }
    };

    var sizeFormHandler = new FormHandler('sizes_form', 'size_set');
    sizeFormHandler.init();
    var sizeFormListener = getFormListener(sizeFormHandler, 'extra_record', 'sizes_form');
    sizeFormHandler.setNewFormCallback(sizeFormListener);
    sizeFormListener();

    var colourFormHandler = new FormHandler('colours_form', 'colour_set');
    colourFormHandler.init();
    var colourFormListener = getFormListener(colourFormHandler, 'extra_record', 'colours_form');
    colourFormHandler.setNewFormCallback(colourFormListener);
    colourFormListener();
});
