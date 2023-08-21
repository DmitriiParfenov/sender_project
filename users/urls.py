from django.contrib.auth.views import LogoutView, PasswordChangeDoneView
from django.urls import path

from users.apps import UsersConfig
from users.views import LoginView, RegisterUserView, verify_registration, user_reset_password, PasswordChangeView, \
    UserProfileUpdateView, user_profile_view, moderating_senders_view, ModeratorSenderUpdateView, \
    ModeratorUserUpdateView

app_name = UsersConfig.name

urlpatterns = [
    path('', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterUserView.as_view(), name='register'),
    path('<int:user_pk>/<slug:user_identity>/', verify_registration, name='verify_registration'),
    path('reset_password/', user_reset_password, name='reset_password'),
    path('profile/', UserProfileUpdateView.as_view(), name='profile'),
    path('change_password/', PasswordChangeView.as_view(), name='change_password'),
    path('password_change/done/', PasswordChangeDoneView.as_view(template_name='users/password_change_done.html'),
         name='password_change_done'),
    path('user_profile/', user_profile_view, name='user_profile'),
    path('moderating_page/', moderating_senders_view, name='moderating_page'),
    path('moderating_page/sender/<int:pk>/', ModeratorSenderUpdateView.as_view(), name='moderator_sender_update'),
    path('moderating_page/user/<int:pk>/', ModeratorUserUpdateView.as_view(), name='moderator_user_update'),
]
