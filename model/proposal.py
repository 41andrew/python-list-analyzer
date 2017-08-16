class Proposal:
    """

    Attributes:
        company(str): company nip
        proposal_id(str): company nip
        proposal_name(str): company nip
        proposal_partner(str): company nip
        create_date(str): company nip
        status(str): company nip

    """

    def __init__(self, company, proposal_id, proposal_name, proposal_partner, create_date, status):
        self.company = company
        self.proposal_id = proposal_id
        self.proposal_name = proposal_name
        self.proposal_partner = proposal_partner
        self.create_date = create_date
        self.status = status
