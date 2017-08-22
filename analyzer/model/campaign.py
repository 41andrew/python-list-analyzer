from .base_row import BaseRow


class Campaign(BaseRow):

    COLUMN_NAMES = ["CAMPAIGN_ID", "CAMPAIGN_NAME", "NIP", "NAME", "LAST_CALL", "LAST_COMMENT"]

    def __init__(self, campaign_id, campaign_name, nip, name, last_call, last_comment):
        super().__init__()
        self.campaign_id = campaign_id
        self.campaign_name = campaign_name
        self.nip = nip
        self.name = name
        self.last_call = last_call
        self.last_comment = last_comment

    def get_column_values_as_list(self):
        data = list()
        data.append(self.campaign_id)
        data.append(self.campaign_name)
        data.append(self.nip)
        data.append(self.name)
        data.append(self.last_call)
        data.append(self.last_comment)

        return data

    def print_attributes_separated_by_semicolon(self):
        return "{0.campaign_id};{0.campaign_name};{0.nip};{0.name};{0.last_call};{0.last_comment};".format(self)
