from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import redirect, reverse
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from config import settings
from mailing.views import ManagerRequiredMixin
from users.forms import UserRegisterForm, UserProfileForm, UserStatusForm
from django.views.generic import CreateView, UpdateView, TemplateView, View, ListView
from users.models import User
from users.token import email_verification_token
from django.core.mail import send_mail


class RegisterView(CreateView):
    """Контроллер регистрации пользователя"""
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:register_need_verify')

    def form_valid(self, form):  # Отправка ссылки для верификации email на почту
        if form.is_valid():
            user = form.save()
            user.is_active = False  # Деактивация аккаунта до процедуры верификации по почте
            user.save()
            current_site = get_current_site(self.request)  # Получение адреса сайта для формирования ссылки
            subject = "Активация аккаунта"
            body = render_to_string(
                'users/email_verification.html',
                {'domain': current_site,
                 'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                 'token': email_verification_token.make_token(user),
                 }
            )
            send_mail(
                subject=subject,
                html_message=body,
                message=user.email,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[user.email]
            )

        return super().form_valid(form)


class RegistrationEmailSentView(TemplateView):
    """Контроллер сообщения о необходимости активации аккаунта"""
    template_name = 'users/email_registration_sent.html'


class ProfileView(LoginRequiredMixin, UpdateView):
    """Контроллер редактирования профиля пользователя"""
    model = User
    form_class = UserProfileForm
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user


class ActivateView(View):
    """Контроллер активации аккаунта через почту"""

    @staticmethod
    def get_user_from_email_verification_token(uidb64, token: str):
        """Метод извлечения данных пользователя из хэша"""
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = get_user_model().objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, get_user_model().DoesNotExist):
            return None

        if user is not None and email_verification_token.check_token(user, token):
            return user
        else:
            return None

    def get(self, request, uidb64, token):
        """Метод активации аккаунта через email"""
        user = self.get_user_from_email_verification_token(uidb64, token)
        if user is not None:
            user.is_active = True
            user.save()
            return redirect(reverse('users:verification_success'))
        else:
            return redirect(reverse('users:verification_failed'))


class VerificationFailedView(TemplateView):
    """Контроллер ошибки верификации"""

    template_name = 'users/email_verification_failed.html'


class VerificationSuccessView(TemplateView):
    """Контроллер успешной верификации"""

    template_name = 'users/email_verification_success.html'


class UserListView(ListView):
    """Контроллер просмотра списка пользователей"""
    model = User
    paginate_by = 9  # количество элементов на одну страницу
    ordering = ['-id']

    def dispatch(self, request, *args, **kwargs):  # доступ к списку только для менеджера
        if self.request.user.is_anonymous:
            return redirect('mailing:access_error')
        elif not self.request.user.is_manager:
            return redirect('mailing:access_error')
        return super().dispatch(request, *args, **kwargs)


class UserUpdateView(ManagerRequiredMixin, UpdateView):
    """Контроллер редактирования пользователя"""

    model = User
    form_class = UserStatusForm
    success_url = reverse_lazy('users:user_list')
