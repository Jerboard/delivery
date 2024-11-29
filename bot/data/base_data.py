from config import DEBUG
from enums import OrderStatus, CompanyDLV, CompanyOPR, OrderAction, Letter


company_dlv = {
    CompanyDLV.POST.value: 'Почта / СДЭК',
    CompanyDLV.MASTER.value: 'Мастер',
    CompanyDLV.PUTILIN.value: 'Путилин',
    CompanyDLV.MASTER_SPB.value: 'Мастер СПБ'
}

company_dlv_opr_bt = {
    CompanyDLV.MASTER.value: 'Мастер МСК',
    CompanyDLV.PUTILIN.value: 'Путилин МСК',
    CompanyDLV.MASTER_SPB.value: 'Мастер СПБ'
}

company_dlv_revers = {
    'Почта / СДЭК': CompanyDLV.POST.value,
    'Мастер': CompanyDLV.MASTER.value,
    'Путилин': CompanyDLV.PUTILIN.value,
    'Мастер СПБ': CompanyDLV.MASTER_SPB.value
}

company_opr = {
    CompanyOPR.VLADA.value: 'Влада',
    CompanyOPR.VERA.value: 'Вера',
    CompanyOPR.NADIA.value: 'Надежда',
    CompanyOPR.BOSS.value: 'Руководитель'
}

order_status_data = {
    OrderStatus.NEW.value: '',
    OrderStatus.SUC.value: 'доставлен',
    OrderStatus.ACTIVE.value: 'на руках',
    OrderStatus.ACTIVE_TAKE.value: 'на руках (забрать)',
    OrderStatus.NOT_COME.value: 'не явился',
    OrderStatus.REF.value: 'отказ',
    OrderStatus.TAKE.value: 'принят',
    OrderStatus.SUC_TAKE.value: 'забран',
    OrderStatus.REF_TAKE.value: 'отказан',
    OrderStatus.REMAKE.value: 'переделка',
    OrderStatus.SEND.value: 'отправлен',
    '': OrderStatus.NEW.value,
    'доставлен': OrderStatus.SUC.value,
    'на руках': OrderStatus.ACTIVE.value,
    'на руках (забрать)': OrderStatus.ACTIVE_TAKE.value,
    'не явился': OrderStatus.NOT_COME.value,
    'отказ': OrderStatus.REF.value,
    'принят': OrderStatus.TAKE.value,
    'забран': OrderStatus.SUC_TAKE.value,
    'отказан': OrderStatus.REF_TAKE.value,
    'переделка': OrderStatus.REMAKE.value,
    'отправлен': OrderStatus.SEND.value,
}

order_mark = {
    OrderStatus.NEW.value: '⚪️',
    OrderStatus.SUC.value: '🟢',
    OrderStatus.ACTIVE.value: '🟡',
    OrderStatus.ACTIVE_TAKE.value: '🟡',
    OrderStatus.REF.value: '🔴',
    OrderStatus.TAKE.value: '🔵',
    OrderStatus.SUC_TAKE.value: '🟢',
    OrderStatus.REF_TAKE.value: '🔴',
    OrderStatus.REMAKE.value: '🔴',
    OrderStatus.SEND.value: '🟠',
}


expensis_dlv = {
    1: {'emoji': '💵', 'text': 'ЗП', 'column': 'k', 'photo': 0, 'comment': 0},
    2: {'emoji': '📱', 'text': 'Связь', 'column': 'c', 'photo': 1, 'comment': 0},
    3: {'emoji': '📦', 'text': 'Достависта', 'column': 'd', 'photo': 1, 'comment': 0},
    4: {'emoji': '🚕', 'text': 'Такси', 'column': 'e', 'photo': 1, 'comment': 0},
    5: {'emoji': '🚌', 'text': 'Транспорт', 'column': 'e', 'photo': 1, 'comment': 0},
    6: {'emoji': '🛴', 'text': 'Самокат', 'column': 'e', 'photo': 1, 'comment': 0},
    7: {'emoji': '📬', 'text': 'Забор от писаря', 'column': 'e', 'photo': 1, 'comment': 0},
    8: {'emoji': '🚃', 'text': 'Проездной Метро', 'column': 'f', 'photo': 1, 'comment': 0},
    9: {'emoji': '🏥', 'text': 'МЦ', 'column': 'g', 'photo': 0, 'comment': 1},
    10: {'emoji': '🖇', 'text': 'Канцелярия', 'column': 'h', 'photo': 1, 'comment': 0},
    11: {'emoji': '✉️', 'text': 'Почта / СДЭК', 'column': 'i', 'photo': 0, 'comment': 0},
    12: {'emoji': '💰', 'text': 'Премия', 'column': 'b', 'photo': 0, 'comment': 0},
    13: {'emoji': '🏧', 'text': 'Подписка на переводы', 'column': 'b', 'photo': 1, 'comment': 0},
    14: {'emoji': '💸', 'text': 'Разное', 'column': 'b', 'photo': 0, 'comment': 1},
}


letters = {
    Letter.D.value: 'День',
    Letter.V.value: 'Вечер',
    Letter.A.value: 'Адрес',
}


order_actions = {
    OrderAction.COST.value: 'Скидка',
    OrderAction.DELI.value: 'Доставка',
}

if DEBUG:
    work_chats = {
        f'take_{CompanyDLV.MASTER.value}': -1001669708234,
        f'take_{CompanyDLV.PUTILIN.value}': -1001669708234,
        f'take_{CompanyDLV.MASTER_SPB.value}': -1001669708234,
        'group_expenses': -1001669708234,
        'group_report': -1001669708234,
        f'refuse_{CompanyDLV.MASTER.value}': -1001669708234,
        f'refuse_{CompanyDLV.PUTILIN.value}': -1001669708234,
        f'refuse_{CompanyDLV.MASTER_SPB.value}': -1001669708234,
        f'refuse_{CompanyDLV.POST.value}': -1001669708234,
        f'report_{CompanyDLV.MASTER.value}': -1001669708234,
        f'report_{CompanyDLV.PUTILIN.value}': -1001669708234,
        f'report_{CompanyDLV.MASTER_SPB.value}': -1001669708234,
        f'report_{CompanyDLV.POST.value}': -1001669708234,
        f'post_{CompanyOPR.VLADA.value}': -1001669708234,
        f'post_{CompanyOPR.VERA.value}': -1001669708234,
    }
else:
    work_chats = {
        f'take_{CompanyDLV.MASTER.value}': -1001838764189,
        f'take_{CompanyDLV.PUTILIN.value}': -1001864910335,
        f'take_{CompanyDLV.MASTER_SPB.value}': -1001653186290,
        'group_expenses': -1001903349475,
        'group_report': -1001863016934,
        f'refuse_{CompanyDLV.MASTER.value}': -1001997852647,
        f'refuse_{CompanyDLV.PUTILIN.value}': -1002141489538,
        f'refuse_{CompanyDLV.MASTER_SPB.value}': -1002097241384,
        f'refuse_{CompanyDLV.POST.value}': -1002117858384,
        f'report_{CompanyDLV.MASTER.value}': -1001863016934,
        f'report_{CompanyDLV.PUTILIN.value}': -1001887194825,
        f'report_{CompanyDLV.MASTER_SPB.value}': -1001971855032,
        f'report_{CompanyDLV.POST.value}': -1002062614241,
        f'post_{CompanyOPR.VLADA.value}': -1002234546766,
        f'post_{CompanyOPR.VERA.value}': -1002199877687,
    }
