from django.contrib import admin
from django.db.models import Max

from bot_admin import models as md


@admin.register(md.OrderTable)
class ViewOrderTable(admin.ModelAdmin):
    list_display = ['row_num', 'n', 'o', 'm', 'x', 'f', 'g']
    search_fields = ['n', 'o', 'row_num']
    list_filter = ('g', 'f',)
    ordering = ['-row_num']
    # ordering_fields = []

    def get_form(self, request, obj=None, **kwargs):
        # Получаем стандартную форму
        form = super ().get_form (request, obj, **kwargs)
        # Получаем максимальное значение из колонки row_num
        max_row_num = md.OrderTable.objects.aggregate (max_row=Max ('row_num')) ['max_row']
        # Если максимальное значение есть, увеличиваем на 1, иначе используем 1
        initial_row_num = max_row_num + 1 if max_row_num is not None else 1
        # Устанавливаем начальное значение для поля row_num в форме
        form.base_fields ['row_num'].initial = initial_row_num
        return form


@admin.register(md.ReportTable)
class ViewReportTable(admin.ModelAdmin):
    list_display = ['n', 'm', 'l']
    search_fields = ['n']
    list_filter = ['m', 'n']
    ordered = ['-row_num']
    # ordering_fields = []

    def report_text(self, obj):
        text = ''
        for row in obj.l:
            text += row
        return text

    report_text.short_description = 'Отчёт техт'


@admin.register(md.UserTable)
class ViewUserTable(admin.ModelAdmin):
    list_display = ['name', 'phone', 'company', 'role']
    search_fields = ['name']
    list_filter = ['company']
    ordered = ['-row_num', 'role']


@admin.register(md.ActionJournal)
class ViewActionTable(admin.ModelAdmin):
    list_display = ['dlv_name', 'created_at', 'action', 'comment']
    search_fields = ['dlv_name', 'action']
    list_filter = ['dlv_name', 'action']
    ordered = ['-created_at']


@admin.register(md.ErrorsJournal)
class ViewActionTable(admin.ModelAdmin):
    list_display = ['name', 'created_at', 'error']
    search_fields = ['name', 'error']
    list_filter = ['user_id', 'error']
    ordered = ['-created_at']

    def name(self, obj):
        user = md.UserTable.objects.filter (user_id=obj.user_id).first ()
        if not user:
            return None
        if user.name:
            return user.name
        else:
            return str (obj.user_id)

    name.short_description = 'Имя'
