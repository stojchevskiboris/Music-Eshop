from django import forms
from .models import Instrument, Customer


class InstrumentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(InstrumentForm, self).__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs["class"] = "form-control"

    class Meta:
        model = Instrument
        fields = '__all__'

class CustomerForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CustomerForm, self).__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs["class"] = "form-control"

    class Meta:
        model = Customer
        exclude = ("customersession",)