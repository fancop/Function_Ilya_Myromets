import os
from random import randint, choice

first_names = ("Жран", "Дрын", "Брысь", "Жлыг")
last_names = ("Ужасный", "Зловонный", "Борзый", "Кровавый")


def make_hero(
        name=None,
        hp_now=None,
        hp_max=None,
        lvl=1,
        xp_now=0,
        weapon=None,
        shield=None,
        attack=1,
        defence=1,
        luck=1,
        money=None,
        inventory=None,
) -> dict:
    if not name:
        name = choice(first_names) + " " + choice(last_names)

    if not hp_now:
        hp_now = randint(1, 100)

    if not hp_max:
        hp_max = hp_now

    xp_next = lvl * 100

    if money is None:
        money = randint(0, 100)

    if not inventory:
        inventory = []

    if not weapon:
        weapon = {
            "тип": "оружие",
            "название": "Обычный меч",
            "свойство": "атака",
            "модификатор": 3,
            "цена": 100,
        }

    return {
        "имя": name,
        "здоровье": hp_now,
        "здоровье макс": hp_max,
        "уровень": lvl,
        "опыт": xp_now,
        "опыт след": xp_next,
        "оружие": weapon,
        "щит": shield,
        "атака": attack,
        "защита": defence,
        "удача": luck,
        "деньги": money,
        "инвентарь": inventory
    }


def show_item(item: dict) -> None:
    """
    Показывает предмет
    """
    if item:
        if item['модификатор'] >= 0:
            print(f"{item['название']} +{item['модификатор']} {item['свойство']}")
        else:
            print(f"{item['название']} {item['модификатор']} {item['свойство']}")
    else:
        print("-пусто-")


def equip_item(hero: dict) -> None:
    """
    Показывает пронумерованные предметы
    Выбрать предмет

    """
    pass


def recalculate_stats(hero: dict) -> None:
    weapon = hero['оружие']
    shield = hero['щит']
    if weapon:
        hero['атака'] += weapon['модификатор']
    if shield:
        hero['защита'] += shield['модификатор']


def show_inventory(inventory: list) -> None:
    print("предметы: ")
    for item in inventory:
        show_item(item)


def show_hero(hero: list) -> None:
    print("имя:", hero['имя'])
    print("здоровье:", hero['здоровье'], "/", hero['здоровье макс'])
    print("уровень:", hero['уровень'])
    print("опыт:", hero['опыт'], "/", hero['опыт след'])
    print("оружие:", end=" ")
    show_item(hero['оружие'])
    print("щит:", end=" ")
    show_item(hero['щит'])
    print("атака:", hero['атака'])
    print("защита:", hero['защита'])
    print("удача:", hero['удача'])
    print("деньги:", hero['деньги'])
    show_inventory(hero['инвентарь'])
    print("")


def levelup(hero: list) -> None:
    """
    TODO: что растет с уровнем?
    """
    while hero['опыт'] >= hero['опыт след']:
        hero['уровень'] += 1
        hero['опыт след'] = hero['уровень'] * 100
        print(f"\n{hero['имя']} получил {hero['уровень']} уровень\n")


def buy_item(hero: list, price: int, item: str) -> None:
    """
    Покупает предмет item за price монет и кладет его в инвентарь героя
    """
    os.system("cls")
    if hero['деньги'] >= price:
        hero['деньги'] -= price
        hero['инвентарь'].append(item)
        print(f"{hero['имя']} купил {item} за {price} монет!")
    else:
        print(f"У {hero['имя']} нет столько монет! Не хватило {price - hero['деньги']}")
    input("\nНажмите ENTER чтобы продолжить")


