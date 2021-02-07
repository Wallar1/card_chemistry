from enemy import Enemy
from utilities import slow_print


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