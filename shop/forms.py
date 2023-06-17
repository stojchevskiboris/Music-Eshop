from django import forms
from .models import Instrument


class InstrumentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(InstrumentForm, self).__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs["class"] = "form-control"

    class Meta:
        model = Instrument
        fields = '__all__'