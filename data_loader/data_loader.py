from model.input_entity import InputEntity
from model.engagement import Engagement
from model.entity import Entity
from model.proposal import Proposal
from model.business_development_activities import BusinessDevelopmentActivities


class CsvDataLoader:
    """
    Class used to load data from input .csv files

    Attributes:
        default_input_files_directory(str): default directory where input files are stored
        default_data_paths(dict): default locations of input files
        input_entities(dict): dictionary of input entities, with nip as keys
    """

    def __init__(self):
        self.default_input_files_directory = "source_files"
        self.default_data_paths = {
            'input_file_source': "{}/input.csv".format(self.default_input_files_directory),
            'input_file_crm_names': "{}/company_names.csv".format(self.default_input_files_directory),
            'input_file_engagements': "{}/engagements.csv".format(self.default_input_files_directory),
            'input_file_proposals': "{}/proposals.csv".format(self.default_input_files_directory),
            'input_file_bda': "{}/bda.csv".format(self.default_input_files_directory)
        }
        self.input_entities = {}

    def read_from_input_csv_files(self):
        """
        Method responsible for loading data from input csv files

        :return: dict of loaded from csv file input entities
        """

        self.read_input_entities()
        self.read_crm_names()
        self.read_engagements_from_file()
        self.read_proposals_from_file()
        self.read_bda_from_file()

    def read_crm_names(self):
        # TODO implement this method
        pass

    def read_input_entities(self):
        """
        Method responsible for loading data from input_file_source

        :return: None
        """

        with open(self.default_data_paths['input_file_source'], 'r', encoding='utf8') as source_file:
            for line in source_file.readlines():
                input_entity_data = line.strip('\n').split(sep=';')
                input_entity = InputEntity(input_entity_data[0],
                                           input_entity_data[1],
                                           input_entity_data[2])
                self.input_entities[input_entity.nip] = input_entity

    def read_engagements_from_file(self):
        """
        Method responsible for loading data from input_file_engagements

        :return: None
        """

        with open(self.default_data_paths['input_file_engagements'], 'r', encoding='utf8') as source_file:
            for line in source_file.readlines():
                engagements_data = line.strip('\n').split(sep=';')
                entity = Entity(engagements_data[0], engagements_data[1],
                                engagements_data[2], engagements_data[3])
                engagement = Engagement(entity, engagements_data[4], engagements_data[5],
                                        engagements_data[6], engagements_data[7], engagements_data[8])
                self.add_element_to_entity_collection(engagement, "engagements")

    def read_proposals_from_file(self):
        """
        Method responsible for loading data from input_file_proposals

            :return: None
        """

        with open(self.default_data_paths['input_file_proposals'], 'r', encoding='utf8') as source_file:
            for line in source_file.readlines():
                proposal_data = line.strip('\n').split(sep=';')
                entity = Entity(proposal_data[0], proposal_data[1],
                                proposal_data[2], proposal_data[3])
                proposal = Proposal(entity, proposal_data[4], proposal_data[5],
                                    proposal_data[6], proposal_data[7], proposal_data[8])
                self.add_element_to_entity_collection(proposal, "proposals")

    def read_bda_from_file(self):
        """
        Method responsible for loading data from input_file_bda

            :return: None
        """

        with open(self.default_data_paths['input_file_bda'], 'r', encoding='utf8') as source_file:
            for line in source_file.readlines():
                bda_data = line.strip('\n').split(sep=';')
                entity = Entity(bda_data[0], bda_data[1],
                                bda_data[2], description="")
                proposal = BusinessDevelopmentActivities(entity, bda_data[3], bda_data[4], bda_data[5],
                                                         bda_data[6], bda_data[7], bda_data[8])
                self.add_element_to_entity_collection(proposal, "bda")

    def add_element_to_entity_collection(self, element, collection):
        """
        Method responsible for adding element to one of input entity lists,if it exists in dictionary

        :param element: element to be added to particular collection
        :param(str) collection: 'engagements' or 'proposals' or 'bda'
        :return: None
        """

        if element.entity.nip in self.input_entities:
            if collection == "engagements":
                self.input_entities[element.entity.nip].engagements.append(element)
            elif collection == "proposals":
                self.input_entities[element.entity.nip].proposals.append(element)
            elif collection == "bda":
                self.input_entities[element.entity.nip].bda.append(element)
