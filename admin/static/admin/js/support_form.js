// $(document).ready(function() {
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
    imageFormHandler.setFormCleanCallback(function(formHtml){
        formHtml.find('span.select2-container').remove();
        formHtml.find('.select2-hidden-accessible').removeClass('select2-hidden-accessible');
        return formHtml;
    });
    imageFormHandler.init();
    imageFormListener();
// });
