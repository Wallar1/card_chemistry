class Lifeline(object):
    """
    you get to choose whether to get a hint, functional group, or 5 cards, and they each have a cooldown
    """ 
    def __init__(self, max_cooldown, current_cooldown):
        self.max_cooldown = max_cooldown
        self.current_cooldown = current_cooldown

    def apply(self):
        raise NotImplementedError


class FunctionalGroupEffect(Lifeline):
    def apply(self):
        pass


class Hint(Lifeline):
    def apply(self, battle, player):
        hint = player.compound_finder.find_random_compound(self, battle.elements, player.compounds_unlocked)
        battle.show_modal()


class Add5Cards(Lifeline):
    pass

class AddHealth(Lifeline):
    pass