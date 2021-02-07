class Instrument(object):
    """
    This is the 'weapon' for the player. But it is supposed to be different tools, like erlemeiher flask or pipette or 
    bunsen burner or condenser etc
    """
    def __init__(self, name, level_effect):
        self.name = name
        self.level_effect = level_effect

    def affect_level(self):
        pass