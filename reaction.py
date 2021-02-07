class ReactionRequirement(object):
    def __init__(self, temperature, catalyst):
        self.temperature = temperature
        self.catalyst = catalyst


class Reaction(object):
    def __init__(self, reactants, products, reaction_requirements):
        """
        Question: data type for reactants/products?
        probably a dict, but what are the keys? string of the chemical formula, and the value is the coefficient?
        or just do a set of the coefficient + formula
        """
        self.reactants = reactants
        self.products = products
        self.reaction_requirements = reaction_requirements


