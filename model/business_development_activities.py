class BusinessDevelopmentActivities:
    """
    Class used to represent company entity

    Attributes:
        company(Company):
        id(str):
        subject(str):
        details(str):
        activity_date(str):
        contact(str):
        category(str):
    """
    def __init__(self, company, id, subject, details, activity_date, contact, category):
        self.company = company
        self.id = id
        self.subject = subject
        self.details = details
        self.activity_date = activity_date
        self.contact = contact
        self.category = category
