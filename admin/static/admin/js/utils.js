var FormHandler = function(formId, prefix, appendTo) {
    var self = this;
    self.formId = formId;
    self.prefix = prefix;
    self.formContainer = $('#' + formId);
    self.newFormcallback = function() {};
    self.init = function () {
        self.currentIndex = self.__getIndex() - 1;
        self.extraForm = self.__prepareNextExtraForm();
    };
    self.addNewForm = function () {
        var self = this;
        //remove the extraform class from the last form
        self.formContainer
            .find('.extra_record')
            .removeClass('extra_record');
        if (appendTo) {
            self.extraForm.appendTo($(appendTo).appendTo(self.formContainer));
        } else {
            self.extraForm.appendTo(self.formContainer);
        }
        //increment counter
        self.__incrementIndex();
        //prepare next form
        self.extraForm = self.__prepareNextExtraForm();
        self.newFormcallback();
    };
    self.setNewFormCallback = function (callback) {
        //this runs after adding the form
        var self = this;
        self.newFormcallback = callback;
    };
    self.setFormCleanCallback = function (callback) {
        //this will run when cleaning the cloned form. callback will process the html string
        var self = this;
        self.formCleanCallback = callback;
    };
    self.__prepareNextExtraForm = function () {
        var self = this;
        var nextExtraForm = self.formContainer.find('.extra_record').clone(true)
        if (self.formCleanCallback) {
            nextExtraForm = self.formCleanCallback(nextExtraForm);
        }
        //replace former values
        var replace = self.prefix+'-'+self.currentIndex;
        var replaceWith = self.prefix+'-'+(self.currentIndex+1);
        var newForm = $('<div></div>')
            .addClass('row')
            .addClass('extra_record')
            .append(
                nextExtraForm.html().split(replace).join(replaceWith)
            );
        return newForm;
    };
    self.__getIndex = function() {
        // function for getting the index
        var self = this;
        return parseInt($('#id_'+self.prefix+'-TOTAL_FORMS').val());
    };
    self.__incrementIndex = function() {
        // sets form counters - TOTAL_FORMS
        var self = this;
        self.currentIndex += 1;
        $('#id_'+self.prefix+'-TOTAL_FORMS').val(self.currentIndex+1);
    };
};
