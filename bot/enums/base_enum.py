from enum import Enum


class UserRole(str, Enum):
    DLV = 'dlv'
    OPR = 'opr'
    OWN = 'own'


class OrderStatus(str, Enum):
    NEW = 'new'
    SUC = 'success'
    SUC_TAKE = 'success_take'
    ACTIVE = 'active'
    ACTIVE_TAKE = 'active_take'
    REF = 'refuse'
    TAKE = 'take'
    REF_TAKE = 'refuse_take'
    NOT_COME = 'not_come'
    REMAKE = 'remake'
    SEND = 'send'


active_status_list = [
    OrderStatus.ACTIVE.value,
    OrderStatus.ACTIVE_TAKE.value,
    OrderStatus.SEND.value]
done_status_list = [OrderStatus.SUC.value, OrderStatus.SUC_TAKE.value]
ref_status_list = [OrderStatus.REF.value, OrderStatus.REF_TAKE.value, OrderStatus.REMAKE.value]


class OrderAction(str, Enum):
    SUC = 'success'
    NOT_COME = 'not_come'
    SUC_TAKE = 'success_take'
    REF = 'refuse'
    TRANS = 'trans'
    COST = 'edit_cost'
    DELI = 'edit_cost_dlv'


class DataKey(str, Enum):
    ADD_OPR_ORDER = 'add_opr_order'
    ORDERS = 'dlv_orders'


class UserActions(str, Enum):
    TAKE_ORDER = 'Взял заказ'
    TAKE_ORDER_TAKE = 'Взял заказ (забор)'
    SEND_POST_ORDER = 'Отправил заказ (почта)'
    REFUSE_ORDER = 'Отказался от заказа'
    SUCCESS_ORDER = 'Заказ выполнен'
    REFUSE_TAKE_ORDER = 'Отказался от забора'
    SUCCESS_TAKE_ORDER = 'Забор выполнен'
    NOT_COME_ORDER = 'Клиент не вышел'
    ADD_DISCOUNT = 'Добавил скидку'
    ADD_DISCOUNT_DLV = 'Изменил стоимость доставки'
    TRANSFER_ORDER = 'Передал заказ'
    TRANSFER_ORDER_OWN = 'Назначен заказ'
    ADD_EXPENSES = 'Добавил трату'
    VIEW_REPORT = 'Просмотрел отчёт'
    SEND_REPORT = 'Отправил отчёт'
    ADD_TAKE_ORDER = 'Добавил заказ на забор'


class TypeOrderUpdate(str, Enum):
    EDIT = 'edit'
    ADD = 'add'
    ADD_OPR = 'add_opr'
    STATE = 'state'
    EDIT_COST = 'edit_cost'
    EDIT_COST_DELIVERY = 'edit_cost_dlv'
    NOT_COME = 'not_come'
    UPDATE_ROW = 'update'
    TRANS = 'trans'
    PICKUP = 'pickup'


class SearchType(str, Enum):
    PHONE = 'phone'
    NAME = 'name'
    METRO = 'metro'
    POST = 'post'


class ShortText (str, Enum):
    ACTIVE = 'active_orders'
    FREE = 'free_orders'
    REPORT = 'report'


class CompanyDLV (str, Enum):
    POST = 'post'
    MASTER = 'master'
    PUTILIN = 'putilin'
    MASTER_SPB = 'master_spb'


class CompanyOPR (str, Enum):
    VLADA = 'vlada'
    VERA = 'vera'
    NADIA = 'nadia'
    BOSS = 'boss'

'''
Влада - Цифры (1. 2. 3. 4. 5. и так далее)
Вера - Буквы Русские (А Б В Г Д …)
Надежда - Буквы Латинские (F V W Z …)
Руковолители - остальные ребята, которые из руководящих

'''

class Letter (str, Enum):
    D = 'Д'
    V = 'В'
    A = 'А'


class TypeOrderButton (str, Enum):
    BASE = 'base'
    TAKE = 'take'
    PICKUP = 'pickup'


class KeyWords(str, Enum):
    NOT_COME = 'не явился'
    ID = 'ids'
    REPORT = 'report_date'


class Action(str, Enum):
    ADD = 'add'
    DEL = 'del'
