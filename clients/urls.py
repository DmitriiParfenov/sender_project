from django.urls import path
from django.views.decorators.cache import cache_page

from clients.apps import ClientsConfig
from clients.views import SenderTemplateView, ClientListView, ClientCreateView, ClientUpdateView, ClientDetailView, \
    ClientDeleteView

app_name = ClientsConfig.name

urlpatterns = [
    path('', cache_page(60)(SenderTemplateView.as_view()), name='index'),
    path('clients/', ClientListView.as_view(), name='clients_list'),
    path('add_client/', ClientCreateView.as_view(), name='add_client'),
    path('update_client/<int:pk>/', ClientUpdateView.as_view(), name='update_client'),
    path('clients/<int:pk>/', ClientDetailView.as_view(), name='client_detail'),
    path('delete_client/<int:pk>/', ClientDeleteView.as_view(), name='delete_client')
]