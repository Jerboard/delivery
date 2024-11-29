

order_status = (
    ('new', 'Новый'),
    ('success', 'Доставлен'),
    ('active', 'На руках'),
    ('active_take', 'На руках (забрать)'),
    ('refuse', 'Отказ'),
    ('take', 'Забор'),
    ('success_take', 'Забран'),
    ('refuse_take', 'Отказан'),
    ('not_come', 'Не явился'),
    ('remake', 'Переделка'),
    ('send', 'Отправлен')
)


user_status = (
    ('dlv', 'Курьер'),
    ('opr', 'Оператор'),
    ('own', 'Владелец'),
)

company_dlv = (
    ('post', 'Почта / СДЭК'),
    ('master', 'Мастер'),
    ('putilin', 'Путилин'),
    ('master_spb', 'Мастер СПБ')
)

company_opr = (
    ('vlada', 'Влада'),
    ('vera', 'Вера'),
    ('boss', 'Руководитель')
)

company_all = company_dlv + company_opr

dlvs = (
    ("Женька тестер", "Женька тестер"),
    ("Димка тестер", "Димка тестер"),
    ("Рустам", "Рустам"),
    ("Омар", "Омар"),
    ("Мел", "Мел"),
    ("Мияги", "Мияги"),
    ("Нови", "Нови"),
    ("Ян", "Ян"),
    ("Белка", "Белка"),
    ("Альберто", "Альберто"),
    ("Бур", "Бур"),
    ("Гиви", "Гиви"),
    ("Димас", "Димас"),
    ("Евгений", "Евгений"),
    ("Конь", "Конь"),
    ("Соня", "Соня"),
    ("Твердый", "Твердый"),
    ("Тэйл", "Тэйл"),
    ("Чико", "Чико"),
    ("Джон", "Джон"),
    ("Кан", "Кан"),
    ("Робот", "Робот"),
    ("Сармат", "Сармат"),
    ("Андро", "Андро"),
    ("Веталь", "Веталь"),
    ("Палыч", "Палыч"),
    ("Роман", "Роман"),
    ("Сэлюк", "Сэлюк"),
    ("Тичер", "Тичер"),
    ("Фрик", "Фрик"),
    ("Хан", "Хан"),
    ("Шон", "Шон"),
    ("Ярик", "Ярик"),
)