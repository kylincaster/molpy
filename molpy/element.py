# author: Roy Kid
# contact: lijichen365@126.com
# date: 2021-10-28
# version: 0.0.1

from collections import OrderedDict
from molpy.unit import Unit

unit = Unit()
daltons = unit.daltons

class Element(object):
    """An Element represents a chemical element.

    The openmm.app.element module contains objects for all the standard chemical elements,
    such as element.hydrogen or element.carbon.  You can also call the static method Element.getBySymbol() to
    look up the Element with a particular chemical symbol.

    Element objects should be considered immutable
    """

    _elements_by_symbol = {}
    _elements_by_atomic_number = {}
    _elements_by_mass = None

    def __init__(self, number, name, symbol, mass):
        """Create a new element

        Parameters
        ----------
        number : int
            The atomic number of the element
        name : string
            The name of the element
        symbol : string
            The chemical symbol of the element
        mass : float
            The atomic mass of the element
        """
        ## The atomic number of the element
        self._atomic_number = number
        ## The name of the element
        self._name = name
        ## The chemical symbol of the element
        self._symbol = symbol
        ## The atomic mass of the element
        self._mass = mass
        # Index this element in a global table
        s = symbol.strip().upper()
        ## If we add a new element, we need to re-hash elements by mass
        Element._elements_by_mass = None

        ## The VDW radii of the element
        self._radii = 0.0;
        if symbol in COVALENT_RADII:
            self._radii = COVALENT_RADII[symbol]

        if s in Element._elements_by_symbol:
            raise ValueError('Duplicate element symbol %s' % s)
        Element._elements_by_symbol[s] = self
        if number in Element._elements_by_atomic_number:
            other_element = Element._elements_by_atomic_number[number]
            if mass < other_element.mass:
                # If two "elements" share the same atomic number, they're
                # probably hydrogen and deuterium, and we want to choose
                # the lighter one to put in the table by atomic_number,
                # since it's the "canonical" element.
                Element._elements_by_atomic_number[number] = self
        else:
            Element._elements_by_atomic_number[number] = self

    @staticmethod
    def getBySymbol(symbol):
        """Get the Element with a particular chemical symbol."""
        s = symbol.strip().upper()
        return Element._elements_by_symbol[s]

    @staticmethod
    def getByAtomicNumber(atomic_number):
        return Element._elements_by_atomic_number[atomic_number]

    @staticmethod
    def getByMass(mass):
        """
        Get the element whose mass is CLOSEST to the requested mass. This method
        should not be used for repartitioned masses

        Parameters
        ----------
        mass : float or Quantity
            Mass of the atom to find the element for. Units assumed to be
            daltons if not specified

        Returns
        -------
        Element
            The element whose atomic mass is closest to the input mass
        """
        # Assume masses are in daltons if they are not units
        
        mass = mass.to('daltons')
        if mass.magnitude < 0:
            raise ValueError('Invalid Higgs field')
        # If this is our first time calling getByMass (or we added an element
        # since the last call), re-generate the ordered by-mass dict cache
        if Element._elements_by_mass is None:
            Element._elements_by_mass = OrderedDict()
            for elem in sorted(Element._elements_by_symbol.values(),
                               key=lambda x: x.mass):
                Element._elements_by_mass[elem.mass.value_in_unit(daltons)] = elem

        diff = mass
        best_guess = None

        for elemmass, element in Element._elements_by_mass.items():
            massdiff = abs(elemmass - mass)
            if massdiff < diff:
                best_guess = element
                diff = massdiff
            if elemmass > mass:
                # Elements are only getting heavier, so bail out early
                return best_guess

        # This really should only happen if we wanted ununoctium or something
        # bigger... won't really happen but still make sure we return an Element
        return best_guess

    @property
    def atomic_number(self):
        return self._atomic_number

    @property
    def name(self):
        return self._name

    @property
    def symbol(self):
        return self._symbol

    @property
    def mass(self):
        return self._mass
    
    def __eq__(self, e):
        if isinstance(e, Element):
            return self._symbol == e.symbol
        elif isinstance(e, str):
            return self._symbol == e