def consume_item(hero: list) -> None:
    """
    Удаляет предмет из инвентаря по индексу и дает герою эффект этого предмета
    """
    os.system("cls")
    show_options(hero, hero['инвентарь'])
    idx = choose_option(hero, hero['инвентарь'])
    os.system("cls")
    if idx is not None:
        if idx <= len(hero['инвентарь']) - 1 and idx > -1:
            print(f"{hero['имя']} употребил {hero['инвентарь'][idx]}", end=", ")
            if hero['инвентарь'][idx] == "зелье здоровья":
                hero['здоровье'] += 10
                if hero['здоровье'] > hero['здоровье макс']:
                    hero['здоровье'] = hero['здоровье макс']
                print(f"{hero['имя']} восстановил здоровье")  # TODO: показать, сколько очков  здоровья восстановлено
            elif hero['инвентарь'][idx] == "зелье силы":
                hero['атака'] += 1
                print(f"{hero['имя']} прибавил 1 к силе атаки")
            else:
                print("Никакого эффекта")
            hero['инвентарь'].pop(idx)
    else:
        print("Нет такого индекса!")


def play_dice(hero: list, bet: str) -> None:
    """
    Ставка от 1 монеты до количества монет героя
    Игрок и казино бросаю кости, кто больше, то забирает ставку
    TODO: Как удача влияет на кости?
    """
    try:
        bet = int(bet)
    except ValueError:
        print("Ошибка! Ставка должна быть целым числом!")
    else:
        if bet > 0:
            if hero['деньги'] >= bet:
                hero_score = randint(2, 12)
                casino_score = randint(2, 12)
                print(f"{hero['имя']} выбросил {hero_score}")
                print(f"Трактирщик выбросил {casino_score}")
                if hero_score > casino_score:
                    hero['деньги'] += bet
                    print(f"{hero['имя']} выиграл {bet} монет")
                elif hero_score < casino_score:
                    hero['деньги'] -= bet
                    print(f"{hero['имя']} проиграл {bet} монет")
                else:
                    print("Ничья!")
            else:
                print(f"У {hero['имя']} нет денег на такую ставку!")
        else:
            print("Ставки начинаются от 1 монеты!")
        print("")
    input("\nНажмите ENTER чтобы продолжить")


def get_award(hero, enemy):
    os.system("cls")
    if hero['здоровье'] > 0 and enemy['здоровье'] <= 0:
        print(f"{hero['имя']} победил и получает в награду:")
        hero['опыт'] += enemy['опыт']
        print(enemy['опыт'], "опыта")
        hero['деньги'] += enemy['деньги']
        print(enemy['деньги'], "монет")
        print("и предметы: ", end="")
        for item in enemy['инвентарь']:
            print(item, end=", ")
        hero['инвентарь'] += enemy['инвентарь']
        levelup(hero)
    elif hero['здоровье'] <= 0 and enemy['здоровье'] > 0:
        print(f"{enemy['имя']} победил!")
        print("Игра должна закончиться тут!")
    else:
        print(f"{hero['имя']} и {enemy['имя']} пали в бою:(")
        print("Игра должна закончиться тут!")


def show_options(hero: list, options: list) -> None:
    for num, option in enumerate(options):
        print(f"{num}. {option}")


def choose_option(hero: list, options: list) -> int:
    """
    Принимает описание ситуации, где происходит выбор
    Принимает список возможных вариантов
    Спросить номер варианта у пользователя
    Проверяет, есть ли вариант пользователя в возможных вариантах
    Если есть, возвращает вариант пользователя
    """
    option = input("\nВведите номер варианта и нажмите ENTER: ")
    try:  # что пробуем сделать?
        option = int(option)
    except ValueError:  # сработает, если try вызвал ошибку
        print("Ошибка! Введите целое неотрицательное число")
    else:  # выполнится, если try без ошибки
        if option < len(options) and option > -1:
            return option
        else:
            print("Такой выбор невозможен!")


