class CalculationsObject:

    def __init__(self, company_name, nip, company_name_in_crm):
        self.company_name = company_name
        self.nip = nip
        self.category = -1
        self.company_name_in_crm = company_name_in_crm
        self.engagements = []

    def __str__(self):
        return "[{0.company_name}][{0.nip}][{0.category}][{0.company_name_in_crm}]".format(self)
