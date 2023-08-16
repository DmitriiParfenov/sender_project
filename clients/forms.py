from django.forms import models

from clients.models import Client


class StyleMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class ClientForm(StyleMixin, models.ModelForm):
    class Meta:
        model = Client
        fields = ('first_name', 'last_name', 'middle_name', 'email', 'comment')
