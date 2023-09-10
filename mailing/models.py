from django.db import models


class Mailing(models.Model):
    """Рассылка"""

    #  варианты периодичности рассылки
    PERIOD_CHOICES = (
        ('ONCE', 'Единоразовая'),
        ('DAILY', 'Раз в день'),
        ('WEEKLY', 'Раз в неделю'),
        ('MONTHLY', 'Раз в месяц'),
    )

    #  варианты статуса рассылки
    STATUS_CHOICES = (
        ('CREATED', 'Создана'),
        ('STARTED', 'Запущена'),
        ('FINISHED', 'Завершена'),
    )

    message = models.ForeignKey('message.Message', on_delete=models.CASCADE, verbose_name='сообщение')
    contacts = models.ManyToManyField('contact.Contact', verbose_name='контакты')
    datetime_start = models.DateTimeField(verbose_name='время начала рассылки')
    datetime_finish = models.DateTimeField(verbose_name='время окончания рассылки')
    period = models.CharField(max_length=25, choices=PERIOD_CHOICES, default='DAILY', verbose_name='периодичность')
    status = models.CharField(max_length=25, choices=STATUS_CHOICES, default='CREATED', verbose_name='статус рассылки')
    created_by = models.ForeignKey('users.User', on_delete=models.CASCADE, null=True, blank=True, verbose_name='автор')

    def __str__(self):
        return f'{self.datetime_start}-{self.datetime_finish}, {self.period}, {self.status}'

    class Meta:
        verbose_name = 'рассылка'
        verbose_name_plural = 'рассылки'


class Log(models.Model):
    """Логи рассылки"""
    mailing = models.ForeignKey('Mailing', on_delete=models.CASCADE, verbose_name='рассылка')
    contacts = models.ForeignKey('contact.Contact', on_delete=models.CASCADE, verbose_name='контакты')
    try_time = models.DateTimeField(auto_now_add=True, verbose_name='дата и время последней попытки')
    try_status = models.CharField(max_length=50, verbose_name='статус попытки')
    server_answer = models.CharField(max_length=250, null=True, blank=True, verbose_name='ответ почтового сервера')

    def __str__(self):
        return f'{self.try_time}: {self.try_status}'

    class Meta:
        verbose_name = 'лог'
        verbose_name_plural = 'логи'
