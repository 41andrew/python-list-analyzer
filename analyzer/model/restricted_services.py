from .base_row import BaseRow


class RestrictedServices(BaseRow):
    """
    Class used to represent restricted services on entity

    """

    COLUMN_NAMES = ["NIP", "ENTITY_NAME", "RESTRICTED_SERVICES_COUNT"]

    def __init__(self, nip, entity_name, count):
        super().__init__()
        self.nip = nip
        self.entity_name = entity_name
        self.count = count

    def get_column_values_as_list(self):
        data = list()
        data.append(self.nip)
        data.append(self.entity_name)
        data.append(self.count)

        return data

    def print_attributes_separated_by_semicolon(self):
        return "{0.nip};{0.entity_name};{0.count};".format(self)
