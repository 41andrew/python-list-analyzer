from ..model.input_row import Category

class Reporter:

    def __init__(self):
        self.__not_assigned_count = 0
        self.__accepted_count = 0
        self.__to_check_count = 0
        self.__not_accepted_count = 0
        self.__execution_time = 0

    def set_report_result(self, input_rows):
        print("set_report_result")
        self.__not_assigned_count = sum(map(Reporter.__condition_for_certain_category, input_rows))
        print(self.__not_assigned_count)
        # self.__accepted_count = accepted
        # self.__to_check_count = to_check
        # self.__not_accepted_count = not_accepted

    def set_execution_time(self, execution_time):
        self.__execution_time = execution_time

    @staticmethod
    def __condition_for_certain_category(expected_category):
        return expected_category == Category.NOT_ASSIGNED


class HtmlReporter(Reporter):

    def __init__(self):
        super().__init__()
        self.__page_name = "report.html"
        self.__page_content = ""
        self.__output_directory = "output_raport"
        self.__output_file_path = "{}/{}"
        self.__header = ""\
"""
<!DOCTYPE html>
<html lang="en">
<head lang=en>
    <meta charset="UTF-8">
    <title>Report</title>
    <link 
        rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css" 
        integrity="sha384-BVYiiSIFeK1dGmJRAkycuHAHRg32OmUcww7on3RYdg4Va+PmSTsz/K68vbdEjh4u" 
        crossorigin="anonymous">
</head>
<body>
"""
        self.__footer = """
<script 
    src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js" 
    integrity="sha384-Tc5IQib027qvyjSMfHjOMaLkfuWVxZxUPnCJA7l2mCWNIpG9mGCD8wGNIcPD7Txa" 
    crossorigin="anonymous"></script>
</body>
</html>
"""

    def create_report_page(self):
        page_path = self.__output_file_path.format(self.__output_directory, self.__page_name)

        with open(page_path, 'w') as report_page:
            print(self.__build_page_content(), file=report_page)

    def __build_page_content(self):
        self.__page_content += self.__header
        self.__page_content += self.__footer
        return self.__page_content


