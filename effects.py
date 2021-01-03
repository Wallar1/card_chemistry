import uuid

from utilities import slow_print


class Effect:
    def __init__(self, compound, enemy, damage, turns_until_effect):
        self.compound = compound
        self.enemy = enemy
        self.damage = damage
        self.turns_until_effect = turns_until_effect
        self.uuid = uuid.uuid4()

    def call(self):
        raise NotImplementedError


class Poison(Effect):
    def __init__(self, compound=None, enemy=None, damage=0):
        turns_until_effect = 0
        super(Poison, self).__init__(compound, enemy, damage, turns_until_effect)

    def __str__(self):
        return "Poison: does {} damage every turn".format(self.damage)

    def call(self):
        slow_print('{} poison does {} damage to {}'.format(self.compound.name, self.damage, self.enemy.name))
        self.enemy.damage(self.damage)
        self.damage -= 1
        if self.damage <= 0:
            self.enemy.remove_effect(self.uuid)
            del self


class Doom(Effect):
    def __init__(self, compound=None, enemy=None, damage=0):
        turns_until_effect = 4
        super(Doom, self).__init__(compound, enemy, damage, turns_until_effect)

    def __str__(self):
        return "Doom: a blast of {} damage after {} turns".format(self.damage, self.turns_until_effect)

    def call(self):
        if self.turns_until_effect > 0:
            slow_print('{} turns until DOOM effect on {}'.format(self.turns_until_effect, self.enemy.name))
            self.turns_until_effect -= 1   
        else:
            slow_print('{} does {} DOOM damage to {}'.format(self.compound.name, self.damage, self.enemy.name))
            self.enemy.damage(self.damage)
            self.enemy.remove_effect(self.uuid)
            del self
