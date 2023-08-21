import random

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DetailView, DeleteView

from blog.models import Blog
from clients.forms import ClientForm
from clients.models import Client
from sender.models import Sender


# Create your views here.
class SenderTemplateView(TemplateView):
    """Контроллер генерирует страницу index.html, на которой представлены три карточки:
    1) Добавление клиента — количество уникальных клиентов и возможность добавления клиента.
    2) Создание сообщения — количество всех рассылок и количество уникальных рассылок, а также возможность добавить
    сообщение.
    3) Просмотр статей — 3 случайных заголовка из базы статей, а также возможность к переходу ко всем статьям."""

    template_name = 'clients/index.html'
    extra_context = {
        'title': 'Sender: Главная'
    }

    def get_context_data(self, **kwargs):
        """Метод добавляет в context ключ all_clients, значение которого — количество уникальных клиентов, ключ
        active_senders, значение которого — это количество активных рассылок, ключ all_senders, значение которого — это
        количество всех рассылок, а также ключ blogs — в случае, если количество статей меньше 3 в базе, то значение
        ключа — это все статьи из модели Blog, иначе — список из 3 случайных объектов модели Blog."""

        context_data = super().get_context_data(**kwargs)

        context_data['all_clients'] = Client.objects.distinct().count()
        context_data['active_senders'] = Sender.objects.filter(status=Sender.Status.STARTED).count()
        context_data['all_senders'] = Sender.objects.count()

        if Blog.objects.count() < 3:
            context_data['blogs'] = Blog.objects.all()
        else:
            context_data['blogs'] = random.sample([x for x in Blog.objects.all()], 3)

        return context_data


class ClientListView(LoginRequiredMixin, ListView):
    """Контроллер генерирует страницу client_list.html, на которой представлены все клиенты.
    Добавлена пагинация, на каждой странице присутствуют до 3 объктов."""

    model = Client
    paginate_by = 3
    extra_context = {
        'title': 'Клиенты'
    }

    def get_queryset(self):
        """Метод возвращает список только тех объектов модели Client, которые создал сам пользователь. Если пользователь
         — это superuser, то метод вернет все объекты."""

        if self.request.user.is_superuser:
            return super().get_queryset()
        return super().get_queryset().filter(
            client_user=self.request.user
        )


class ClientCreateView(LoginRequiredMixin, CreateView):
    """Контроллер создает форму, которая позволяет пользователю добавить клиента в базу данных Client."""

    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('client:clients_list')
    extra_context = {
        'title': 'Добавление'
    }

    def form_valid(self, form):
        """Метод возвращает только валидную форму. Объекты в модели Client могут создать только авторизованные
        пользатели, причем эти пользователи автоматически присваиваются к создаваемому объекту."""

        if form.is_valid():
            self.object = form.save()
            self.object.client_user = self.request.user
            self.object.save()

        return super().form_valid(form)


class ClientUpdateView(LoginRequiredMixin, UpdateView):
    """Контроллер на основе шаблона client_form.html позволяет редактировать клиента по модели Client."""

    model = Client
    form_class = ClientForm
    extra_context = {
        'title': 'Изменение'
    }

    def get_object(self, queryset=None):
        """Если текущий пользователь — это создатель клиента или пользователь с расширенными правами
       для редактирования, то вернется текущий объект, иначе — ошибка 404."""

        self.object = super().get_object(queryset)
        current_user = self.request.user
        if current_user == self.get_context_data()['client_user'] or self.request.user.is_superuser:
            return self.object
        else:
            raise Http404

    def get_context_data(self, **kwargs):
        """Метод добавляет в контекст шаблонную переменную client_user cо значением создателя текущего клиента."""

        context_data = super().get_context_data(**kwargs)
        context_data['client_user'] = self.object.client_user
        return context_data

    def form_valid(self, form):
        """Метод возвращает только валидную форму. Объекты в модели Client могут изменять только авторизованные
        пользатели, к тому же пользователи не могут изменять клиентов, создателями которых они не являются."""

        if form.is_valid():
            self.object = form.save()
            if not self.request.user.is_staff:
                self.object.client_user = self.request.user
                self.object.save()
            self.object.save()

        return super().form_valid(form)

    def get_success_url(self):
        """Метод возвращает страницу client_detail.html при успешном обновлении клиента."""
        return reverse('client:client_detail', args=[self.kwargs.get('pk')])


class ClientDetailView(LoginRequiredMixin, DetailView):
    """Контроллер генерирует страницу client_detail.html, на которой представлена информация о конкретном клиенте."""

    model = Client

    def get_object(self, queryset=None):
        """Если текущий пользователь — это создатель клиента или пользователь с расширенными правами
        для просмотра, то вернется текущий объект, иначе — ошибка 404."""

        self.object = super().get_object(queryset)
        current_user = self.request.user
        if current_user == self.get_context_data()['client_user'] or self.request.user.is_superuser:
            return self.object
        else:
            raise Http404

    def get_context_data(self, **kwargs):
        """Метод добавляет в context ключ title, значение которого — название текущей страницы, ключ client_user,
        значение которого — создатель текущего клиента."""

        context = super().get_context_data(**kwargs)
        client_name = get_object_or_404(Client, pk=self.kwargs.get('pk'))
        context['title'] = client_name.last_name + ' ' + client_name.first_name[0]
        context['client_user'] = self.object.client_user
        return context


class ClientDeleteView(LoginRequiredMixin, DeleteView):
    """Контроллер на основе шаблона client_confirm_delete.html позволяет удалять строки из модели Client.
    При успешном удалении произойдет переадресация на страницу client_list.html."""

    model = Client
    success_url = reverse_lazy('client:clients_list')
    extra_context = {
        'title': 'Удаление'
    }

    def get_object(self, queryset=None):
        """Если текущий пользователь — это создатель клиента или пользователь с расширенными правами
        для удаления, то вернется текущий объект, иначе — ошибка 404."""

        self.object = super().get_object(queryset)
        current_user = self.request.user
        if current_user == self.object.client_user or self.request.user.is_superuser:
            return self.object
        else:
            raise Http404
