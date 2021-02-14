from heat import Heat
from utilities import JsonSerializable


class Scientist(JsonSerializable):
    """
    So each battle will be against a scientist, and they are summoning smaller enemies. 
    The smaller enemies are summoned every 5 turns, and you have to kill them before attacking the scientist.
    The scientist has special effects based on their dicoveries.

    I imagine the game looks like a timeline, and you can fight any of the scientists at any time (so they are always
    scrolling through and seeing the order). But it also allows for a metagame where they can fight different people
    depending on what they have

    Story summary is just a simple blurb about the scientists achievements
    Heat are just the added difficulties/effects
    """
    def __init__(self, name: str, year: int, story: str, heat: Heat = None):
        self.name = name
        self.year = year
        self.story = story
        self.heat = heat


class Democritus(Scientist):
    def __init__(self):
        story = 'Declared that matter is composed of indivisible and indestructible particles called "atomos"'
        heat = Heat()
        super(Democritus, self).__init__('Democritus', -380, story, heat)


class Geber(Scientist):
    def __init__(self):
        name = 'Jābir ibn Hayyān (Geber)'
        story = 'Father of chemistry: introduced a systematic classification of chemical substances, and provided instructions for deriving an inorganic compound (sal ammoniac or ammonium chloride) from organic substances (such as plants, blood, and hair) by chemical means. Declared there were 6 idealized elements: air, earth, fire, water, sulphur (combustability), and mercury (metallic properties).'
        year = 800
        heat = Heat()
        super(Geber, self).__init__(name, year, story, heat)


class SirFrancisBacon(Scientist):
    def __init__(self):
        name = 'Sir Francis Bacon'
        story = 'Developed the scientific method.'
        year = 1605
        heat = Heat()
        super(SirFrancisBacon, self).__init__(name, year, story, heat)


class RobertBoyle(Scientist):
    def __init__(self):
        name = 'Robert Boyle'
        story = "Founder of modern chemistry. Boyle's law states that the volume and pressure of a gas are inversely proportional when the temperature is constant. So when the pressure goes up, the volume goes down, and vice versa."
        year = 1662
        heat = Heat()
        super(RobertBoyle, self).__init__(name, year, story, heat)


class AlessandroVolta(Scientist):
    def __init__(self):
        name = 'Alessandro Volta'
        story = 'Constructed the first electrical battery and founded electrochemistry with the invention of galvonic cells.'
        year = 1800
        heat = Heat()
        super(AlessandroVolta, self).__init__(name, year, story, heat)


class Lavoisier(Scientist):
    def __init__(self):
        name = 'Antoine-Laurent de Lavoisier'
        story = "Brought about a rennaissance in chemistry by discovering the Law of Conservation of Mass, inventing our system of naming with Berthollet, working with Laplace on calorimetry, and understanding combustion with his wife."
        year = 1780
        heat = Heat()
        super(Lavoisier, self).__init__(name, year, story, heat)


class DuPont(Scientist):
    def __init__(self):
        name = 'Éleuthère Irénée du Pont'
        year = 1802
        story = 'Invented gun powder and founded the DuPont chemical company. Studied under Lavoisier.'
        super(DuPont, self).__init__(name, year, story)
        

class JohnDalton(Scientist):
    def __init__(self):
        name = 'John Dalton'
        year = 1803
        story = "Discovered the relationship between a mixture of gases and their partial pressures (Dalton's Law). Provided a basis for modern atomic theory and stoichiometry."
        super(JohnDalton, self).__init__(name, year, story)


class Berzelius(Scientist):
    def __init__(self):
        name = 'Jöns Jacob Berzelius'
        year = 1828
        story = "Invented our chemical symbals for elements and subscripts/proportions (eg H2O), as well as identified several new elements (silicon, selenium, thorium, cerium, lithium, and vanadium)."
        super(Berzelius, self).__init__(name, year, story)


class HumphryDavy(Scientist):
    def __init__(self):
        name = 'Humphry Davy'
        year = 1807
        story = "Discovered several earth metals (sodium, potassium, calcium, magnesium, strontium, and barium), as well as contributions to the discoveries of the elemental nature of chlorine and iodine."
        super(HumphryDavy, self).__init__(name, year, story)


ALL_SCIENTISTS = [
    Democritus(),
    Geber(),
    SirFrancisBacon(),
    RobertBoyle(),
    AlessandroVolta(),
    Lavoisier(),
    DuPont(),
    JohnDalton(),
    Berzelius(),
    HumphryDavy()
]
