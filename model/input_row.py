from enum import Enum
from calculations.strategy import EngagementStrategy


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

    def assign_category(self):
        self.category = EngagementStrategy(self).assign_category()

    def has_any_engagements(self):
        return len(self.engagements) != 0


class Category(Enum):

    NOT_ASSIGNED = 0
    ACCEPTED = 1
    TO_CHECK = 2
    NOT_ACCEPTED = 3
