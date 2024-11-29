from enum import Enum


class TypeOrderUpdate(str, Enum):
    EDIT = 'edit'
    ADD = 'add'
    ADD_OPR = 'add_opr'
    STATE = 'state'
    EDIT_COST = 'edit_cost'
    EDIT_COST_DELIVERY = 'edit_cost_dlv'
    NOT_COME = 'not_come'
    UP_DATE = 'up_date'
    TRANS = 'trans'


class OrderStatus(str, Enum):
    NEW = 'new'
    SUC = 'success'
    ACTIVE = 'active'
    ACTIVE_TAKE = 'active_take'
    REF = 'refuse'
    TAKE = 'take'
    SUC_TAKE = 'success_take'
    REF_TAKE = 'refuse_take'
    NOT_COME = 'not_come'
    REMAKE = 'remake'
    SEND = 'send'
