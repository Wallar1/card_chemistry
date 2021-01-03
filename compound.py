from effects import Doom, Poison, Effect
from utilities import slow_print


compound_to_damage_dict = {
    'H2': 2,
    'CH4': 4,
    'NH3': 5,
    'CO': 1,
    'CN': 4,
    'H2O': 2,
    'O2': 1,
    'Au': 5,
    'Ag': 4,
    'Pb': 8,
    'Al': 9,
    'Si': 2,
    'Ca': 4,
    'Na': 9,
    'Cl': 9,
    'Mg': 6
}

formula_to_name_dict = {
    'H2': 'Hydrogen gas',
    'CH4': 'Methane',
    'NH3': 'Ammonia',
    'CO': 'Carbon Monoxide',
    'CN': 'Cyanide',
    'H2O': 'Water',
    'O2': 'Oxygen gas',
    'Au': 'Gold',
    'Ag': 'Silver',
    'Pb': 'Lead',
    'Al': 'Aluminum',
    'Si': 'Silicon',
    'Ca': 'Calcium',
    'Na': 'Sodium',
    '2Na': 'Sodium x 2',
    '3Na': 'Sodium x 3',
    'Cl': 'Chlorine',
    '2Cl': 'Chlorine x 2',
    '3Cl': 'Chlorine x 3',
    'Mg': 'Mercury',
    'NaCl': 'Sodium Chloride (table salt)'
}

"""
Mercury: makes enemies crazy and attack each other
Gold: grants 2 other attacks
Silver: grants 1 other attack
Lead: some doom damage
Cyanide: poison
Chlorine: poison
Sodium: explodes on neighbors
Calcium: makes player stronger
Copper: electric shock that jumps from enemy to enemy 
"""


class Compound(object):
    def __init__(self, formula, effects=[]):
        self.formula = str
        self.name = str
        self.effects = list(Effect)
        self.damage = int
        raise NotImplementedError

    def __str__(self):
        string = "{} ({}): {} damage. \n\tEffects: ".format(self.name, self.formula, self.damage)
        for effect in self.effects:
            string += "\n\t\t"
            string += str(effect)
        return string

    @classmethod
    def classmeth_parse_formula_to_dict(cls, formula):
        """
        returns a dictionary of the element counts
        ex: Br2ClNH3 -> {'Br': 2, 'Cl': 1, 'N': 1, 'H': 3}
        """
        element_counts = {}
        element = ''
        count = ''
        for c in formula:
            try:
                num = int(c)
                if count:
                    count += num
                else:
                    count = num
            except ValueError:
                # Every element symbol has only 1 capital, so a capital signals a new element
                if c.isupper():
                    if element:
                        try:
                            addition = int(count) if int(count) else 1
                        except ValueError:
                            addition = 1
                        if element_counts.get(element, None):
                            element_counts[element] += addition
                        else:
                            element_counts[element] = addition
                        element = ''
                        count = ''
                    element = c
                else:
                    element += c
        if element:
            try:
                addition = int(count) if int(count) else 1
            except ValueError:
                addition = 1
            if element_counts.get(element, None):
                element_counts[element] += int(count)
            else:
                element_counts[element] = addition
        return element_counts

    def parse_formula_to_dict(self):
        return Compound.classmeth_parse_formula_to_dict(self.formula)

    # TODO: Coefficient doesnt multiply effects. Seems fair right?
    def damage_enemy(self, enemy, coefficient):
        if not enemy:
            raise Exception('Could not damage enemy that doesnt exist.')
        dmg = self.damage * coefficient
        slow_print("Attacked enemy {} with {}({}) for {} damage".format(enemy.name, self.name, self.formula, dmg))
        enemy.damage(dmg)
        # TODO: this stacks the effects, but do we want that?
        if len(self.effects):
            for effect in self.effects:
                enemy.add_effect(effect)


class Cyanide(Compound):
    def __init__(self, enemy):
        self.formula = 'CN'
        self.name = 'Cyanide'
        self.effects = [Poison(compound=self, enemy=enemy, damage=2)]
        self.damage = 4


class Lead(Compound):
    def __init__(self, enemy):
        self.formula = 'Pb'
        self.name = 'Lead'
        self.effects = [Doom(compound=self, enemy=enemy, damage=20)]
        self.damage = 5


class Chlorine(Compound):
    def __init__(self, enemy):
        self.formula = 'Cl'
        self.name = 'Chlorine'
        self.effects = []
        self.damage = 9


class CompoundFactory(object):
    formulas_to_class = {
        'H2': 'Hydrogen gas',
        'CH4': 'Methane',
        'NH3': 'Ammonia',
        'CO': 'Carbon Monoxide',
        'CN': Cyanide,
        'H2O': 'Water',
        'O2': 'Oxygen gas',
        'Au': 'Gold',
        'Ag': 'Silver',
        'Pb': Lead,
        'Al': 'Aluminum',
        'Si': 'Silicon',
        'Ca': 'Calcium',
        'Na': 'Sodium',
        '2Na': 'Sodium x 2',
        '3Na': 'Sodium x 3',
        'Cl': 'Chlorine',
        '2Cl': 'Chlorine x 2',
        '3Cl': 'Chlorine x 3',
        'Mg': 'Mercury',
        'NaCl': 'Sodium Chloride (table salt)'
        }

    @classmethod
    def create(cls, formula, enemy):
        return cls.formulas_to_class.get(formula)(enemy)
