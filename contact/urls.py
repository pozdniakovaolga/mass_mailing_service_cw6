from django.urls import path
from contact.views import ContactListView, ContactCreateView
from contact.views import ContactDetailView, ContactUpdateView, ContactDeleteView
from contact.apps import ContactConfig

app_name = ContactConfig.name

urlpatterns = [
    path('list/', ContactListView.as_view(), name='contact_list'),
    path('create/', ContactCreateView.as_view(), name='contact_create'),
    path('view/<int:pk>/', ContactDetailView.as_view(), name='contact_detail'),
    path('edit/<int:pk>/', ContactUpdateView.as_view(), name='contact_edit'),
    path('delete/<int:pk>/', ContactDeleteView.as_view(), name='contact_delete'),
]
