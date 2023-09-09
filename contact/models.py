from django.db import models


class Contact(models.Model):
    """Клиент сервиса"""
    last_name = models.CharField(max_length=50, verbose_name='фамилия')
    first_name = models.CharField(max_length=50, verbose_name='имя')
    middle_name = models.CharField(max_length=50, verbose_name='отчество')
    email = models.EmailField(verbose_name='email')
    created_by = models.ForeignKey('users.User', on_delete=models.CASCADE, null=True, blank=True, verbose_name='автор')
    comment = models.CharField(max_length=250, verbose_name='комментарий')

    def __str__(self):
        return f'{self.last_name} {self.first_name}: {self.email}'

    class Meta:
        verbose_name = 'контакт'
        verbose_name_plural = 'контакты'
