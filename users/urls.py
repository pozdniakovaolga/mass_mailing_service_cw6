from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from users.apps import UsersConfig
from users.views import RegisterView, RegistrationEmailSentView, ProfileView
from users.views import VerificationFailedView, VerificationSuccessView, ActivateView
from users.views import UserListView, UserUpdateView

app_name = UsersConfig.name


urlpatterns = [
    path('', LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('register_need_verify', RegistrationEmailSentView.as_view(), name='register_need_verify'),
    path('verification_failed/', VerificationFailedView.as_view(), name='verification_failed'),
    path('verification_success/', VerificationSuccessView.as_view(), name='verification_success'),
    path('activate/<uidb64>/<token>', ActivateView.as_view(), name='activate'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('list/', UserListView.as_view(), name='user_list'),
    path('edit/<int:pk>/', UserUpdateView.as_view(), name='user_edit'),
]
