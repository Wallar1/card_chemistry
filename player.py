import math
import random

from battle import Battle
from compound import Compound
from element import ElementFrequency, ELEMENT_PROBABILITIES
from enemy import Enemy
from instrument import Instrument
from utilities import measure_performance, slow_print, least_common_multiple, JsonSerializable


class Player(JsonSerializable):
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
