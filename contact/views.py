from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from contact.models import Contact
from django.urls import reverse_lazy
from contact.forms import ContactForm
from mailing.views import OwnerRequiredMixin, ManagerRequiredMixin


class ContactCreateView(LoginRequiredMixin, CreateView):
    """Контроллер создания клиента сервиса"""
    model = Contact
    form_class = ContactForm
    success_url = reverse_lazy('contact:contact_list')

    def form_valid(self, form):  # автоматическое формирование автора
        if form.is_valid():
            product = form.save()
            product.created_by = self.request.user
            product.save()

        return super().form_valid(form)


class ContactListView(ListView):
    """Контроллер просмотра списка клиентов сервиса"""
    model = Contact
    paginate_by = 15  # количество элементов на одну страницу
    ordering = ['-id']

    def dispatch(self, request, *args, **kwargs):  # запрет доступа без авторизации
        if self.request.user.is_anonymous:
            return redirect('mailing:access_error')
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self, *args, **kwargs):  # отображение только тех контактов, которые созданы пользователем
        queryset = super().get_queryset()
        if not self.request.user.is_manager:  # менеджеру доступны все контакты
            queryset = queryset.filter(created_by=self.request.user.pk)
        return queryset


class ContactDetailView(OwnerRequiredMixin, ManagerRequiredMixin, DetailView):
    """Контроллер просмотра отдельного клиента сервиса"""
    model = Contact


class ContactUpdateView(OwnerRequiredMixin, UpdateView):
    """Контроллер редактирования клиента сервиса"""
    model = Contact
    form_class = ContactForm
    success_url = reverse_lazy('contact:contact_list')


class ContactDeleteView(OwnerRequiredMixin, DeleteView):
    """Контроллер удаления клиента сервиса"""
    model = Contact
    success_url = reverse_lazy('contact:contact_list')
