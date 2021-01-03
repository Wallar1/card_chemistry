import collections
import math
import os
import random

from functools import reduce

from compound import CompoundFactory, Compound
from enemy import Enemy
from utilities import measure_performance, slow_print, get_coefficient


class Element(object):
    def __init__(self, symbol):
        self.symbol = symbol


class Instrument(object):
    def __init__(self, name, level_effect):
        self.name = name
        self.level_effect = level_effect

    def affect_level(self):
        pass


ALL_COMPOUNDS = ['H2', 'CH4', 'NH3', 'CO', 'CN']

# this is a reverse probability, with everything related to hydrogen. So if hydrogen is 4x more likely to appear
# than another element X, the probability weight of X will be 4. You can use this by finding the least common multiple,
# and then dividing the LCM by the weight. For example, the LCM of 2 and 3 is 6. So for {a: 2, b: 3} you do 6/2 = 3a and
# 6/3 = 2b
ELEMENT_PROBABILITIES = {
    'H': 1,
    'C': 3,
    'N': 6,
    'O': 6,
    'Au': 20,
    'Ag': 12,
    'Pb': 8,
    'Al': 9,
    'Si': 11,
    'Ca': 9,
    'Na': 10,
    'Cl': 12,
    'Mg': 20
}


ElementFrequency = collections.namedtuple('ElementFrequency', ['min_range', 'max_range', 'element_name'])


class Player(object):
    """
    improvements could be new instrument (bunsen burner, condensor or something), new compound unlocks
    """
    def __init__(self, health=50):
        self.instruments_unlocked = [Instrument('bunsen burner', 'melt state')]
        # TODO: in order to uncomment out these lines, you need to create compound classes for each compound
        # self.compounds_unlocked = ['H2', 'CH4', 'NH3', 'CO', 'CN', 'H2O', 'O2']
        self.compounds_unlocked = ['Pb', 'CN']
        # self.elements_unlocked = ['H', 'C', 'O', 'N', 'Au', 'Ag', 'Pb', 'Al', 'Si', 'Ca', 'Na', 'Cl', 'Mg']
        self.elements_unlocked = ['Pb', 'C', 'N']
        self.initial_health = health
        self.current_health = health
        self.element_counts = {}
        self.elements_in_their_occuring_frequencies = []

    def start_battle(self, heat, lifelines):
        # health, attack, trait, speed, weakness, state_of_matter
        slow_print('Starting battle!')
        if not heat.get('starting_level', None):
            heat['starting_level'] = 10

        # TODO: maybe only battles need to create enemies
        enemy1 = Enemy.create_enemy_of_level(heat['starting_level'])
        enemy2 = Enemy.create_enemy_of_level(heat['starting_level'])
        battle = Battle(self, [enemy1, enemy2], heat, lifelines)

        battle.start()

    def possible_compound_choices(self):
        # returned dict of {'formula': number_that_can_be_made (max coefficient)}
        possible_compounds = {}

        def can_make_compound(formula):
            compound_as_dict = Compound.classmeth_parse_formula_to_dict(formula)
            max_coefficient = math.inf
            for element, count in compound_as_dict.items():
                dont_have_element = not self.element_counts.get(element, None)
                if dont_have_element:
                    max_coefficient = 0
                    break
                max_compounds_possible = math.floor(self.element_counts.get(element) / count)
                max_coefficient = min(max_compounds_possible, max_coefficient)
                if max_coefficient == 0:
                    break
            return formula, max_coefficient

        for unlocked_formula in self.compounds_unlocked:
            formula, max_coefficient = can_make_compound(unlocked_formula)
            if max_coefficient:
                possible_compounds[formula] = max_coefficient
        return possible_compounds

    @property
    def elements_array_of_occuring_frequencies(self):
        """
        brute force way of getting a random element. I build an array that has all of the elements by their expected
        frequency, and then choose a random one of those elements. For example, if the unlocked elements were C, H, and
        O, the array I would build is [O,C,C,H,H,H,H,H,H] because the weights of C,H, and O are 3, 1, and 6 respectively
        """
        if self.elements_in_their_occuring_frequencies:
            return self.elements_in_their_occuring_frequencies
        else:
            el_probabilities = []
            for el in self.elements_unlocked:
                el_probabilities.append(ELEMENT_PROBABILITIES.get(el))
            lcm = least_common_multiple(el_probabilities)
            # I store an array of tuples of the element and the max range of it. so we are basically partitioning space
            # for each element [(0, 1, Ag), (1, 5, C), (5, 17, H)] because H is 12x more likely than Ag and 5x more vs C
            current_min = 0
            ranges = []
            for el in self.elements_unlocked:
                count = lcm / ELEMENT_PROBABILITIES.get(el)
                ranges.append(ElementFrequency(current_min, current_min + count, el))
                current_min += count
            # cache it
            self.elements_in_their_occuring_frequencies = ranges
            return self.elements_in_their_occuring_frequencies

    @measure_performance
    def get_random_elements_with_probabilities(self, max_count=1):
        ret_arr = []
        count = random.randint(1, max_count)
        for i in range(count):
            element_idx = random.randrange(self.elements_array_of_occuring_frequencies[-1].max_range)
            for element_frequency in self.elements_array_of_occuring_frequencies:
                if element_frequency.max_range > element_idx:
                    el = element_frequency.element_name
                    break
            ret_arr.append(el)
        return ret_arr


