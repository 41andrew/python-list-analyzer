from .base_row import BaseRow
from .entity import Entity


class BusinessDevelopmentActivities(BaseRow):
    """
    Class used to represent row from file with Business Development Activities

    Attributes:
        entity(Entity): object of Entity class composed in this row
        bda_id(str):
        subject(str):
        details(str):
        activity_date(str):
        contact(str):
        category(str):
    """

    COLUMN_NAMES = ["NIP", "NATIONAL_ACCOUNT", "ENTITY_NAME", "DESCRIPTION", "BDA_ID", "SUBJECT", "DETAILS",
                    "ACTIVITY_DATE", "CONTACT", "CATEGORY"]

    def __init__(self, entity, bda_id, subject, details, activity_date, contact, category):
        self.entity = entity
        self.bda_id = bda_id
        self.subject = subject
        self.details = details
        self.activity_date = activity_date
        self.contact = contact
        self.category = category

    def __str__(self):
        return "[{0.entity}][{0.bda_id}][{0.subject}][{0.details}][{0.activity_date}][{0.contact}]"\
               "[{0.category}]".format(self)

    def print_attributes_separated_by_semicolon(self):
        return "{0.entity};{0.bda_id};{0.subject};{0.details};{0.activity_date};{0.contact};{0.category}".format(self)

    def get_column_values_as_list(self):
        data = list()
        data.extend(self.entity.get_column_values_as_list())
        data.append(self.bda_id)
        data.append(self.subject)
        data.append(self.details)
        data.append(self.activity_date)
        data.append(self.contact)
        data.append(self.category)

        return data