# copy from lammps_interface/atomic.py
COVALENT_RADII = {
    # Covalent radii revisited -- DOI:10.1039/B801115J
    "*": 0,
    "H": 0.31,
    "He": 0.28,
    "Li": 1.28,
    "Be": 0.96,
    "B": 0.84,
    "C": 0.76,  # for sp3; sp2 = 0.73; sp = 0.69
    "C_1": 0.69,
    "C_2": 0.73,
    "C_R": 0.73,
    "C_3": 0.76,
    "N": 0.71,
    "O": 0.66,
    "F": 0.57,
    "Ne": 0.58,
    "Na": 1.66,
    "Mg": 1.41,
    "Al": 1.21,
    "Si": 1.11,
    "P": 1.07,
    "S": 1.05,
    "Cl": 1.02,
    "Ar": 1.06,
    "K": 2.03,
    "Ca": 1.76,
    "Sc": 1.7,
    "Ti": 1.6,
    "V": 1.53,
    "Cr": 1.39,
    "Mn": 1.61,  # low spin = 1.39
    "Fe": 1.52,  # low spin = 1.32
    "Co": 1.5,  # low spin = 1.26
    "Ni": 1.24,
    "Cu": 1.32,
    "Zn": 1.22,
    "Ga": 1.22,
    "Ge": 1.2,
    "As": 1.19,
    "Se": 1.2,
    "Br": 1.2,
    "Kr": 1.16,
    "Rb": 2.2,
    "Sr": 1.95,
    "Y": 1.9,
    "Zr": 1.5,  # 1.75  !! temporarily added to correct the UIO cluster bonding problem
    "Nb": 1.64,
    "Mo": 1.54,
    "Tc": 1.47,
    "Ru": 1.46,
    "Rh": 1.42,
    "Pd": 1.39,
    "Ag": 1.45,
    "Cd": 1.44,
    "In": 1.42,
    "Sn": 1.39,
    "Sb": 1.39,
    "Te": 1.38,
    "I": 1.39,
    "Xe": 1.4,
    "Cs": 2.44,
    "Ba": 2.15,
    "La": 2.07,
    "Ce": 2.04,
    "Pr": 2.03,
    "Nd": 2.01,
    "Pm": 1.99,
    "Sm": 1.98,
    "Eu": 1.98,
    "Gd": 1.96,
    "Tb": 1.94,
    "Dy": 1.92,
    "Ho": 1.92,
    "Er": 1.89,
    "Tm": 1.9,
    "Yb": 1.87,
    "Lu": 1.87,
    "Hf": 1.75,
    "Ta": 1.7,
    "W": 1.62,
    "Re": 1.51,
    "Os": 1.44,
    "Ir": 1.41,
    "Pt": 1.36,
    "Au": 1.36,
    "Hg": 1.32,
    "Tl": 1.45,
    "Pb": 1.46,
    "Bi": 1.48,
    "Po": 1.4,
    "At": 1.5,
    "Rn": 1.5,
    "Fr": 2.6,
    "Ra": 2.21,
    "Ac": 2.15,
    "Th": 2.06,
    "Pa": 2,
    "U": 1.96,
    "Np": 1.9,
    "Pu": 1.87,
    "Am": 1.8,
    "Cm": 1.69,
}

METALS = [3, 4, 11, 12, 13, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31,
          37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 55, 56, 57,
          58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74,
          75, 76, 77, 78, 79, 80, 81, 82, 83, 87, 88, 89, 90, 91, 92, 93, 94,
          95, 96, 97, 98, 99, 100, 101, 102, 103]

# keeping track of some different groups of atoms.
organic = set(["H", "C", "N", "O", "S"])
non_metals = set(["H", "He", "C", "N", "O", "F", "Ne",
                  "P", "S", "Cl", "Ar", "Se", "Br", "Kr",
                  "I", "Xe", "Rn"])
noble_gases = set(["He", "Ne", "Ar", "Kr", "Xe", "Rn"])
metalloids = set(["B", "Si", "Ge", "As", "Sb", "Te", "At"])
lanthanides = set(["La", "Ce", "Pr", "Nd", "Pm", "Sm", "Eu",
                   "Gd", "Tb", "Dy", "Ho", "Er", "Tm", "Yb", "Lu"])
actinides = set(["Ac", "Th", "Pa", "U", "Np", "Pu", "Am", "Cm", "Bk",
                 "Cf", "Es", "Fm", "Md", "No", "Lr"])
transition_metals = set(["Sc", "Ti", "V", "Cr", "Mn", "Fe", "Co", "Ni",
                         "Cu", "Zn", "Y", "Zr", "Nb", "Mo", "Tc", "Ru",
                         "Rh", "Pd", "Ag", "Cd", "Hf", "Ta", "W", "Re",
                         "Os", "Ir", "Pt", "Ir", "Pt", "Au", "Hg", "Rf",
                         "Db", "Sg", "Bh", "Hs", "Mt", "Ds", "Rg", "Cn"])
alkali = set(["Li", "Na", "K", "Rb", "Cs", "Fr"])
alkaline_earth = set(["Be", "Mg", "Ca", "Sr", "Ba", "Ra"])
main_group = set(["Al", "Ga", "Ge", "In", "Sn", "Sb", "Tl", "Pb", "Bi",
                  "Po", "At", "Cn", "Uut", "Fl", "Uup", "Lv", "Uus"])

metals = main_group | alkaline_earth | alkali | transition_metals | metalloids