def visit_hub(hero: list) -> None:
    text = f"{hero['имя']} приехал в Хаб, осюда идут несколько дорог"
    options = [
        "Заглянуть в лавку алхимика",
        "Съездить в трактир",
        "Поехать на арену",
        "Выйти в главное меню"
    ]
    os.system("cls")
    show_hero(hero)
    print(text)
    show_options(hero, options)
    option = choose_option(hero, options)
    os.system("cls")
    if option == 0:
        return visit_shop(hero)
    elif option == 1:
        return visit_inn(hero)
    elif option == 2:
        return visit_arena(hero)
    else:
        print("Такой вариант еще не сделан")
    input("\nНажмите ENTER чтобы продолжить - из функции хаба")


def visit_shop(hero: list) -> None:
    text = f"{hero['имя']} зашел в лавку алхимика. Здесь продаются зелья и странно пахнет."
    options = [
        "Купить зелье здоровья за 10 монет",
        "Купить зелье силы за 20 монет",
        "Уйти в Хаб"
    ]
    os.system("cls")
    show_hero(hero)
    print(text)
    show_options(hero, options)
    option = choose_option(hero, options)
    os.system("cls")
    if option == 0:
        buy_item(hero, 10, "зелье здоровья")
        return visit_shop(hero)
    elif option == 1:
        buy_item(hero, 20, "зелье силы")
        return visit_shop(hero)
    elif option == 2:
        return visit_hub(hero)
    else:
        print("Такого варианта нет")
        input("\nНажмите ENTER чтобы продолжить")
        return visit_shop(hero)


def visit_inn(hero: list) -> None:
    text = f"{hero['имя']} приехал в трактир, хозин предлагает сыграть в кости на деньги."
    options = [
        "Сыграть в кости на деньги",
        "Уйти в Хаб"
    ]
    os.system("cls")
    show_hero(hero)
    print(text)
    show_options(hero, options)
    option = choose_option(hero, options)
    os.system("cls")
    if option == 0:
        bet = input("\nВведите, сколько монет поставить и нажмите ENTER: ")
        play_dice(hero, bet)
        return visit_inn(hero)
    elif option == 1:
        return visit_hub(hero)
    else:
        print("Такого варианта нет")
        return visit_inn(hero)


def visit_arena(hero: list) -> None:
    text = f"{hero['имя']} добрался до арены. Здесь можно сразиться с разюойником."
    options = [
        "Начать битву с разбойником",
        "Уйти в Хаб"
    ]
    os.system("cls")
    show_hero(hero)
    print(text)
    show_options(hero, options)
    option = choose_option(hero, options)
    os.system("cls")
    if option == 0:
        start_fight(hero)
    elif option == 1:
        return visit_hub(hero)
    else:
        return visit_arena(hero)  # FIXME: нет паузы для чтения ошибки с неправильным вариантом


def combat_turn(attacker, defender):
    if attacker['здоровье'] > 0:
        damage = attacker['атака']
        defender['здоровье'] -= damage
        print(f"{attacker['имя']} ударил {defender['имя']} на {damage} жизней!")


def start_fight(hero: list) -> None:
    """
    Зависит ли враг от уровня героя
    Формула аткаи и защиты?
    Можно ли выпить зелье в бою?
    TODO:
        не показывать опцию использования предмета, если предметов нет
        пауза между ходами, чтобы прочитать сообщения боя
    """
    enemy = make_hero(hp_now=5, xp_now=100, money=25, inventory=["меч орка", "щит орка"])
    options = [
        "Атаковать противника",
        "Использовать предмет из инвентаря"
    ]

    show_hero(hero)
    show_hero(enemy)

    while hero['здоровье'] > 0 and enemy['здоровье'] > 0:
        show_options(hero, options)
        option = choose_option(hero, options)
        os.system("cls")
        if option == 0:
            combat_turn(hero, enemy)
            combat_turn(enemy, hero)
            print("")
            show_hero(hero)
            show_hero(enemy)
        elif option == 1:
            consume_item(hero)
            combat_turn(enemy, hero)
            print("")
            show_hero(hero)
            show_hero(enemy)
    get_award(hero, enemy)
    input("\nНажмите ENTER чтобы продолжить")
    return visit_arena(hero)