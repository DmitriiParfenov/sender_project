from django.forms import models

from clients.forms import StyleMixin
from sender.models import Sender


class SenderForm(StyleMixin, models.ModelForm):
    class Meta:
        model = Sender
        fields = ('subject', 'message', 'client', 'period', 'time', 'status')