wildcard =       Element(  0, 'wildcard', '*', 0*daltons)
hydrogen =       Element(  1, "hydrogen", "H", 1.007947*daltons)
deuterium =      Element(  1, "deuterium", "D", 2.01355321270*daltons)
helium =         Element(  2, "helium", "He", 4.003*daltons)
lithium =        Element(  3, "lithium", "Li", 6.9412*daltons)
beryllium =      Element(  4, "beryllium", "Be", 9.0121823*daltons)
boron =          Element(  5, "boron", "B", 10.8117*daltons)
carbon =         Element(  6, "carbon", "C", 12.01078*daltons)
nitrogen =       Element(  7, "nitrogen", "N", 14.00672*daltons)
oxygen =         Element(  8, "oxygen", "O", 15.99943*daltons)
fluorine =       Element(  9, "fluorine", "F", 18.99840325*daltons)
neon =           Element( 10, "neon", "Ne", 20.17976*daltons)
sodium =         Element( 11, "sodium", "Na", 22.989769282*daltons)
magnesium =      Element( 12, "magnesium", "Mg", 24.30506*daltons)
aluminum =       Element( 13, "aluminum", "Al", 26.98153868*daltons)
silicon =        Element( 14, "silicon", "Si", 28.08553*daltons)
phosphorus =     Element( 15, "phosphorus", "P", 30.9737622*daltons)
sulfur =         Element( 16, "sulfur", "S", 32.0655*daltons)
chlorine =       Element( 17, "chlorine", "Cl", 35.4532*daltons)
argon =          Element( 18, "argon", "Ar", 39.9481*daltons)
potassium =      Element( 19, "potassium", "K", 39.09831*daltons)
calcium =        Element( 20, "calcium", "Ca", 40.0784*daltons)
scandium =       Element( 21, "scandium", "Sc", 44.9559126*daltons)
titanium =       Element( 22, "titanium", "Ti", 47.8671*daltons)
vanadium =       Element( 23, "vanadium", "V", 50.94151*daltons)
chromium =       Element( 24, "chromium", "Cr", 51.99616*daltons)
manganese =      Element( 25, "manganese", "Mn", 54.9380455*daltons)
iron =           Element( 26, "iron", "Fe", 55.8452*daltons)
cobalt =         Element( 27, "cobalt", "Co", 58.9331955*daltons)
nickel =         Element( 28, "nickel", "Ni", 58.69342*daltons)
copper =         Element( 29, "copper", "Cu", 63.5463*daltons)
zinc =           Element( 30, "zinc", "Zn", 65.4094*daltons)
gallium =        Element( 31, "gallium", "Ga", 69.7231*daltons)
germanium =      Element( 32, "germanium", "Ge", 72.641*daltons)
arsenic =        Element( 33, "arsenic", "As", 74.921602*daltons)
selenium =       Element( 34, "selenium", "Se", 78.963*daltons)
bromine =        Element( 35, "bromine", "Br", 79.9041*daltons)
krypton =        Element( 36, "krypton", "Kr", 83.7982*daltons)
rubidium =       Element( 37, "rubidium", "Rb", 85.46783*daltons)
strontium =      Element( 38, "strontium", "Sr", 87.621*daltons)
yttrium =        Element( 39, "yttrium", "Y", 88.905852*daltons)
zirconium =      Element( 40, "zirconium", "Zr", 91.2242*daltons)
niobium =        Element( 41, "niobium", "Nb", 92.906382*daltons)
molybdenum =     Element( 42, "molybdenum", "Mo", 95.942*daltons)
technetium =     Element( 43, "technetium", "Tc", 98*daltons)
ruthenium =      Element( 44, "ruthenium", "Ru", 101.072*daltons)
rhodium =        Element( 45, "rhodium", "Rh", 102.905502*daltons)
palladium =      Element( 46, "palladium", "Pd", 106.421*daltons)
silver =         Element( 47, "silver", "Ag", 107.86822*daltons)
cadmium =        Element( 48, "cadmium", "Cd", 112.4118*daltons)
indium =         Element( 49, "indium", "In", 114.8183*daltons)
tin =            Element( 50, "tin", "Sn", 118.7107*daltons)
antimony =       Element( 51, "antimony", "Sb", 121.7601*daltons)
tellurium =      Element( 52, "tellurium", "Te", 127.603*daltons)
iodine =         Element( 53, "iodine", "I", 126.904473*daltons)
xenon =          Element( 54, "xenon", "Xe", 131.2936*daltons)
cesium =         Element( 55, "cesium", "Cs", 132.90545192*daltons)
barium =         Element( 56, "barium", "Ba", 137.3277*daltons)
lanthanum =      Element( 57, "lanthanum", "La", 138.905477*daltons)
cerium =         Element( 58, "cerium", "Ce", 140.1161*daltons)
praseodymium =   Element( 59, "praseodymium", "Pr", 140.907652*daltons)
neodymium =      Element( 60, "neodymium", "Nd", 144.2423*daltons)
promethium =     Element( 61, "promethium", "Pm", 145*daltons)
samarium =       Element( 62, "samarium", "Sm", 150.362*daltons)
europium =       Element( 63, "europium", "Eu", 151.9641*daltons)
gadolinium =     Element( 64, "gadolinium", "Gd", 157.253*daltons)
terbium =        Element( 65, "terbium", "Tb", 158.925352*daltons)
dysprosium =     Element( 66, "dysprosium", "Dy", 162.5001*daltons)
holmium =        Element( 67, "holmium", "Ho", 164.930322*daltons)
erbium =         Element( 68, "erbium", "Er", 167.2593*daltons)
thulium =        Element( 69, "thulium", "Tm", 168.934212*daltons)
ytterbium =      Element( 70, "ytterbium", "Yb", 173.043*daltons)
lutetium =       Element( 71, "lutetium", "Lu", 174.9671*daltons)
hafnium =        Element( 72, "hafnium", "Hf", 178.492*daltons)
tantalum =       Element( 73, "tantalum", "Ta", 180.947882*daltons)
tungsten =       Element( 74, "tungsten", "W", 183.841*daltons)
rhenium =        Element( 75, "rhenium", "Re", 186.2071*daltons)
osmium =         Element( 76, "osmium", "Os", 190.233*daltons)
iridium =        Element( 77, "iridium", "Ir", 192.2173*daltons)
platinum =       Element( 78, "platinum", "Pt", 195.0849*daltons)
gold =           Element( 79, "gold", "Au", 196.9665694*daltons)
mercury =        Element( 80, "mercury", "Hg", 200.592*daltons)
thallium =       Element( 81, "thallium", "Tl", 204.38332*daltons)
lead =           Element( 82, "lead", "Pb", 207.21*daltons)
bismuth =        Element( 83, "bismuth", "Bi", 208.980401*daltons)
polonium =       Element( 84, "polonium", "Po", 209*daltons)
astatine =       Element( 85, "astatine", "At", 210*daltons)
radon =          Element( 86, "radon", "Rn", 222.018*daltons)
francium =       Element( 87, "francium", "Fr", 223*daltons)
radium =         Element( 88, "radium", "Ra", 226*daltons)
actinium =       Element( 89, "actinium", "Ac", 227*daltons)
thorium =        Element( 90, "thorium", "Th", 232.038062*daltons)
protactinium =   Element( 91, "protactinium", "Pa", 231.035882*daltons)
uranium =        Element( 92, "uranium", "U", 238.028913*daltons)
neptunium =      Element( 93, "neptunium", "Np", 237*daltons)
plutonium =      Element( 94, "plutonium", "Pu", 244*daltons)
americium =      Element( 95, "americium", "Am", 243*daltons)
curium =         Element( 96, "curium", "Cm", 247*daltons)
berkelium =      Element( 97, "berkelium", "Bk", 247*daltons)
californium =    Element( 98, "californium", "Cf", 251*daltons)
einsteinium =    Element( 99, "einsteinium", "Es", 252*daltons)
fermium =        Element(100, "fermium", "Fm", 257*daltons)
mendelevium =    Element(101, "mendelevium", "Md", 258*daltons)
nobelium =       Element(102, "nobelium", "No", 259*daltons)
lawrencium =     Element(103, "lawrencium",     "Lr", 262*daltons)
rutherfordium =  Element(104, "rutherfordium",  "Rf", 261*daltons)
dubnium =        Element(105, "dubnium",        "Db", 262*daltons)
seaborgium =     Element(106, "seaborgium",     "Sg", 266*daltons)
bohrium =        Element(107, "bohrium",        "Bh", 264*daltons)
hassium =        Element(108, "hassium",        "Hs", 269*daltons)
meitnerium =     Element(109, "meitnerium",     "Mt", 268*daltons)
darmstadtium =   Element(110, "darmstadtium",   "Ds", 281*daltons)
roentgenium =    Element(111, "roentgenium",    "Rg", 272*daltons)
ununbium =       Element(112, "ununbium",       "Uub", 285*daltons)
ununtrium =      Element(113, "ununtrium",      "Uut", 284*daltons)
ununquadium =    Element(114, "ununquadium",    "Uuq", 289*daltons)
ununpentium =    Element(115, "ununpentium",    "Uup", 288*daltons)
ununhexium =     Element(116, "ununhexium",     "Uuh", 292*daltons)

# default unsettled element
unknownium =     Element(1000, "unknown",       "UNK", 0*daltons)

# Aliases to recognize common alternative spellings. Both the '==' and 'is'
# relational operators will work with any chosen name
sulphur = sulfur
aluminium = aluminum