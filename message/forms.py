from django import forms
from message.models import Message
from contact.forms import StyleFormMixin


class MessageForm(StyleFormMixin, forms.ModelForm):
    """Форма для создания/редактирования сообщения"""

    class Meta:
        model = Message
        exclude = ('created_by',)
