from .base_row import BaseRow
from .entity import Entity


class Engagement(BaseRow):
    """
    Class used to represent row from file with Engagements

    Attributes:
        entity(Entity): object of Entity class composed in this row
        engagement_code(str):
        engagement_name(str):
        engagement_partner(str):
        create_date(str):
        status(EngagementStatus):
    """

    COLUMN_NAMES = ["NIP", "NATIONAL_ACCOUNT", "ENTITY_NAME", "DESCRIPTION","CODE", "ENGAGEMENT_NAME",
                    "ENGAGEMENT_PARTNER", "CREATE_DATE", "STATUS"]

    def __init__(self, entity, engagement_code, engagement_name,
                 engagement_partner, create_date, status):

        self.entity = entity
        self.engagement_code = engagement_code
        self.engagement_name = (engagement_name).encode('windows-1250', 'ignore').decode('windows-1250')
        self.engagement_partner = engagement_partner
        self.create_date = create_date
        self.status = status

    def __str__(self):
        return "[{0.entity}][{0.engagement_code}][{0.engagement_name}][{0.engagement_partner}]"\
            "[{0.create_date}][{0.status}]".format(self)

    def is_active(self):
        return self.status.upper() == "ACTIVE"

    def print_attributes_separated_by_semicolon(self):
        return "{0.entity};{0.engagement_code};{0.engagement_name};{0.engagement_partner};{0.create_date};" \
               "{0.status};".format(self)

    def get_column_values_as_list(self):
        data = list()
        data.extend(self.entity.get_column_values_as_list())
        data.append(self.engagement_code)
        data.append(self.engagement_name)
        data.append(self.engagement_partner)
        data.append(self.create_date)
        data.append(self.status)

        return data
