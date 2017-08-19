class Engagement:



    """
    Class used to represent engagement between capital group and particular company

    Attributes:
        entity(Entity):
        engagement_code(str):
        engagement_name(str):
        engagement_partner(str):
        create_date(str):
        status(EngagementStatus):
    """

    def __init__(self, entity, engagement_code, engagement_name,
                 engagement_partner, create_date, status):

        self.entity = entity
        self.engagement_code = engagement_code
        self.engagement_name = engagement_name
        self.engagement_partner = engagement_partner
        self.create_date = create_date
        self.status = status

    def __str__(self):
        return "[{0.entity}][{0.engagement_code}][{0.engagement_name}][{0.engagement_partner}]"\
            "[{0.create_date}][{0.status}]".format(self)

    def is_active(self):
        return self.status.upper() == "ACTIVE"
