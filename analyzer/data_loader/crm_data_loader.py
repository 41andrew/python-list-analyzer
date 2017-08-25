import pyodbc
from .data_loader import CsvDataLoader
from ..model.engagement import Engagement
from ..model.proposal import Proposal
from ..model.bda import BusinessDevelopmentActivities
from ..model.entity import Entity


class CrmDataLoader:

    input_nips = ['5252223038', '6491110585']
    no_national_account = ['none', 'Other']
    crm_engagements = []
    crm_proposals = []
    crm_bda = []

    def __init__(self):
        self.conn = None
        self.input_from_csv = CsvDataLoader().get_input_rows_as_dict()
        self.connect_to_crm()

    def connect_to_crm(self):

        try:
            self.conn = pyodbc.connect(r'DRIVER={SQL Server};SERVER=plwawdb20,1113;DATABASE=MARS4_API;Trusted_Connection=yes;')
            print("Connected to database")
        except Exception as e:
            print("Unable to connect to the database")
            print("Error msg : {}".format(e))

    def find_nationalaccount_for_input_nip(self, nip):

        cursor = self.conn.cursor()

        sql = """SELECT na.NationalAccount
                FROM ems.v_Entity en LEFT JOIN
                        ems.v_NationalAccount na ON na.NationalAccount_ID = en.NationalAccount_ID
                WHERE en.TaxNumber = '{}'"""

        cursor.execute(sql.format(nip))

        # Pobieram nazwę grupy kapitałowej
        capital_group = (cursor.fetchone()[0])

        print("NIP: {} ma grupę kapitałową: {}".format(nip, capital_group))

        return capital_group

    def find_engagements_for_nationalaccount(self, account):

        cursor = self.conn.cursor()

        sql = """SELECT en.TaxNumber, na.NationalAccount, en.EntityName, cl.Description, eg.Engagement_ID, eg.EngagementName, CONCAT(em.LastName, ' ', em.FirstName) AS 'EngagementPartner', eg.CreateDate, es.Status
              FROM ems.v_Engagement eg INNER JOIN
                        ems.v_Entity en ON eg.Entity_ID = en.Entity_ID LEFT JOIN
                        ems.v_NationalAccount na ON en.NationalAccount_ID = na.NationalAccount_ID INNER JOIN
                        ems.v_EntityAdditional ea ON en.Entity_ID = ea.Entity_ID LEFT JOIN
                        ems.v_CustomList cl ON ea.SentinelCategory_ID = cl.CustomList_ID LEFT JOIN
                        ems.v_Employee em ON eg.EngagementPartner_ID = em.Employee_ID INNER JOIN
                        ems.v_EngagementStatus es ON eg.EngagementStatus_ID = es.EngagementStatus_ID
              WHERE na.NationalAccount = N'{}' AND eg.CreateDate >= '2015'
				"""

        cursor.execute(sql.format(account))

        return cursor.fetchall()

    def find_proposals_for_nationalaccount(self, account):

        cursor = self.conn.cursor()

        sql = """SELECT en.TaxNumber, na.NationalAccount, en.EntityName, cl.Description, pr.Proposal_ID, pr.ProposalName, CONCAT(em.LastName, ' ', em.FirstName) AS 'ProposalPartner', pr.CreateDate, ps.Status
                    FROM ems.v_Proposal pr INNER JOIN
                                    ems.v_Entity en ON pr.Entity_ID = en.Entity_ID LEFT JOIN
                                    ems.v_NationalAccount na ON en.NationalAccount_ID = na.NationalAccount_ID INNER JOIN
                                    ems.v_EntityAdditional ea ON en.Entity_ID = ea.Entity_ID LEFT JOIN
                                    ems.v_CustomList cl ON ea.SentinelCategory_ID = cl.CustomList_ID LEFT JOIN
                                    ems.v_Employee em ON pr.KpmgContact_ID = em.Employee_ID INNER JOIN
                                    ems.v_ProposalStatus ps ON pr.ProposalStatus_ID = ps.ProposalStatus_ID
                    WHERE na.NationalAccount = N'{}' AND pr.CreateDate >= '2017'"""

        cursor.execute(sql.format(account))

        return cursor.fetchall()

    def find_bda_for_nationalaccount(self, account):

        cursor = self.conn.cursor()

        sql = """SELECT en.TaxNumber, na.NationalAccount, en.EntityName, cl.Description, bd.BDActivity_ID, bd.Subject, bd.Details, bd.ActivityDate, CONCAT(em.LastName, ' ', em.FirstName) AS 'KPMG Contact', bdc.Category
                    FROM ems.v_BDActivity bd INNER JOIN
                                    ems.v_Entity en ON bd.Entity_ID = en.Entity_ID LEFT JOIN
                                    ems.v_NationalAccount na ON en.NationalAccount_ID = na.NationalAccount_ID INNER JOIN
                                    ems.v_EntityAdditional ea ON en.Entity_ID = ea.Entity_ID LEFT JOIN
                                    ems.v_CustomList cl ON ea.SentinelCategory_ID = cl.CustomList_ID  LEFT JOIN
                                    ems.v_Employee em ON bd.Employee_ID = em.Employee_ID INNER JOIN
                                    ems.v_BDActivityCategory bdc ON bd.BDActivityCategory_ID = bdc.BDActivityCategory_ID
                    WHERE na.NationalAccount = N'{}' AND bd.ActivityDate >= '2017'"""

        cursor.execute(sql.format(account))

        return cursor.fetchall()

    def find_engagements_for_nip(self, nip):

        cursor = self.conn.cursor()

        sql = """SELECT en.TaxNumber, na.NationalAccount, en.EntityName, cl.Description, eg.EngagementCode, eg.EngagementName, CONCAT(em.LastName, ' ', em.FirstName) AS 'EngagementPartner', eg.CreateDate, es.Status
                      FROM ems.v_Engagement eg INNER JOIN
                                ems.v_Entity en ON eg.Entity_ID = en.Entity_ID LEFT JOIN
                                ems.v_NationalAccount na ON en.NationalAccount_ID = na.NationalAccount_ID INNER JOIN
                                ems.v_EntityAdditional ea ON en.Entity_ID = ea.Entity_ID LEFT JOIN
                                ems.v_CustomList cl ON ea.SentinelCategory_ID = cl.CustomList_ID LEFT JOIN
                                ems.v_Employee em ON eg.EngagementPartner_ID = em.Employee_ID INNER JOIN
                                ems.v_EngagementStatus es ON eg.EngagementStatus_ID = es.EngagementStatus_ID
                      WHERE en.TaxNumber = N'{}' AND eg.CreateDate >= '2017'
        				"""

        cursor.execute(sql.format(nip))
        return cursor.fetchall()

    def find_proposals_for_nip(self, nip):

        cursor = self.conn.cursor()

        sql = """SELECT en.TaxNumber, na.NationalAccount, en.EntityName, cl.Description, pr.Proposal_ID, pr.ProposalName, CONCAT(em.LastName, ' ', em.FirstName) AS 'ProposalPartner', pr.CreateDate, ps.Status
                    FROM ems.v_Proposal pr INNER JOIN
                                    ems.v_Entity en ON pr.Entity_ID = en.Entity_ID LEFT JOIN
                                    ems.v_NationalAccount na ON en.NationalAccount_ID = na.NationalAccount_ID INNER JOIN
                                    ems.v_EntityAdditional ea ON en.Entity_ID = ea.Entity_ID LEFT JOIN
                                    ems.v_CustomList cl ON ea.SentinelCategory_ID = cl.CustomList_ID LEFT JOIN
                                    ems.v_Employee em ON pr.KpmgContact_ID = em.Employee_ID INNER JOIN
                                    ems.v_ProposalStatus ps ON pr.ProposalStatus_ID = ps.ProposalStatus_ID
                    WHERE en.TaxNumber = N'{}' AND pr.CreateDate >= '2017'"""

        cursor.execute(sql.format(nip))
        return cursor.fetchall()

    def find_bda_for_nip(self, nip):

        cursor = self.conn.cursor()

        sql = """SELECT en.TaxNumber, na.NationalAccount, en.EntityName, cl.Description, bd.BDActivity_ID, bd.Subject, bd.Details, bd.ActivityDate, CONCAT(em.LastName, ' ', em.FirstName) AS 'KPMG Contact', bdc.Category
                    FROM ems.v_BDActivity bd INNER JOIN
                                    ems.v_Entity en ON bd.Entity_ID = en.Entity_ID LEFT JOIN
                                    ems.v_NationalAccount na ON en.NationalAccount_ID = na.NationalAccount_ID INNER JOIN
                                    ems.v_EntityAdditional ea ON en.Entity_ID = ea.Entity_ID LEFT JOIN
                                    ems.v_CustomList cl ON ea.SentinelCategory_ID = cl.CustomList_ID  LEFT JOIN
                                    ems.v_Employee em ON bd.Employee_ID = em.Employee_ID INNER JOIN
                                    ems.v_BDActivityCategory bdc ON bd.BDActivityCategory_ID = bdc.BDActivityCategory_ID
                    WHERE en.TaxNumber = N'{}' AND bd.ActivityDate >= '2017'"""

        cursor.execute(sql.format(nip))
        return cursor.fetchall()

    def load_data_from_crm(self):

        self.connect_to_crm()

        for nip in self.input_nips:

            grupa = self.find_nationalaccount_for_input_nip(nip)

            if (grupa in self.no_national_account) or (not grupa):
                self.input_nips2[nip].engagements = self.find_engagements_for_nip(nip)
                # self.find_engagements_for_nip(nip)
                self.find_proposals_for_nip(nip)
                self.find_bda_for_nip(nip)
            else:
                self.find_engagements_for_nationalaccount(grupa)
                self.find_proposals_for_nationalaccount(grupa)
                self.find_bda_for_nationalaccount(grupa)



        #print (self.crm_engagements)
        #print ("")
        #print (self.crm_proposals)
        #print ("")
        #print (self.crm_bda)

    def load_data_from_crm2(self):

        for nip in self.input_from_csv:

            grupa = self.find_nationalaccount_for_input_nip(nip)

            if (grupa in self.no_national_account) or (not grupa):
                engagements_from_db  = self.find_engagements_for_nip(nip)
                proposals_from_db = self.find_proposals_for_nip(nip)
                bda_from_db = self.find_bda_for_nip(nip)

                for engagement_row in engagements_from_db:
                    entity = Entity(nip=engagement_row[0],
                                    national_account=engagement_row[1],
                                    entity_name=engagement_row[2],
                                    description=engagement_row[3])
                    engagement = Engagement(entity=entity,
                                            engagement_code=engagement_row[4],
                                            engagement_name=engagement_row[5],
                                            engagement_partner=engagement_row[6],
                                            create_date=engagement_row[7],
                                            status=engagement_row[8])
                    self.input_from_csv[nip].engagements.append(engagement)

                for proposal_row in proposals_from_db:
                    entity = Entity(nip=proposal_row[0],
                                    national_account=proposal_row[1],
                                    entity_name=proposal_row[2],
                                    description=proposal_row[3])
                    proposal = Proposal(entity=entity,
                                        proposal_id=proposal_row[4],
                                        proposal_name=proposal_row[5],
                                        proposal_partner=proposal_row[6],
                                        create_date=proposal_row[7],
                                        status=proposal_row[8])
                    self.input_from_csv[nip].proposals.append(proposal)

                for bda_row in bda_from_db:
                    entity = Entity(nip=bda_row[0],
                                    national_account=bda_row[1],
                                    entity_name=bda_row[2],
                                    description=bda_row[3])
                    bda = BusinessDevelopmentActivities(entity=entity,
                                                        bda_id=bda_row[4],
                                                        subject=bda_row[5],
                                                        details=bda_row[6],
                                                        activity_date=bda_row[7],
                                                        contact=bda_row[8],
                                                        category=bda_row[9])
                    self.input_from_csv[nip].bda.append(bda)

            else:
                engagements_from_db = self.find_engagements_for_nationalaccount(grupa)
                proposals_from_db = self.find_proposals_for_nationalaccount(grupa)
                bda_from_db = self.find_bda_for_nationalaccount(grupa)

                for engagement_row in engagements_from_db:
                    entity = Entity(nip=engagement_row[0],
                                    national_account=engagement_row[1],
                                    entity_name=engagement_row[2],
                                    description=engagement_row[3])
                    engagement = Engagement(entity=entity,
                                            engagement_code=engagement_row[4],
                                            engagement_name=engagement_row[5],
                                            engagement_partner=engagement_row[6],
                                            create_date=engagement_row[7],
                                            status=engagement_row[8])
                    self.input_from_csv[nip].engagements.append(engagement)

                for proposal_row in proposals_from_db:
                    entity = Entity(nip=proposal_row[0],
                                    national_account=proposal_row[1],
                                    entity_name=proposal_row[2],
                                    description=proposal_row[3])
                    proposal = Proposal(entity=entity,
                                        proposal_id=proposal_row[4],
                                        proposal_name=proposal_row[5],
                                        proposal_partner=proposal_row[6],
                                        create_date=proposal_row[7],
                                        status=proposal_row[8])
                    self.input_from_csv[nip].proposals.append(proposal)

                for bda_row in bda_from_db:
                    entity = Entity(nip=bda_row[0],
                                    national_account=bda_row[1],
                                    entity_name=bda_row[2],
                                    description=bda_row[3])
                    bda = BusinessDevelopmentActivities(entity=entity,
                                                        bda_id=bda_row[4],
                                                        subject=bda_row[5],
                                                        details=bda_row[6],
                                                        activity_date=bda_row[7],
                                                        contact=bda_row[8],
                                                        category=bda_row[9])
                    self.input_from_csv[nip].bda.append(bda)
