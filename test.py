from main import *

player = make_hero(name="Вася Питонов", inventory=["зелье"], hp_now=100, money=1000)

game = True
while game:
    visit_hub(player)
