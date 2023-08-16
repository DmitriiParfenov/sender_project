from django.urls import reverse_lazy, reverse
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DetailView, DeleteView

from clients.forms import ClientForm
from clients.models import Client
from django.shortcuts import get_object_or_404


# Create your views here.
class SenderTemplateView(TemplateView):
    template_name = 'clients/index.html'
    extra_context = {
        'title': 'Sender: Главная'
    }


class ClientListView(ListView):
    model = Client
    paginate_by = 3
    extra_context = {
        'title': 'Клиенты'
    }


class ClientCreateView(CreateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('client:clients_list')
    extra_context = {
        'title': 'Добавление'
    }


class ClientUpdateView(UpdateView):
    model = Client
    form_class = ClientForm
    extra_context = {
        'title': 'Изменение'
    }

    def get_success_url(self):
        return reverse('client:client_detail', args=[self.kwargs.get('pk')])


class ClientDetailView(DetailView):
    model = Client

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        client_name = get_object_or_404(Client, pk=self.kwargs.get('pk'))
        context['title'] = client_name.last_name + ' ' + client_name.first_name[0]
        return context


class ClientDeleteView(DeleteView):
    model = Client
    success_url = reverse_lazy('client:clients_list')
    extra_context = {
        'title': 'Удаление'
    }
