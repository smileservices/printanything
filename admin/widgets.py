from django.forms import widgets

widgets.CheckboxInput.template_name = 'widgets/delete.html'


class BoostrapCheckbox(widgets.Input):
    template_name = 'widgets/checkbox.html'

    def get_context(self, name, value, attrs):
        context = super(BoostrapCheckbox, self).get_context(name, value, attrs)
        return context


class BoostrapFileInput(widgets.FileInput):
    template_name = 'widgets/file_input.html'


class ColorInput(widgets.Input):
    template_name = 'widgets/color.html'


class HiddenInput(widgets.Input):
    template_name = 'widgets/hidden.html'
