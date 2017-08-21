from .base_row import BaseRow
from .entity import Entity


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

    COLUMN_NAMES = ["NIP", "NATIONAL_ACCOUNT", "ENTITY_NAME", "DESCRIPTION", "PROPOSAL_ID", "PROPOSAL_NAME",
                    "PROPOSAL_PARTNER", "CREATE_DATE", "STATUS"]
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

    def get_column_values_as_list(self):
        data = list()
        data.extend(self.entity.get_column_values_as_list())
        data.append(self.proposal_id)
        data.append(self.proposal_name)
        data.append(self.proposal_partner)
        data.append(self.create_date)
        data.append(self.status)

        return data
