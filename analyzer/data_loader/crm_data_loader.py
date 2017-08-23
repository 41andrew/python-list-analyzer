import pyodbc

class CrmDataLoader:

    input_nips = ['5252223038', '6491110585']
    no_national_account = ['none', 'Other']
    crm_engagements = []
    crm_proposals = []
    crm_bda = []

    def __init__(self):
        self.conn = None
        self.connect_to_crm()

    def connect_to_crm(self):

        try:
            self.conn = pyodbc.connect(r'DRIVER={SQL Server};SERVER=plwawdb20,1113;DATABASE=MARS4_API;Trusted_Connection=yes;')
            print ("Connected to database")
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

        capital_group = (cursor.fetchone()[0])

        print (capital_group)

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

    def find_proposals_for_nationalaccount(self, account):

        cursor = self.conn.cursor()

        sql = """SELECT na.NationalAccount, en.EntityName, cl.Description, pr.Proposal_ID, pr.ProposalName, CONCAT(em.LastName, ' ', em.FirstName) AS 'ProposalPartner', pr.CreateDate, ps.Status
                    FROM ems.v_Proposal pr INNER JOIN
                                    ems.v_Entity en ON pr.Entity_ID = en.Entity_ID LEFT JOIN
                                    ems.v_NationalAccount na ON en.NationalAccount_ID = na.NationalAccount_ID INNER JOIN
                                    ems.v_EntityAdditional ea ON en.Entity_ID = ea.Entity_ID LEFT JOIN
                                    ems.v_CustomList cl ON ea.SentinelCategory_ID = cl.CustomList_ID LEFT JOIN
                                    ems.v_Employee em ON pr.KpmgContact_ID = em.Employee_ID INNER JOIN
                                    ems.v_ProposalStatus ps ON pr.ProposalStatus_ID = ps.ProposalStatus_ID
                    WHERE na.NationalAccount = '{}'"""

        cursor.execute(sql.format(account))

        self.crm_proposals.extend(cursor.fetchall())

    def find_bda_for_nationalaccount(self, account):

        cursor = self.conn.cursor()

        sql = """SELECT na.NationalAccount, en.EntityName, cl.Description, bd.BDActivity_ID, bd.Subject, bd.Details, bd.ActivityDate, CONCAT(em.LastName, ' ', em.FirstName) AS 'KPMG Contact', bdc.Category
                    FROM ems.v_BDActivity bd INNER JOIN
                                    ems.v_Entity en ON bd.Entity_ID = en.Entity_ID LEFT JOIN
                                    ems.v_NationalAccount na ON en.NationalAccount_ID = na.NationalAccount_ID INNER JOIN
                                    ems.v_EntityAdditional ea ON en.Entity_ID = ea.Entity_ID LEFT JOIN
                                    ems.v_CustomList cl ON ea.SentinelCategory_ID = cl.CustomList_ID  LEFT JOIN
                                    ems.v_Employee em ON bd.Employee_ID = em.Employee_ID INNER JOIN
                                    ems.v_BDActivityCategory bdc ON bd.BDActivityCategory_ID = bdc.BDActivityCategory_ID
                    WHERE na.NationalAccount = '{}'"""

        cursor.execute(sql.format(account))

        self.crm_bda.extend(cursor.fetchall())

    def find_engagements_for_nip(self, nip):

        cursor = self.conn.cursor()

        sql = """SELECT na.NationalAccount, en.EntityName, cl.Description, eg.Engagement_ID, eg.EngagementName, CONCAT(em.LastName, ' ', em.FirstName) AS 'EngagementPartner', es.Status
                      FROM ems.v_Engagement eg INNER JOIN
                                ems.v_Entity en ON eg.Entity_ID = en.Entity_ID LEFT JOIN
                                ems.v_NationalAccount na ON en.NationalAccount_ID = na.NationalAccount_ID INNER JOIN
                                ems.v_EntityAdditional ea ON en.Entity_ID = ea.Entity_ID LEFT JOIN
                                ems.v_CustomList cl ON ea.SentinelCategory_ID = cl.CustomList_ID LEFT JOIN
                                ems.v_Employee em ON eg.EngagementPartner_ID = em.Employee_ID INNER JOIN
                                ems.v_EngagementStatus es ON eg.EngagementStatus_ID = es.EngagementStatus_ID
                      WHERE en.TaxNumber = '{}'
        				"""

        cursor.execute(sql.format(nip))
        self.crm_engagements.extend(cursor.fetchall())

    def find_proposals_for_nip(self, nip):

        cursor = self.conn.cursor()

        sql = """SELECT na.NationalAccount, en.EntityName, cl.Description, pr.Proposal_ID, pr.ProposalName, CONCAT(em.LastName, ' ', em.FirstName) AS 'ProposalPartner', pr.CreateDate, ps.Status
                    FROM ems.v_Proposal pr INNER JOIN
                                    ems.v_Entity en ON pr.Entity_ID = en.Entity_ID LEFT JOIN
                                    ems.v_NationalAccount na ON en.NationalAccount_ID = na.NationalAccount_ID INNER JOIN
                                    ems.v_EntityAdditional ea ON en.Entity_ID = ea.Entity_ID LEFT JOIN
                                    ems.v_CustomList cl ON ea.SentinelCategory_ID = cl.CustomList_ID LEFT JOIN
                                    ems.v_Employee em ON pr.KpmgContact_ID = em.Employee_ID INNER JOIN
                                    ems.v_ProposalStatus ps ON pr.ProposalStatus_ID = ps.ProposalStatus_ID
                    WHERE en.TaxNumber = '{}'"""

        cursor.execute(sql.format(nip))
        self.crm_proposals.extend(cursor.fetchall())

    def find_bda_for_nip(self, nip):

        cursor = self.conn.cursor()

        sql = """SELECT na.NationalAccount, en.EntityName, cl.Description, bd.BDActivity_ID, bd.Subject, bd.Details, bd.ActivityDate, CONCAT(em.LastName, ' ', em.FirstName) AS 'KPMG Contact', bdc.Category
                    FROM ems.v_BDActivity bd INNER JOIN
                                    ems.v_Entity en ON bd.Entity_ID = en.Entity_ID LEFT JOIN
                                    ems.v_NationalAccount na ON en.NationalAccount_ID = na.NationalAccount_ID INNER JOIN
                                    ems.v_EntityAdditional ea ON en.Entity_ID = ea.Entity_ID LEFT JOIN
                                    ems.v_CustomList cl ON ea.SentinelCategory_ID = cl.CustomList_ID  LEFT JOIN
                                    ems.v_Employee em ON bd.Employee_ID = em.Employee_ID INNER JOIN
                                    ems.v_BDActivityCategory bdc ON bd.BDActivityCategory_ID = bdc.BDActivityCategory_ID
                    WHERE en.TaxNumber = '{}'"""

        cursor.execute(sql.format(nip))
        self.crm_bda.extend(cursor.fetchall())


    def load_data_from_crm(self):

        self.connect_to_crm()

        for nip in self.input_nips:

            grupa = self.find_nationalaccount_for_input_nip(nip)

            if (grupa in self.no_national_account) or (not grupa):
                self.find_engagements_for_nip(nip)
                self.find_proposals_for_nip()
                self.find_bda_for_nip()
            else:
                self.find_engagements_for_nationalaccount(grupa)
                self.find_proposals_for_nationalaccount(grupa)
                self.find_bda_for_nationalaccount(grupa)



        print (self.crm_engagements)
        print ("")
        print (self.crm_proposals)
        print ("")
        print (self.crm_bda)
