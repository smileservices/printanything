var FormHandler = function(formId, prefix) {
    var self = this;
    self.formId = formId;
    self.prefix = prefix;
    self.formContainer = $('#' + formId);
    self.init = function () {
        self.currentIndex = self.__getIndex() - 1;
        self.extraForm = self.__prepareNextExtraForm();
    };
    self.addNewForm = function () {
        var self = this;
        //remove the extraform class from the last form
        self.formContainer
            .find('.extra_record')
            .removeClass('extra_record')
            .parent()
            .append(self.extraForm);
        //increment counter
        self.__incrementIndex();
        //prepare next form
        self.extraForm = self.__prepareNextExtraForm();
        self.newFormcallback();
    };
    self.setNewFormCallback = function (callback) {
        var self = this;
        self.newFormcallback = callback;
    };
    self.__prepareNextExtraForm = function () {
        var self = this;
        var nextExtraForm = self.formContainer.find('.extra_record').clone(true)
        //replace former values
        var replace = self.prefix+'_set-'+self.currentIndex;
        var replaceWith = self.prefix+'_set-'+(self.currentIndex+1);
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
        return parseInt($('#id_'+self.prefix+'_set-TOTAL_FORMS').val());
    };
    self.__incrementIndex = function() {
        // sets form counters - TOTAL_FORMS
        var self = this;
        self.currentIndex += 1;
        $('#id_'+self.prefix+'_set-TOTAL_FORMS').val(self.currentIndex+1);
    };
};
