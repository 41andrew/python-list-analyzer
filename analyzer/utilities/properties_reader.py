class PropertiesReader:

    __default_properties_path = "source_files/db.properties"

    @staticmethod
    def get_properties_file_as_dict(properties_file_path=""):
        properties_as_lines = PropertiesReader.__get_lines_from_file(properties_file_path)
        properties_dict = PropertiesReader.__create_dict_from_lines(properties_as_lines)

        return properties_dict

    @staticmethod
    def __get_lines_from_file(file_path):

        if PropertiesReader.__is_property_path_invalid(file_path):
            file_path = PropertiesReader.__default_properties_path

        try:
            with open(file_path, encoding='utf-8') as properties_file:
                return properties_file.readlines()
        except FileExistsError as file_error:
            PropertiesReader.__log_error(file_error)
        except Exception as exception:
            PropertiesReader.__log_error(exception)

    @staticmethod
    def __is_property_path_invalid(path):
        return path is None or len(path) == 0

    @staticmethod
    def __log_error(exception):
        print("An error has occurred")
        print(exception)

    @staticmethod
    def __create_dict_from_lines(properties_as_lines=[]):
        properties_dict = {}

        for line in properties_as_lines:
            splitted_line_as_list = line.rstrip('\n').rstrip('\r\n').split(sep="=")

            if PropertiesReader.__is_property_line_valid(splitted_line_as_list):
                property_key = splitted_line_as_list[0]
                property_value = splitted_line_as_list[1]
                properties_dict[property_key] = property_value

        return properties_dict

    @staticmethod
    def __is_property_line_valid(splitted_line_as_list):
        return len(splitted_line_as_list) == 2
