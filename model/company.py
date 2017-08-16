class Company:
    """
    Class used to represent company entity

    Attributes:
        nip(str):
        national_account(str):
        entity_name(str):
        description(str):
    """
    def __init__(self, nip, national_account, entity_name, description):
        self.nip = nip
        self.national_account = national_account
        self.entity_name = entity_name
        self.description = description
