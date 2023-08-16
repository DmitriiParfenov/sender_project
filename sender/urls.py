from django.urls import path

from sender.apps import SenderConfig
from sender.views import SenderCreateView, SenderListView, SenderUpdateView, SenderDetailView, SenderDeleteView

app_name = SenderConfig.name

urlpatterns = [
    path('add_mail/', SenderCreateView.as_view(), name='add_mail'),
    path('', SenderListView.as_view(), name='sender_list'),
    path('update_sender/<int:pk>/', SenderUpdateView.as_view(), name='update_sender'),
    path('delete_sender/<int:pk>/', SenderDeleteView.as_view(), name='delete_sender'),
    path('<int:pk>/', SenderDetailView.as_view(), name='sender_detail')
]
