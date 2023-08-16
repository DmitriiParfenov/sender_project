from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, ListView, DeleteView, DetailView, UpdateView

from sender.forms import SenderForm
from sender.models import Sender


# Create your views here.
class SenderCreateView(CreateView):
    model = Sender
    form_class = SenderForm
    success_url = reverse_lazy('sender:sender_list')
    extra_context = {
        'title': 'Создание рассылки'
    }


class SenderListView(ListView):
    model = Sender
    paginate_by = 3
    extra_context = {
        'title': 'Рассылки'
    }


class SenderUpdateView(UpdateView):
    model = Sender
    form_class = SenderForm
    extra_context = {
        'title': 'Изменение'
    }

    def get_success_url(self):
        return reverse('sender:sender_detail', args=[self.kwargs.get('pk')])


class SenderDetailView(DetailView):
    model = Sender
    extra_context = {
        'title': 'Рассылка'
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        sender_name = get_object_or_404(Sender, pk=self.kwargs.get('pk'))
        context['title'] = sender_name.subject
        return context


class SenderDeleteView(DeleteView):
    model = Sender
    success_url = reverse_lazy('sender:sender_list')
    extra_context = {
        'title': 'Удаление'
    }
