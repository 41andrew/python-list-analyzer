from model.calculations_target import CalculationsObject
from model.engagement import Engagement
from model.company import Company


class DataLoader:
    """
    Class used to load data from input .csv files

    Attributes:
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
        self.calculations_target = {}

    def read_calculations_targets_from_source(self):
        with open(self.default_data_paths['input_file_source'], 'r', encoding='utf8') as source_file:
            for line in source_file.readlines():
                data = line.strip('\n').split(sep=';')
                calc = CalculationsObject(data[0], data[1], data[2])
                self.calculations_target[calc.nip] = calc

    def read_engagements_from_file(self):
        with open(self.default_data_paths['input_file_engagements'], 'r', encoding='utf8') as source_file:
            for line in source_file.readlines():
                data = line.strip('\n').split(sep=';')
                comp = Company(data[0], data[1], data[2], data[3])
                eng = Engagement(comp, data[4], data[5], data[6], data[7], data[8])
                self.calculations_target[comp.nip].engagements.append(eng)
