import psycopg2
from ..utilities.properties_reader import PropertiesReader

class PostGreDataLoader:

    CAMPAIGN_ID_LIST = [10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28,
                        29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47,
                        48, 49, 50, 51]

    all_campaigns = []

    def __init__(self):
        self.props = PropertiesReader.get_properties_file_as_dict()
        self.conn = None

    def connect_to_pgsql(self):
        try:
            self.conn = psycopg2.connect("dbname='ContactDirect' user='master' host='{}' password='{}'".format(self.props['host'],self.props['pass']))
        except Exception as e:
            print (e)

    def load_data(self):

        self.connect_to_pgsql()

        cursor = self.conn.cursor()

        sql = """SELECT * FROM "Custom"."GetRecordsToExport"((%s), '2017-08-01', '2017-08-10'"""

        for x in self.CAMPAIGN_ID_LIST:
            cursor.execute(sql, (x))
            self.all_campaigns.extend(cursor.fetchall())