class Battle(object):
    """
    Heat are things that make the match more difficult, lifelines make the battle easier
    """
    def __init__(self, player, enemies, heat={}, lifelines={}):
        self.player = player
        self.enemies = enemies
        # two way connection
        for enemy in enemies:
            enemy.battle = self
        self.heat = heat
        self.lifelines = lifelines

    def start(self):
        level = self.heat.get('starting_level', 1)
        turns_to_increase_level = self.heat.get('turns_to_increase_level', 5)
        turn = 0
        self.player.element_counts = {}
        while level < 20:
            turn += 1
            slow_print("\n\nTurn {}".format(turn))
            if turn % turns_to_increase_level == 0:
                level += 1
                slow_print('New enemy spotted!')
                self.add_enemy(Enemy.create_enemy_of_level(level))
            # enemy attack and effect damage
            # TODO: give the enemies a name instead of an index
            for enemy in self.enemies:
                if enemy.distance > 0:
                    enemy.distance = max(0, enemy.distance - enemy.speed)
                slow_print('Enemy {} is {} distance away now with {} health and a speed of {}.'.format(enemy.name, enemy.distance, enemy.health, enemy.speed))
                if enemy.distance == 0:
                    slow_print('Enemy {} attacks for {} damage.'.format(enemy.name, enemy.attack))
                    self.player.current_health -= enemy.attack
                    if self.player.current_health <= 0:
                        slow_print('YOU DIED!! GAME OVER')
                        return False
                    else:
                        slow_print('You have {} health left.'.format(self.player.current_health))
                for effect in enemy.effects:
                    effect.call()

            if len(self.enemies) == 0:
                level += 1
                slow_print("New enemy spotted!")
                self.add_enemy(Enemy.create_enemy_of_level(level))

            slow_print('Your Health: {}'.format(self.player.current_health))
            max_possible_new_elements = self.lifelines.get('max_possible_new_lifelines', level)
            elements_to_add = self.player.get_random_elements_with_probabilities(max_possible_new_elements)
            slow_print('You picked up {}!'.format(', '.join(elements_to_add)))
            for element in elements_to_add:
                if self.player.element_counts.get(element, None):
                    self.player.element_counts[element] += 1
                else:
                    self.player.element_counts[element] = 1
            slow_print('Elements:')
            slow_print(self.player.element_counts)
            possible_compound_choices = self.player.possible_compound_choices()
            printable_choices = ['Up to {} {}'.format(coeff, str(CompoundFactory.create(formula, None))) for formula, coeff in possible_compound_choices.items()]
            slow_print('You can make the following compounds:')
            slow_print('\n'.join(printable_choices))
            self.player_attacks(level, possible_compound_choices, printable_choices)     
        slow_print('You made it to level 20! YOU WIN!!')

    def player_attacks(self, level, possible_compound_choices, printable_choices):

        attacks_left = 1
        resp = ''
        formula = ''
        coefficient = 0
        while attacks_left > 0:
            while not resp:
                if not len(possible_compound_choices.items()):
                    slow_print('You dont have enough elements to make any compounds')
                    break
                resp = input('What compound would you like to form? (Enter "skip" to skip your turn):  ')
                coefficient, formula = get_coefficient(resp)
                max_coefficient = possible_compound_choices.get(formula, 0)
                if max_coefficient >= coefficient or formula in ['skip', 's']:
                    break
                else:
                    slow_print('You have only unlocked the following compounds: ')
                    slow_print(self.player.compounds_unlocked)
                    slow_print('And you can only build these compounds with the elements you have:')
                    for printable_choice in printable_choices:
                        slow_print(printable_choice)
                    resp = ''
            attacks_left -= 1
            if formula and formula != "skip" and formula != "s":
                chosen_compound = CompoundFactory.create(formula, None)
                compound_as_dict = chosen_compound.parse_formula_to_dict()
                for _ in range(coefficient):
                    for elem, count in compound_as_dict.items():
                        if self.player.element_counts[elem] - count == 0:
                            del self.player.element_counts[elem]
                        else:
                            self.player.element_counts[elem] -= count
                # pick one of the closest enemies
                self.enemies.sort(key=lambda e: e.distance)
                # TODO: pass all enemies so we can add effects like bomb to all of them?
                chosen_compound.damage_enemy(self.enemies[0], coefficient)

                if len(self.enemies) == 0:
                    level += 1
                    slow_print("New enemy spotted!")
                    self.add_enemy(Enemy.create_enemy_of_level(level))   

    def kill(self, enemy):
        self.enemies = [e for e in self.enemies if e.uuid != enemy.uuid]

    def add_enemy(self, enemy):
        enemy.battle = self
        self.enemies.append(enemy)


class HeatAdder(object):
    """
    heat determines things like the enemy strength/speed/health, cooldowns, number of enemies etc
    """
    pass


def play_game():
    os.system('clear')
    player = Player()
    # TODO: make this some kind of loop
    won = player.start_battle(heat={}, lifelines={})


def least_common_multiple(num_arr):
    #lazy method is just return the multiple of all of the numbers, which is not an LCM, but it works the same
    return reduce(lambda serialized, num: serialized * num, num_arr, 1)

    # lcm = 1
    # # make sure they are all not 1, because if so, the lcm is just 1
    # if max(num_arr) == 1:
    #     return 1

    # def all_nums_are_factors(num_arr):
    #     for num in num_arr:
    #         if lcm % num != 0:
    #             return False
    #     return True

    # # some random upper bound so we dont run to infinity if this code is wrong
    # while lcm < 1000:
    #     lcm += 1
    #     if all_nums_are_factors(num_arr):
    #         return lcm
    # raise Exception("Least common multiple was not found")


play_game()
