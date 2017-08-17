class Engagement:
    """
    Class used to represent engagement between capital group and particular company

    Attributes:
        company(Company):
        engagement_code(str):
        engagement_name(str):
        engagement_partner(str):
        create_date(str):
        status(str):
    """

    def __init__(self, company, engagement_code, engagement_name,
                 engagement_partner, create_date, status):

        self.company = company
        self.engagement_code = engagement_code
        self.engagement_name = engagement_name
        self.engagement_partner = engagement_partner
        self.create_date = create_date
        self.status = status
