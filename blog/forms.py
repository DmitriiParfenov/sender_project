from django.forms import models

from blog.models import Blog
from clients.forms import StyleMixin


class BlogForm(StyleMixin, models.ModelForm):
    class Meta:
        model = Blog
        fields = ('title', 'content', 'image', 'email')
        labels = {'email': 'Электронная почта для связи с вами'}

