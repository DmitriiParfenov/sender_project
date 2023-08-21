from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, ListView, DeleteView, DetailView, UpdateView

from sender.forms import SenderForm
from sender.models import Sender, SenderLog


# Create your views here.
class SenderCreateView(LoginRequiredMixin, CreateView):
    """Контроллер создает форму, которая позволяет пользователю добавить клиента в базу данных Sender."""

    model = Sender
    form_class = SenderForm
    success_url = reverse_lazy('sender:sender_list')
    extra_context = {
        'title': 'Создание рассылки'
    }

    def form_valid(self, form):
        """Метод возвращает только валидную форму. Объекты в модели Sender могут создать только авторизованные
        пользатели, причем эти пользователи автоматически присваиваются к создаваемому объекту."""

        if form.is_valid():
            self.object = form.save()
            self.object.sender_user = self.request.user
            self.object.save()

        return super().form_valid(form)


class SenderListView(LoginRequiredMixin, ListView):
    """Контроллер генерирует страницу sender_list.html, на которой представлены все рассылки.
    Добавлена пагинация, на каждой странице присутствуют до 3 объктов."""

    model = Sender
    paginate_by = 3
    extra_context = {
        'title': 'Рассылки'
    }

    def get_queryset(self):
        """Метод возвращает список только тех объектов модели Sender, которые создал сам пользователь. Если пользователь
         — это superuser, то метод вернет все объекты."""

        if self.request.user.is_superuser:
            return super().get_queryset()
        return super().get_queryset().filter(
            sender_user=self.request.user
        )


class SenderUpdateView(LoginRequiredMixin, UpdateView):
    """Контроллер на основе шаблона sender_form.html позволяет редактировать рассылку по модели Sender."""

    model = Sender
    form_class = SenderForm
    extra_context = {
        'title': 'Изменение'
    }

    def get_object(self, queryset=None):
        """Если текущий пользователь — это создатель рассылки или пользователь с расширенными правами
       для редактирования, то вернется текущий объект, иначе — ошибка 404."""

        self.object = super().get_object(queryset)
        current_user = self.request.user
        if current_user == self.get_context_data()['sender_user'] or self.request.user.is_superuser:
            return self.object
        else:
            raise Http404

    def get_context_data(self, **kwargs):
        """Метод добавляет в контекст шаблонную переменную sender_user cо значением создателя текущей рассылки."""

        context_data = super().get_context_data(**kwargs)
        context_data['sender_user'] = self.object.sender_user
        return context_data

    def form_valid(self, form):
        """Метод возвращает только валидную форму. Объекты в модели Sender могут изменять только авторизованные
        пользатели, к тому же пользователи не могут изменять рассылки, создателями которых они не являются."""

        if form.is_valid():
            self.object = form.save()
            if not self.request.user.is_staff:
                self.object.sender_user = self.request.user
                self.object.save()
            self.object.save()

        return super().form_valid(form)

    def get_success_url(self):
        """Метод возвращает страницу sender_detail.html при успешном обновлении рассылки."""

        return reverse('sender:sender_detail', args=[self.kwargs.get('pk')])


class SenderDetailView(LoginRequiredMixin, DetailView):
    """Контроллер генерирует страницу sender_detail.html, на которой представлена информация о конкретной рассылке."""

    model = Sender
    extra_context = {
        'title': 'Рассылка'
    }

    def get_object(self, queryset=None):
        """Если текущий пользователь — это создатель рассылки или пользователь с расширенными правами
        для редактирования, то вернется текущий объект, иначе — ошибка 404."""

        self.object = super().get_object(queryset)
        current_user = self.request.user
        if current_user == self.get_context_data()['sender_user'] or self.request.user.is_superuser:
            return self.object
        else:
            raise Http404

    def get_context_data(self, **kwargs):
        """Метод добавляет в context ключ title, значение которого — название текущей страницы, ключ sender_user,
        значение которого — создатель текущей рассылки."""

        context = super().get_context_data(**kwargs)
        sender_name = get_object_or_404(Sender, pk=self.kwargs.get('pk'))
        context['title'] = sender_name.subject
        context['sender_user'] = self.object.sender_user
        return context


class SenderDeleteView(LoginRequiredMixin, DeleteView):
    """Контроллер на основе шаблона sender_confirm_delete.html позволяет удалять строки из модели Sender.
    При успешном удалении произойдет переадресация на страницу sender_list.html."""

    model = Sender
    success_url = reverse_lazy('sender:sender_list')
    extra_context = {
        'title': 'Удаление'
    }

    def get_object(self, queryset=None):
        """Если текущий пользователь — это создатель рассылки или пользователь с расширенными правами
        для удаления, то вернется текущий объект, иначе — ошибка 404."""

        self.object = super().get_object(queryset)
        if self.request.user == self.object.sender_user or self.request.user.is_superuser:
            return self.object
        else:
            raise Http404


class SenderLogListView(LoginRequiredMixin, ListView):
    """Контроллер генерирует страницу senderlog_list.html, на которой представлены все клиенты. Добавлена пагинация,
    на каждой странице присутствуют до 3 объктов."""

    model = SenderLog
    paginate_by = 3
    my_form = ''
    extra_context = {
        'title': 'Статистика'
    }

    def get_queryset(self):
        """Метод возвращает список только тех объектов модели SenderLog, которые создал сам пользователь. Если
        пользователь — это superuser, то метод вернет все объекты."""

        if self.request.user.is_superuser:
            return super().get_queryset()
        return super().get_queryset().filter(
            sender__sender_user=self.request.user
        )


class SenderLogDetail(LoginRequiredMixin, DetailView):
    """Контроллер генерирует страницу senderlog_detail.html, на которой представлена статистика о конкретной
    рассылке."""

    model = SenderLog
    extra_context = {
        'title': 'Информация о рассылке'
    }

    def get_object(self, queryset=None):
        """Если текущий пользователь — это создатель рассылки, на основе которой получена статистика или пользователь
        с расширенными правами для просмотра, то вернется текущий объект, иначе — ошибка 404."""

        self.object = super().get_object(queryset)
        if self.request.user == self.object.sender.sender_user or self.request.user.is_superuser:
            return self.object
        else:
            raise Http404


class SenderLogDelete(PermissionRequiredMixin, DeleteView):
    """Контроллер на основе шаблона senderlog_confirm_delete.html позволяет удалять строки из модели SenderLog.
    При успешном удалении произойдет переадресация на страницу senderlog_list.html."""

    model = SenderLog
    success_url = reverse_lazy('sender:senderlog_list')
    permission_required = 'sender.senderlog_delete'
    extra_context = {
        'title': 'Информация о рассылке'
    }
