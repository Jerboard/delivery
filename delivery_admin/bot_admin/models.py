from django.db import models
from django.contrib.postgres.fields import ArrayField

from datetime import datetime

from bot_admin import enums
from bot_admin import maps as mp
from delivery_admin.settings import DAY_FORM


# пользователи
class UserTable(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.BigIntegerField(unique=True)
    full_name = models.CharField(max_length=255)
    username = models.CharField(max_length=255, null=True, blank=True)
    role = models.CharField(max_length=255, null=True, blank=True, choices=mp.user_status)
    name = models.CharField(max_length=255, null=True, blank=True)
    company = models.CharField(max_length=255, null=True, blank=True, choices=mp.company_all)
    phone = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.full_name

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        db_table = 'users'
        managed = False


# заказы
class OrderTable(models.Model):
    id = models.AutoField('ID', primary_key=True)
    b = models.CharField('B Биток', max_length=255, null=True, blank=True)
    c = models.CharField('C Виновник отказа', max_length=255, null=True, blank=True)
    d = models.CharField('D Комментарий', max_length=255, null=True, blank=True)
    e = models.CharField('E Дата', max_length=255, default=datetime.now().strftime(DAY_FORM), null=True, blank=True)
    f = models.CharField('F Курьер', max_length=255, null=True, blank=True, choices=mp.dlvs)
    g = models.CharField('G Статус', max_length=255, choices=mp.order_status, default='new')
    h = models.CharField('H Исполнитель', max_length=255, null=True, blank=True)
    i = models.CharField('I Выдан', max_length=255, null=True, blank=True)
    j = models.CharField('J Принят', max_length=255, null=True, blank=True)
    k = models.CharField('K Оператор', max_length=255, null=True, blank=True)
    l = models.CharField('L Партнер', max_length=255, null=True, blank=True)
    m = models.TextField('M ФИО', null=True, blank=True)
    n = models.CharField('N Тел', max_length=255, null=True, blank=True)
    o = models.CharField('O Тел2', max_length=255, null=True, blank=True)
    p = models.TextField('P Бланк', null=True, blank=True)
    q = models.IntegerField('Q Цена')
    r = models.IntegerField('R Наценка')
    s = models.IntegerField('S Доп')
    clmn_t = models.IntegerField('T Доставка')
    u = models.IntegerField('U Кошелек')
    v = models.IntegerField('V Карта')
    w = models.CharField('W Метро', max_length=255, null=True, blank=True)
    x = models.TextField('X Адрес', null=True, blank=True)
    y = models.IntegerField('Y Скидка')
    z = models.CharField('Z Цена бланка', max_length=255, null=True, blank=True)
    aa = models.CharField('AA Итого с клиента', max_length=255, null=True, blank=True)
    ab = models.CharField('AB Примечания', max_length=255, null=True, blank=True)
    ac = models.CharField('AC Курьерская', max_length=255, null=True, blank=True, choices=mp.company_dlv)
    updated = models.BooleanField('Обновлено', default=False)
    time_update = models.DateTimeField('', auto_now_add=True)
    type_update = models.CharField('Тип обновления', max_length=255, default=enums.TypeOrderUpdate.ADD.value)
    comp_opr = models.CharField('Компания оператора', max_length=255, null=True, blank=True, choices=mp.company_opr)
    row_num = models.IntegerField('Строка')

    def __str__(self):
        return f'Заказ {self.row_num}'

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        db_table = 'orders_ggl'
        managed = False


# заказы
class WorkOrders(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.BigIntegerField()
    order_id = models.IntegerField()

    def __str__(self):
        return f'Заказ {self.order_id}'

    class Meta:
        verbose_name = 'Заказы в работе'
        verbose_name_plural = 'Заказы в работе'
        db_table = 'work_orders'
        managed = False


# отчёты
class ReportTable(models.Model):
    id = models.AutoField('ID', primary_key=True)
    b = models.IntegerField('B Расходы разные', default=0)
    c = models.IntegerField('C Связь / SIM', default=0)
    d = models.IntegerField('D Достависта', default=0)
    e = models.IntegerField('E Такси / Самокат / Транспорт', default=0)
    f = models.IntegerField('F Проездной', default=0)
    g = models.IntegerField('G МЦ', default=0)
    h = models.IntegerField('H Комус', default=0)
    i = models.IntegerField('I Почта / СДЭК', default=0)
    j = models.IntegerField('J Развоз', default=0)
    clmn_k = models.IntegerField('K Курьеры ЗП', default=0)
    l = ArrayField(verbose_name='L Траты курьеров', base_field=models.CharField(max_length=255), null=True, blank=True)
    # l = models.TextField('', null=True, blank=True)
    m = models.CharField('M Дата', max_length=255, null=True, blank=True)
    n = models.CharField('N Курьер', max_length=255, null=True, blank=True)
    o = models.IntegerField('O Отчёт курьера')
    p = models.CharField('P Сдал ЧЕК', max_length=255, null=True, blank=True)
    q = models.CharField('Q Сдал НАЛ', max_length=255, null=True, blank=True)
    r = models.IntegerField('R Баланс')
    in_google = models.BooleanField('В таблице', default=False)
    row_num = models.IntegerField('Строка')
    time_update = models.DateTimeField('Время обновления', auto_now=True)

    def __str__(self):
        return f'Отчёт {self.row_num}'

    class Meta:
        verbose_name = 'Отчёт'
        verbose_name_plural = 'Отчёты'
        db_table = 'report_ggl'
        managed = False


# действия пользователей
class ActionJournal(models.Model):
    id = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(null=True, blank=True)
    user_id = models.BigIntegerField(null=True, blank=True)
    dlv_name = models.CharField(max_length=100, null=True, blank=True)
    action = models.CharField(max_length=100, null=True, blank=True)
    comment = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.action

    class Meta:
        verbose_name = 'Журнал действий'
        verbose_name_plural = 'Журнал действий'
        db_table = 'action_journal'
        managed = False


# журнал ошибок
class ErrorsJournal(models.Model):
    id = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    user_id = models.BigIntegerField()
    error = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.error

    class Meta:
        verbose_name = 'Журнал ошибок'
        verbose_name_plural = 'Журнал ошибок'
        db_table = 'errors_journal'
        managed = False
