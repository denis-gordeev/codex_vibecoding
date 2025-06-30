extends CharacterBody2D

export(Array, Resource) var abilities

func use_ability(index: int):
    if index >= 0 and index < abilities.size():
        abilities[index].activate(self)
