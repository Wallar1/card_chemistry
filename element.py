import collections


class Element(object):
    def __init__(self, symbol):
        self.symbol = symbol


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