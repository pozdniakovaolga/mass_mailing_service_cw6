from django import forms
from contact.models import Contact


class StyleFormMixin:
    """Миксин стилизации формы"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class ContactForm(StyleFormMixin, forms.ModelForm):
    """Форма для создания/редактирования клиента сервиса"""
    class Meta:
        model = Contact
        exclude = ('created_by',)
