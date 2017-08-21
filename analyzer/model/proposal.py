from .base_row import BaseRow


class Proposal(BaseRow):
    """
    Class used to represent proposal row from file with Proposals
    Attributes:
        entity(Entity): company nip
        proposal_id(str): company nip
        proposal_name(str): company nip
        proposal_partner(str): company nip
        create_date(str): company nip
        status(str): company nip

    """

    proposal_restricted_status = ["Active", "Sold", "Sent", "New"]

    def __init__(self, entity, proposal_id, proposal_name, proposal_partner, create_date, status):
        self.entity = entity
        self.proposal_id = proposal_id
        self.proposal_name = proposal_name
        self.proposal_partner = proposal_partner
        self.create_date = create_date
        self.status = status

    def __str__(self):
        return "[{0.entity}][{0.proposal_id}][{0.proposal_name}][{0.proposal_partner}][{0.create_date}][{0.status}]"\
            .format(self)

    def is_active(self):
        return self.status in Proposal.proposal_restricted_status

    def print_attributes_separated_by_semicolon(self):
        return "{0.entity};{0.proposal_id};{0.proposal_name};{0.proposal_partner};{0.create_date};" \
               "{0.status};".format(self)
