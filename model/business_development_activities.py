class BusinessDevelopmentActivities:
    """
    Class used to represent company entity

    Attributes:
        entity(Company):
        bda_id(str):
        subject(str):
        details(str):
        activity_date(str):
        contact(str):
        category(str):
    """

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
