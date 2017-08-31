import pyodbc
from .data_loader import CsvDataLoader
from ..model.engagement import Engagement
from ..model.proposal import Proposal
from ..model.relationship import Relationship
from ..model.bda import BusinessDevelopmentActivities
from ..model.entity import Entity
from ..model.restricted_services import RestrictedServices
from ..reporter.reporter import HtmlReporter


class CrmDataLoader:

    no_national_account = ['none', 'Other']
    crm_engagements = []
    crm_proposals = []
    crm_bda = []

    def __init__(self):
        self.conn = None
        self.input_from_csv = CsvDataLoader().get_input_rows_as_dict()
        self.connect_to_crm()
        self.engagements_date = '2015'

    def connect_to_crm(self):

        try:
            self.conn = pyodbc.connect(r'DRIVER={SQL Server};SERVER=plwawdb20,1113;DATABASE=MARS4_API;Trusted_Connection=yes;')
            print("Connected to database")
        except Exception as e:
            print("Unable to connect to the database")
            print("Error msg : {}".format(e))

    def is_nip_in_crm(self, nip):

        cursor = self.conn.cursor()

        sql = """SELECT en.EntityName
                FROM ems.v_Entity en
                WHERE en.TaxNumber = (?)"""

        cursor.execute(sql, nip)

        if cursor.rowcount != 0:
            print ("NIP {} jest w CRMie".format(nip))
            return True
        else:
            print ("NIPu {} nie ma w CRMie".format(nip))
            return False

    def find_nationalaccount_for_input_nip(self, nip):

        cursor = self.conn.cursor()

        sql = """SELECT na.NationalAccount
                FROM ems.v_Entity en LEFT JOIN
                        ems.v_NationalAccount na ON na.NationalAccount_ID = en.NationalAccount_ID
                WHERE en.TaxNumber = (?)"""

        cursor.execute(sql, nip)

        # Pobieram nazwę grupy kapitałowej

        if cursor.rowcount != 0:
            capital_group = (cursor.fetchone()[0])
            print("NIP: {} ma grupę kapitałową: {}".format(nip, capital_group))
            return capital_group
        else:
            print("Brak NIPu w CRMie")
            pass

    def find_engagements_for_nationalaccount(self, account):

        cursor = self.conn.cursor()

        sql = """SELECT en.TaxNumber, na.NationalAccount, en.EntityName, cl.Description, eg.EngagementCode, eg.EngagementName, CONCAT(em.LastName, ' ', em.FirstName) AS 'EngagementPartner', eg.CreateDate, es.Status
              FROM ems.v_Engagement eg INNER JOIN
                        ems.v_Entity en ON eg.Entity_ID = en.Entity_ID LEFT JOIN
                        ems.v_NationalAccount na ON en.NationalAccount_ID = na.NationalAccount_ID INNER JOIN
                        ems.v_EntityAdditional ea ON en.Entity_ID = ea.Entity_ID LEFT JOIN
                        ems.v_CustomList cl ON ea.SentinelCategory_ID = cl.CustomList_ID LEFT JOIN
                        ems.v_Employee em ON eg.EngagementPartner_ID = em.Employee_ID INNER JOIN
                        ems.v_EngagementStatus es ON eg.EngagementStatus_ID = es.EngagementStatus_ID
              WHERE na.NationalAccount = (?) AND eg.CreateDate >= '2015'
				"""

        cursor.execute(sql, account)

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
                    WHERE na.NationalAccount = (?) AND pr.CreateDate >= '2017'"""

        cursor.execute(sql, account)

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
                    WHERE na.NationalAccount = (?) AND bd.ActivityDate >= '2017'"""

        cursor.execute(sql, account)

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
                      WHERE en.TaxNumber = (?) AND eg.CreateDate >= '2017'
        				"""

        cursor.execute(sql, nip)
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
                    WHERE en.TaxNumber = (?) AND pr.CreateDate >= '2017'"""

        cursor.execute(sql, nip)
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
                    WHERE en.TaxNumber = (?) AND bd.ActivityDate >= '2017'"""

        cursor.execute(sql, nip)
        return cursor.fetchall()

    def find_relationship(self, nip):

        cursor = self.conn.cursor()

        sql = """SELECT en.TaxNumber, en.EntityName, CONCAT(co.FirstName, ' ', co.LastName), CONCAT(em.FirstName, ' ', em.LastName), cr.ContactRelationship
                    FROM ems.v_Entity en INNER JOIN
                                    ems.v_Occupation oc ON en.Entity_ID = oc.Entity_ID INNER JOIN
                                    ems.v_Contact co ON oc.Contact_ID = co.Contact_ID INNER JOIN
                                    ems.v_ContactDepContact cdc ON co.Contact_ID = cdc.Contact_ID INNER JOIN
                                    ems.v_Employee em ON cdc.Employee_ID = em.Employee_ID LEFT JOIN
                                    ems.v_ContactRelationship cr ON cdc.ContactRelationship_ID = cr.ContactRelationship_ID
                    WHERE cr.ContactRelationship = 'High' AND co.FirstName <> 'Other' AND co.FirstName <> 'Markets' AND en.TaxNumber = (?)"""

        cursor.execute(sql, nip)
        return cursor.fetchall()

    def find_restricted_services(self, nip):

        cursor = self.conn.cursor()

        sql = """SELECT en.TaxNumber, en.entityName, COUNT(gt.GTOST) AS 'ilosc restricted services'
                    FROM ems.v_Entity en INNER JOIN
                                    ems.v_RestrictedServices rs ON en.Entity_ID = rs.Entity_ID INNER JOIN
                                    ems.v_GTOST gt ON rs.GTOST_ID = gt.GTOST_ID
                    WHERE en.IsActive = 'TRUE' AND en.TaxNumber = (?)
                    GROUP BY EntityName, TaxNumber
                    HAVING COUNT(gt.GTOST) = 5 OR COUNT(gt.GTOST) = 6"""

        cursor.execute(sql, nip)
        return cursor.fetchall()

    def get_crm_name(self, nip):

        cursor = self.conn.cursor()

        sql = """SELECT en.EntityName
                    FROM ems.v_Entity en
                    WHERE en.TaxNumber = (?)"""

        cursor.execute(sql, nip)
        return cursor.fetchall()

    def load_data_from_crm2(self):

        for nip in self.input_from_csv:

            if self.is_nip_in_crm(nip):

                crm_name_from_db = self.get_crm_name(nip)

                self.input_from_csv[nip].company_name_in_crm = crm_name_from_db[0][0]
            else:
                self.input_from_csv[nip].company_name_in_crm = """<strong><font color="red">BRAK NIPu W CRM</font></strong>"""

            grupa = self.find_nationalaccount_for_input_nip(nip)
            is_in_crm = self.is_nip_in_crm(nip)


            relationships_from_db = self.find_relationship(nip)

            for relationship_row in relationships_from_db:
                relationship = Relationship(nip=relationship_row[0],
                                            entity_name=relationship_row[1],
                                            contact_name=relationship_row[2],
                                            kpmg_employee=relationship_row[3],
                                            relationship=relationship_row[4])
                self.input_from_csv[nip].relationships.append(relationship)

            restricted_services_from_db = self.find_restricted_services(nip)

            for restricted_row in restricted_services_from_db:
                restricted = RestrictedServices(nip=restricted_row[0],
                                                entity_name=restricted_row[1],
                                                count=restricted_row[2])
                self.input_from_csv[nip].restricted_services.append(restricted)


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
