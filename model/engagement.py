class Engagement:
    """
    Class used to represent engagement between capital group and particular company

    Attributes:
        company(Company):
        engagement_code(str):
        engagement_name(str):
        engagement(str):
        partner(str):
        create_date(str):
        status(str):
    """

    def __init__(self, company, engagement_code, engagement_name,
                 engagement, partner, create_date, status):

        self.company = company
        self.engagement_code = engagement_code
        self.engagement_name = engagement_name
        self.engagement = engagement
        self.partner = partner
        self.create_date = create_date
        self.status = status
