from .base_row import BaseRow


class Relationship(BaseRow):
    """
    Class used to represent relationship row from database
    
    """

    COLUMN_NAMES = ["NIP", "ENTITY_NAME", "CONTACT_NAME", "KPMG_EMPLOYEE", "RELATIONSHIP"]

    def __init__(self, nip, entity_name, contact_name, kpmg_employee, relationship):
        super().__init__()
        self.nip = nip
        self.entity_name = entity_name
        self.contact_name = contact_name
        self.kpmg_employee = kpmg_employee
        self.relationship = relationship

    def get_column_values_as_list(self):
        data = list()
        data.append(self.nip)
        data.append(self.entity_name)
        data.append(self.contact_name)
        data.append(self.kpmg_employee)
        data.append(self.relationship)

        return data

    def print_attributes_separated_by_semicolon(self):
        return "{0.nip};{0.entity_name};{0.contact_name};{0.kpmg_employee};{0.relationship};".format(self)
