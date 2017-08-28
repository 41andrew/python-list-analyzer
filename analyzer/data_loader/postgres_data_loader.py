import psycopg2
from ..utilities.properties_reader import PropertiesReader
from .data_loader import CsvDataLoader
from ..model.engagement import Engagement
from ..model.proposal import Proposal
from ..model.bda import BusinessDevelopmentActivities
from ..model.entity import Entity
from ..model.campaign import Campaign


class PostGreDataLoader:

    CAMPAIGN_ID_LIST = [6, 7, 11, 14, 16, 17, 18, 19,
                        20, 21, 23, 24, 26, 27, 28, 29,
                        30, 31, 32, 33, 34, 35, 36, 37,
                        39, 40, 41, 42, 43, 44, 46, 47,
                        48, 49, 50]

    all_campaigns = []

    def __init__(self):
        self.props = PropertiesReader.get_properties_file_as_dict()
        # Tutaj nadpisywales input
        # self.input_from_csv = CsvDataLoader().get_input_rows_as_dict()
        self.input_from_csv = {}
        self.conn = None

    def set_input_from_csv(self, input_from_crm):
        self.input_from_csv = input_from_crm

    def connect_to_pgsql(self):
        try:
            self.conn = psycopg2.connect("dbname='ContactDirect' user='master' host='{}' password='{}'"
                                         .format(self.props['host'], self.props['pass']))
        except Exception as e:
            print("Exception while connecting with database")
            print("Error message : {}".format(e))

    def load_data_from_pgs(self):

        self.connect_to_pgsql()

        cursor = self.conn.cursor()

        sql = """SELECT * FROM "Custom"."GetRecordsToExport"(({}), '2017-08-01', '2017-08-10')"""

        for x in self.CAMPAIGN_ID_LIST:
            cursor.execute(sql.format(x))
            self.all_campaigns.extend(cursor.fetchall())

        for nip in self.input_from_csv:

            for campaign_row in self.all_campaigns:

                if nip == campaign_row[2]:

                    campaign = Campaign(campaign_id=campaign_row[0],
                                        campaign_name=campaign_row[1],
                                        nip=campaign_row[2],
                                        name=campaign_row[3],
                                        last_call=campaign_row[4],
                                        last_comment=[5])
                    self.input_from_csv[nip].campaigns.append(campaign)


        #print(self.all_campaigns)
