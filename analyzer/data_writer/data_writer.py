from ..model.input_row import Category


class CsvDataWriter:

    def __init__(self):
        self.__input_rows = None
        self.__output_directory = "output_files"
        self.__output_file_path = "{}/{}"

    @property
    def input_rows(self):
        return self.__input_rows

    @input_rows.setter
    def input_rows(self, input_rows):
        self.__input_rows = input_rows

    def write_category_assignment_result_to_file(self, file_name):

        file_path = self.__output_file_path.format(self.__output_directory, file_name)

        with open(file_path, 'w', encoding="UTF-8") as output_file:
            for row in self.__input_rows:

                if row.category == Category.TO_CHECK:
                    self.__print_to_check_input_row(row, output_file)
                else:
                    self.__print_input_row(row, output_file)

    @staticmethod
    def __print_to_check_input_row(row, file):
        CsvDataWriter.__print_input_row(row, file)
        CsvDataWriter.__print_collection("Engagements : [{}]".format(len(row.engagements)), row.engagements, file)
        CsvDataWriter.__print_collection("Proposals : [{}]".format(len(row.proposals)), row.proposals, file)
        CsvDataWriter.__print_collection("Bda : [{}]".format(len(row.bda)), row.bda, file)

    @staticmethod
    def __print_input_row(row, file):
        print(row.print_attributes_separated_by_semicolon(), file=file)

    @staticmethod
    def __print_collection(collection_name, collection, file):
        print(collection_name, file=file)

        for element in collection:
            print(element.print_attributes_separated_by_semicolon(), file=file)
