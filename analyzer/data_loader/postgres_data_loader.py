import psycopg2
from ..utilities.properties_reader import PropertiesReader

class PostGreDataLoader:

    CAMPAIGN_ID_LIST = [35, 36, 40, 48]

    all_campaigns = []

    def __init__(self):
        self.props = PropertiesReader.get_properties_file_as_dict()
        self.conn = None

    def connect_to_pgsql(self):
        try:
            self.conn = psycopg2.connect("dbname='ContactDirect' user='master' host='{}' password='{}'".format(self.props['host'],self.props['pass']))
        except Exception as e:
            print (e)

    def load_data_from_pgs(self):

        self.connect_to_pgsql()

        cursor = self.conn.cursor()

        sql = """SELECT * FROM "Custom"."GetRecordsToExport"((%s), '2017-08-01', '2017-08-10'"""

        for x in self.CAMPAIGN_ID_LIST:
            cursor.execute(sql, (x))
            self.all_campaigns.extend(cursor.fetchall())

        print (self.all_campaigns)


