from enum import Enum
from . engagement import Engagement
from . entity import Entity

class InputRow:
    """
        Class used to represent input data, which category will be assigned

    Attributes:
        name(str): entity name
        nip(str): entity nip number
        company_name_in_crm(str): entity name in database
        category(Category): final category as a result of calculations
        engagements(list): list of entity engagements
        proposals(list): list of entity proposals
        bda(list): list of entity bda
    """

    def __init__(self, name, nip, company_name_in_crm):
        self.name = name
        self.nip = nip
        self.category = Category.NOT_ASSIGNED
        self.company_name_in_crm = company_name_in_crm
        self.engagements = []
        self.proposals = []
        self.bda = []

    def __str__(self):
        return "[{0.name}][{0.nip}][{0.category}][{0.company_name_in_crm}]".format(self)

    def has_any_engagements(self):
        return len(self.engagements) != 0

    def has_any_proposals(self):
        return len(self.proposals) != 0

    def has_any_bdas(self):
        return len(self.bda) !=0

    def is_entity_name_same_as_crm_name(self, entity_name):
        return entity_name.upper() == self.company_name_in_crm.upper()

    def write_to_file(self, file_name):
        for attr, val in self.__dict__.items():
            print("Attr: {} val {}".format(attr, val))

class Category(Enum):

    NOT_ASSIGNED = 0
    ACCEPTED = 1
    TO_CHECK = 2
    NOT_ACCEPTED = 3
