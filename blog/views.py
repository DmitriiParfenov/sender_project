from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.http import Http404
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView

from blog.forms import BlogForm
from blog.models import Blog


# Create your views here.
class BlogListView(LoginRequiredMixin, ListView):
    """Контроллер генерирует страницу blog_list.html, на которой представлены все публикации, хранящиеся в
    модели Blog. В странице есть пагинация, которая отображает до 3 публикаций на одной странице."""

    paginate_by = 3
    model = Blog
    extra_context = {
        'title': 'Блог'
    }


class BlogCreateView(LoginRequiredMixin, CreateView):
    """Контроллер создает форму, которая позволяет пользователю добавить публикацию на основе модели Blog. При успешном
    добавлении произойдет переадресация на страницу blog_list.html."""

    model = Blog
    form_class = BlogForm
    success_url = reverse_lazy('blog:blog_list')
    extra_context = {
        'title': 'Создание публикации'
    }

    def form_valid(self, form):
        """Метод при успешной генерации формы присваивает публикации создателя — текущего пользователя."""

        if form.is_valid():
            self.object = form.save()
            self.object.user_blog = self.request.user
            self.object.save()

        return super().form_valid(form)


class BlogDetailView(LoginRequiredMixin, DetailView):
    """Контроллер генерирует страницу blog_detail.html, на которой представлена информация о конкретной публикации."""

    model = Blog

    def get_object(self, queryset=None):
        """Метод инкрементирует поле view_count на 1 для конкретной публикации при обращениий к ней. Если view_count
        равняется 100, то пользователь получит письмо на указанный электронный адрес с поздравлением."""

        # Обращение к текущему объекту модели Blog
        self.object = super().get_object(queryset)
        self.object.view_count += 1
        self.object.save()

        # Создание заголовка и тела сообщения для отправки на электронный адрес
        message = f'Поздравляем!\nВаша публикация "{self.object.title}" на сайте Sender набрала ' \
                  f'{self.object.view_count} просмотров!\n\n С уважением, Администрация сайта!'
        subject = 'Поздравление от сайта Catalogue'

        # Объявление получателя сообщения
        recipient = self.object.email

        # Отправка сообщения пользователю, если количество просмотров равно 100
        if self.object.view_count == 100:
            send_mail(subject, message, settings.EMAIL_HOST_USER, (recipient,))
        return self.object

    def get_context_data(self, **kwargs):
        """Метод добавляет в контекст ключ title со значением — название текущей публикации и ключ blog_user с
        значением — создатель текущей публикации."""

        context = super().get_context_data(**kwargs)
        blog_title = Blog.objects.get(pk=self.kwargs.get('pk'))
        context['title'] = blog_title.title
        context['blog_user'] = self.object.user_blog
        return context


class BlogUpdateView(LoginRequiredMixin, UpdateView):
    """Контроллер на основе шаблона blog_form.html позволяет редактировать публикацию по модели Blog."""

    model = Blog
    form_class = BlogForm

    def get_success_url(self):
        """Метод возвращает страницу blog_detail.html при успешном обновлении публикации."""

        return reverse('blog:blog_detail', args=[self.object.id])

    def form_valid(self, form):
        """Метод возвращает только валидную форму. Объекты в модели Blog могут изменять только авторизованные
        пользатели, к тому же пользователи не могут изменять публикации, создателями которых они не являются."""

        if form.is_valid():
            self.object = form.save()
            if not self.request.user.is_superuser:
                self.object.user_blog = self.request.user
                self.object.save()

        return super().form_valid(form)

    def get_object(self, queryset=None):
        """Возвращает объект модели только в том случае, если пользователь обладает расширенными права доступа
        или сам является создателем блога. """

        self.object = super().get_object(queryset)
        if self.request.user == self.object.user_blog or self.request.user.is_superuser:
            return self.object
        else:
            raise Http404

    def get_context_data(self, **kwargs):
        """Метод добавляет в контекст шаблонную переменную blog_user с привязанным к текущей публикации
       пользователем, и переменную title с названием текущей страницы."""

        context_data = super().get_context_data(**kwargs)
        context_data['blog_user'] = self.object.user_blog
        context_data['title'] = 'Изменение'
        return context_data


class BlogDeleteView(LoginRequiredMixin, DeleteView):
    """Контроллер на основе шаблона blog_confirm_delete.html позволяет удалять строки из модели Blog.
    При успешном удалении произойдет переадресация на страницу blog_list.html."""

    model = Blog
    success_url = reverse_lazy('blog:blog_list')
    extra_context = {
        'title': 'Удаление публикации'
    }

    def get_object(self, queryset=None):
        """Возвращает объект модели только в том случае, если пользователь обладает расширенными права доступа
        или сам является создателем блога. """

        self.object = super().get_object(queryset)
        if self.request.user == self.object.user_blog or self.request.user.is_superuser:
            return self.object
        else:
            raise Http404
