import math
import random
import uuid

from utilities import slow_print


class Enemy(object):
    def __init__(self, health=5, attack=1, speed=1, distance=3, traits={}, weaknesses={}, battle={}):
        """
        I imagine traits and weaknesses will be like {'name_of_trait': function_to_call}
        """
        self.health = health
        self.attack = attack
        self.speed = speed
        self.distance = distance
        self.traits = traits
        self.weaknesses = weaknesses
        self.effects = []
        self.name = random.randint(1, 100)
        self.battle = battle
        self.uuid = uuid.uuid4()

    @classmethod
    def create_enemy_of_level(cls, level):
        min_health = math.ceil(level/2)
        max_health = max(min_health, level + 1)
        health = random.randint(min_health, max_health)

        min_attack = math.ceil(level/10)
        max_attack = max(min_attack, math.ceil(level/3))
        attack = random.randint(min_attack, max_attack)

        min_distance = math.ceil(level/2)
        max_distance = max(min_distance, level + 1)
        distance = random.randint(min_distance, max_distance)

        speed = math.ceil(math.sqrt(level))
        traits = {}
        weaknesses = {}
        return Enemy(health, attack, speed, distance, traits, weaknesses)

    def damage(self, damage):
        self.health = max(0, self.health - damage)
        if self.health == 0:
            self.die()

    def die(self):
        print('Enemy {} has died!'.format(self.name))
        self.battle.kill(self)
        del self

    def add_effect(self, effect):
        self.effects.append(effect)
        effect.enemy = self

    def remove_effect(self, removed_id):
        effects = []
        for effect in self.effects:
            if effect.uuid == removed_id:
                del effect
            else:
                effects.append(effect)
        self.effects = effects
