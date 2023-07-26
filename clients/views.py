from django.urls import reverse_lazy, reverse
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DetailView, DeleteView

from clients.models import Client


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
    fields = ('first_name', 'last_name', 'middle_name', 'email', 'comment')
    success_url = reverse_lazy('client:clients_list')


class ClientUpdateView(UpdateView):
    model = Client
    fields = ('first_name', 'last_name', 'middle_name', 'email', 'comment')

    def get_success_url(self):
        return reverse('client:client_detail', args=[self.kwargs.get('pk')])


class ClientDetailView(DetailView):
    model = Client


class ClientDeleteView(DeleteView):
    model = Client
    success_url = reverse_lazy('client:clients_list')
