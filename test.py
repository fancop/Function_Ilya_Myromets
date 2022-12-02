from main import *

player = make_hero(name="Вася", hp_now=100, attack=10, inventory=[])

game = True
while game:
    visit_hub(player)