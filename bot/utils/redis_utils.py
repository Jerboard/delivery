# # from init import redis_client
# from enums import RedisKey
#
# import json
# import typing as t
# from datetime import timedelta
#
#
# # добавляет данные в редис с временем жизни
# def add_data_in_redis(key: str, data: t.Union[dict, list]) -> None:
#     live_time = timedelta(days=2)
#     save_data = json.dumps(data)
#     redis_client.setex (name=key, time=live_time, value=save_data)
#     # redis_client.set (key, save_data)
#
#
# # извлекает данные из редиса
# def get_redis_data(key: str) -> t.Union[dict, list]:
#     data = redis_client.get (key)
#     if data:
#         return json.loads (data.decode ("utf-8"))
#     else:
#         return []
#
#
# # возвращает все заказы курьера
# def get_all_dlv_orders(user_id: int) -> list:
#     key = f'{RedisKey.ORDERS.value}-{user_id}'
#     return get_redis_data(key)
#
#
# # удаляет все заказы курьера
# def clear_order_dlv_redis(user_id: int) -> None:
#     key = f'{RedisKey.ORDERS.value}-{user_id}'
#     orders = []
#     add_data_in_redis(key=key, data=orders)
#
#
# # добавляет заказ курьеру
# def add_order_dlv_redis(user_id: int, order_id: int) -> None:
#     key = f'{RedisKey.ORDERS.value}-{user_id}'
#     orders: list = get_redis_data(key)
#     orders.append(order_id)
#     print (orders)
#     add_data_in_redis(key=key, data=orders)
#
#
# # добавляет заказ курьеру
# def remove_order_dlv_redis(user_id: int, order_id: int) -> None:
#     key = f'{RedisKey.ORDERS.value}-{user_id}'
#     orders: list = get_redis_data(key)
#     orders.remove(order_id)
#     add_data_in_redis(key=key, data=orders)
