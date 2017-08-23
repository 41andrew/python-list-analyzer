import pyodbc

class CrmDataLoader:

    input_nips = ['5252223038', '6491110585']
    crm_engagements = []
    crm_proposals = []
    crm_bda = []

    def __init__(self):
        self.conn = None
        self.connect_to_crm()

    def connect_to_crm(self):

        try:
            conn = pyodbc.connect(r'DRIVER={SQL Server};SERVER=plwawdb20,1113;DATABASE=MARS4_API;Trusted_Connection=yes;')
        except:
            print ("Unable to connect to the database")

    def find_nationalaccount_for_input_nip(self, nip):

        capital_group = ""

        cursor = self.conn.cursor()

        sql = """SELECT na.NationalAccount
                FROM ems.v_Entity en LEFT JOIN
                        ems.v_NationalAccount na ON na.NationalAccount_ID = en.NationalAccount_ID
                WHERE en.TaxNumber = '{}'"""

        cursor.execute(sql.format(nip))

        capital_group = cursor.fetchall()

        return capital_group

    def find_engagements_for_nationalaccount(self, account):

        cursor = self.conn.cursor()

        sql = """SELECT na.NationalAccount, en.EntityName, cl.Description, eg.Engagement_ID, eg.EngagementName, CONCAT(em.LastName, ' ', em.FirstName) AS 'EngagementPartner', es.Status
              FROM ems.v_Engagement eg INNER JOIN
                        ems.v_Entity en ON eg.Entity_ID = en.Entity_ID LEFT JOIN
                        ems.v_NationalAccount na ON en.NationalAccount_ID = na.NationalAccount_ID INNER JOIN
                        ems.v_EntityAdditional ea ON en.Entity_ID = ea.Entity_ID LEFT JOIN
                        ems.v_CustomList cl ON ea.SentinelCategory_ID = cl.CustomList_ID LEFT JOIN
                        ems.v_Employee em ON eg.EngagementPartner_ID = em.Employee_ID INNER JOIN
                        ems.v_EngagementStatus es ON eg.EngagementStatus_ID = es.EngagementStatus_ID
              WHERE na.NationalAccount = '{}'
				"""

        cursor.execute(sql.format(account))

        self.crm_engagements.extend(cursor.fetchall())



    def load_engagements_from_crm(self):

        for nip in self.input_nips:
            grupa = self.find_nationalaccount_for_input_nip(nip)
            self.find_engagements_for_nationalaccount(grupa)



        print (self.crm_engagements)
