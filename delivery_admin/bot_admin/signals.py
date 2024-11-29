from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import OrderTable

from bot_admin.bot import send_order_dlv
from bot_admin.enums import OrderStatus, TypeOrderUpdate

from datetime import datetime


@receiver (pre_save, sender=OrderTable)
def track_changes(sender, instance, **kwargs):
    print(instance)
    instance.updated = False
    instance.type_update = datetime.now()
    # Проверяем, был ли объект уже сохранен в базе данных
    if instance.pk:
        # Получаем предыдущее состояние объекта из базы данных
        old_instance = sender.objects.get (pk=instance.pk)

        # Сравниваем значения полей предыдущего и нового состояний объекта
        for field in instance._meta.fields:
            old_value = getattr (old_instance, field.attname)
            new_value = getattr (instance, field.attname)

            # Если значения различаются, значит поле было изменено
            if old_value != new_value:
                if field.name == 'f':
                    print(f' {instance.f}')
                    instance.g = OrderStatus.ACTIVE.value
                    instance.type_update = TypeOrderUpdate.STATE.value
                    send_order_dlv(name=instance.f, order_info=instance)
                    break

                elif field.name == 'g' and instance.g == OrderStatus.NEW.value:
                    instance.d = None
                    instance.e = None
                    instance.f = '-'
                    instance.g = OrderStatus.NEW.value
                    instance.type_update = TypeOrderUpdate.STATE.value
                    print (instance)
                    print('edited')
                    break
                print (f"Field '{field.name}' was changed from '{old_value}' to '{new_value}'")
