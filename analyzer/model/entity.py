from .base_row import BaseRow


class Entity(BaseRow):
    """
    Class used to represent company entity

    Attributes:
        nip(str):
        national_account(str):
        entity_name(str):
        description(str):
    """

    entity_not_in_capital_group = ["", "Other", "none"]
    descriptions_for_category_3 = ["audit restricted client - PL Secondary approval",
                                   "audit restricted client - PL SLP assigned",
                                   "audit restricted client - SLP assigned",
                                   "SEC/Audit",
                                   "SEC/Audit client - PL Secondary approval"]
    COLUMN_NAMES = ["NIP", "NATIONAL_ACCOUNT", "ENTITY_NAME", "DESCRIPTION"]

    def __init__(self, nip, national_account, entity_name, description):
        self.nip = nip
        self.national_account = national_account
        self.entity_name = entity_name
        self.description = description

    def __str__(self):
        return "[{0.nip}][{0.national_account}][{0.entity_name}][{0.description}]".format(self)

    def is_in_capital_group(self):
        return self.national_account not in Entity.entity_not_in_capital_group

    def is_restricted(self):
        return self.description in Entity.descriptions_for_category_3

    def print_attributes_separated_by_semicolon(self):
        return "{0.nip};{0.national_account};{0.entity_name};{0.description}".format(self)

    def get_column_values_as_list(self):
        data = list()
        data.append(self.nip)
        data.append(self.national_account)
        data.append(self.entity_name)
        data.append(self.description)

        return data
