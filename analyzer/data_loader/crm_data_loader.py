import pyodbc

class CrmDataLoader:

    crm_engagements = []

    def __init__(self):
        self.conn = None

    def connect_to_crm(self):

        try:
            conn = pyodbc.connect(r'DRIVER={SQL Server};SERVER=plwawdb20,1113;DATABASE=MARS4_API;Trusted_Connection=yes;')
        except:
            print ("Unable to connect to the database")


    def load_engagements_from_crm(self):

        self.connect_to_crm()

        cursor = self.conn.cursor()

        sql = """SELECT eg.EngagementName FROM ems.v_Engagement eg"""

        cursor.execute(sql)
        self.crm_engagements = cursor.fetchall()

        print (self.crm_engagements)
