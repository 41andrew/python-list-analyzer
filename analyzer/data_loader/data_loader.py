from ..model.engagement import Engagement
from ..model.input_row import InputRow
from ..model.proposal import Proposal
from ..model.bda import BusinessDevelopmentActivities
from ..model.entity import Entity
import os
import tkinter as tk
from tkinter import filedialog


class CsvDataLoader:
    """
    Class used to load data from input .csv files

    Attributes:
        input_files_directory(str): default directory where input files are stored
        data_paths(dict): locations of input files
        input_entities(dict): dictionary of input entities, with nip as keys
        error_messages(set(list(str)): if data loading gone wrong, error messages will be stored in this set
    """

    def __init__(self):
        root = tk.Tk()
        root.withdraw
        self.input_files_directory = "source_files"
        self.data_paths = {
            'input_file_source': "{}/input.csv".format(self.input_files_directory),
            'input_file_crm_names': "{}/company_names.csv".format(self.input_files_directory),
            'input_file_engagements': "{}/engagements.csv".format(self.input_files_directory),
            'input_file_proposals': "{}/proposals.csv".format(self.input_files_directory),
            'input_file_bda': "{}/bda.csv".format(self.input_files_directory)
        }
        self.data_path_input = filedialog.askopenfilename()
        self.input_entities = {}
        self.error_messages = set([])

    def load_data(self):
        """
            Method responsible for loading data from all input csv files step by step
            The only one 'public' method available from outside
            After loading, data will be in input_entities dict
        """

        self.error_messages = set([])
        self._add_input_rows_to_dict()
        self._add_crm_names_to_input_rows()
        self._add_engagements_to_corresponding_input_row()
        self._add_proposals_to_corresponding_input_row()
        self._add_bda_to_corresponding_input_row()

    def get_input_rows_as_dict(self):
        self._add_input_rows_to_dict()
        return self.input_entities

    def _read_lines_from_file(self, file_path_key):
        """
        Method read all lines from file under given path

        :param(str) file_path_key: key of the path to the file in dict
        :raise FileNotFoundError: when file is not found
        :return: List(str) of lines from file
        """
        print("Actually reading file : {}".format(os.path.abspath(self.data_paths[file_path_key])))

        try:
            with open(self.data_path_input, 'r', encoding='windows-1250', errors='ignore') as source_file:
                return source_file.readlines()
        except FileNotFoundError as e:
            print(e)
            self.error_messages.add("File {} not found".format(file_path_key))

    def _add_input_rows_to_dict(self):
        """
        Method adds input rows to dict

        :return: None
        """

        file_path_key_in_dict = "input_file_source"

        for line in self._read_lines_from_file(file_path_key_in_dict):
            input_entity = self._parse_object_from_semicolon_separated_line(line, file_path_key_in_dict)
            self.input_entities[input_entity.nip] = input_entity

    def _add_engagements_to_corresponding_input_row(self):
        """
        Method responsible for adding engagements to input row engagements collection, for input row
        with same NIP as engagement

        :return: None
        """

        file_path_key_in_dict = "input_file_engagements"

        for line in self._read_lines_from_file(file_path_key_in_dict):
            engagement = self._parse_object_from_semicolon_separated_line(line, file_path_key_in_dict)
            self._add_element_to_input_row_collection(engagement, "engagements")

    def _add_proposals_to_corresponding_input_row(self):
        """
        Method responsible for adding proposals to input row proposals collection, for input row
        with same NIP as proposal

            :return: None
        """

        file_path_key_in_dict = "input_file_proposals"

        for line in self._read_lines_from_file(file_path_key_in_dict):
            proposal = self._parse_object_from_semicolon_separated_line(line, file_path_key_in_dict)
            self._add_element_to_input_row_collection(proposal, "proposals")

    def _add_bda_to_corresponding_input_row(self):
        """
        Method responsible for adding bda to input row bda collection, for input row
        with same NIP as bda

            :return: None
        """

        file_path_key_in_dict = "input_file_bda"

        for line in self._read_lines_from_file(file_path_key_in_dict):
            bda = self._parse_object_from_semicolon_separated_line(line, file_path_key_in_dict)
            self._add_element_to_input_row_collection(bda, "bda")

    def _add_element_to_input_row_collection(self, element, collection):
        """
        Method responsible for adding element to one of input row lists,if it exists in dictionary

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

    def _add_crm_names_to_input_rows(self):
        # TODO implement this method
        pass

    def _parse_object_from_semicolon_separated_line(self, line, file_path_key_in_dict):
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
                input_entity = InputRow(line[0],
                                        line[1])
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

        except IndexError as e:
            print(e)
            self.error_messages.add("Exception while creating {} object - bal line parsing".format(file_path_key_in_dict))
        except TypeError as e:
            print(e)
            self.error_messages.add("Exception while creating {} object".format(file_path_key_in_dict))
