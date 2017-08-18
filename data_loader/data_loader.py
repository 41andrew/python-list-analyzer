from model.input_entity import InputEntity
from model.engagement import Engagement
from model.entity import Entity
from model.proposal import Proposal
from model.business_development_activities import BusinessDevelopmentActivities


class CsvDataLoader:
    """
    Class used to load data from input .csv files

    Attributes:
        input_files_directory(str): default directory where input files are stored
        data_paths(dict): locations of input files
        input_entities(dict): dictionary of input entities, with nip as keys
    """

    def __init__(self):
        self.input_files_directory = "source_files"
        self.data_paths = {
            'input_file_source': "{}/input.csv".format(self.input_files_directory),
            'input_file_crm_names': "{}/company_names.csv".format(self.input_files_directory),
            'input_file_engagements': "{}/engagements.csv".format(self.input_files_directory),
            'input_file_proposals': "{}/proposals.csv".format(self.input_files_directory),
            'input_file_bda': "{}/bda.csv".format(self.input_files_directory)
        }
        self.input_entities = {}
        self.error_messages = set([])

    def load_data(self):
        """
        Method responsible for loading data from all input csv files
        """

        self.add_input_entities()
        self.add_crm_names_to_corresponding_input_entities()
        self.add_engagements_to_corresponding_input_entities()
        self.add_proposals_to_corresponding_input_entities()
        self.add_bda_to_corresponding_input_entities()

    def read_lines_from_file(self, file_path_key):
        """
        Method read all lines from file under given path

        :param(str) file_path_key: key of the path to the file in dict
        :raise FileNotFoundError: when file is not found
        :return: List(str) of lines from file
        """

        try:
            with open(self.data_paths[file_path_key], 'r', encoding='utf8') as source_file:
                return source_file.readlines()
        except FileNotFoundError:
            self.error_messages.add("File {} not found".format(file_path_key))
            return None

    def add_input_entities(self):
        """
        Method adds input entities to dict

        :return: None
        """

        file_path_key_in_dict = "input_file_source"

        for line in self.read_lines_from_file(file_path_key_in_dict):
            input_entity = self.parse_object_from_semicolon_separated_line(line, file_path_key_in_dict)
            self.input_entities[input_entity.nip] = input_entity

    def add_engagements_to_corresponding_input_entities(self):
        """
        Method responsible for adding engagements to its input entity collection

        :return: None
        """

        file_path_key_in_dict = "input_file_engagements"

        for line in self.read_lines_from_file(file_path_key_in_dict):
            engagement = self.parse_object_from_semicolon_separated_line(line, file_path_key_in_dict)
            self.add_element_to_entity_collection(engagement, "engagements")

    def add_proposals_to_corresponding_input_entities(self):
        """
        Method responsible for adding proposals to its input entity collection

            :return: None
        """

        file_path_key_in_dict = "input_file_proposals"

        for line in self.read_lines_from_file(file_path_key_in_dict):
            proposal = self.parse_object_from_semicolon_separated_line(line, file_path_key_in_dict)
            self.add_element_to_entity_collection(proposal, "proposals")

    def add_bda_to_corresponding_input_entities(self):
        """
        Method responsible for loading data from input_file_bda

            :return: None
        """

        file_path_key_in_dict = "input_file_bda"

        for line in self.read_lines_from_file(file_path_key_in_dict):
            bda = self.parse_object_from_semicolon_separated_line(line, file_path_key_in_dict)
            self.add_element_to_entity_collection(bda, "bda")

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

    def add_crm_names_to_corresponding_input_entities(self):
        # TODO implement this method
        pass

    def parse_object_from_semicolon_separated_line(self, line, file_path_key_in_dict):
        """
        Based on file_path_key_in_dict, different type of object is created

        :param(str) line: semicolon separated line which will be splited, and object will be created from line
            values
        :param(str) file_path_key_in_dict: key of the path to the file in dict
        :return: Created object
        """

        try:
            line = line.strip('\n').split(sep=';')
            if file_path_key_in_dict == "input_file_source":
                input_entity = InputEntity(line[0],
                                           line[1],
                                           line[2])
                return input_entity

            else:
                entity = Entity(line[0], line[1],
                                line[2], line[3])

                if file_path_key_in_dict == "input_file_engagements":
                    engagement = Engagement(entity, line[4], line[5], line[6], line[7], line[8])
                    return engagement

                elif file_path_key_in_dict == "input_file_proposals":
                    proposal = Proposal(entity, line[4], line[5], line[6], line[7], line[8])
                    return proposal

                elif file_path_key_in_dict == "input_file_bda":
                    bda = BusinessDevelopmentActivities(entity, line[4], line[5],
                                                        line[6], line[7], line[8], line[9])
                    return bda

        except IndexError:
            self.error_messages.add("Exception while creating {} object - bal line parsing".format(file_path_key_in_dict))
        except TypeError:
            self.error_messages.add("Exception while creating {} object".format(file_path_key_in_dict))
