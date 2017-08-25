from ..model.input_row import Category
from .page_builder import HtmlPageBuilder
from ..model.input_row import InputRow
from ..model.engagement import Engagement
from ..model.proposal import Proposal
from ..model.bda import BusinessDevelopmentActivities
from ..model.campaign import Campaign


class Reporter:

    def __init__(self):
        self.input_rows = None
        self.not_assigned_count = 0
        self.accepted_count = 0
        self.to_check_count = 0
        self.not_accepted_count = 0
        self.execution_time = 0

    def set_report_result(self, input_rows):
        self.input_rows = input_rows

        self.not_assigned_count = sum(map(Reporter.__is_category_not_assigned, input_rows))
        self.accepted_count = sum(map(Reporter.__is_category_accepted, input_rows))
        self.to_check_count = sum(map(Reporter.__is_category_to_check, input_rows))
        self.not_accepted_count = sum(map(Reporter.__is_category_not_accepted, input_rows))

    def set_execution_time(self, execution_time):
        self.execution_time = execution_time

    @staticmethod
    def __is_category_not_assigned(row):
        return row.category == Category.NOT_ASSIGNED

    @staticmethod
    def __is_category_accepted(row):
        return row.category == Category.ACCEPTED

    @staticmethod
    def __is_category_not_accepted(row):
        return row.category == Category.NOT_ACCEPTED

    @staticmethod
    def __is_category_to_check(row):
        return row.category == Category.TO_CHECK

    @staticmethod
    def _get_input_rows_with_given_category(expected_category, rows):
        rows_from_this_category = []

        for row in rows:
            if row.category == expected_category:
                rows_from_this_category.append(row)

        return rows_from_this_category

    @staticmethod
    def _generate_table_data_for_input_row(expected_category, rows):
        rows_for_table_data = Reporter._get_input_rows_with_given_category(expected_category, rows)
        table_data = []

        for row in rows_for_table_data:
            table_data.append(row.get_column_values_as_list())
        return table_data


class HtmlReporter(Reporter):

    def __init__(self):
        super().__init__()
        self.__page_name = "report.html"
        self.__page_content = ""
        self.__output_directory = "output_report"
        self.__output_file_path = "{}/{}"

    def create_report_page(self):
        page_path = self.__output_file_path.format(self.__output_directory, self.__page_name)

        with open(page_path, 'w') as report_page:
            print(self.__build_page_content(), file=report_page)

    def __build_page_content(self):
        self.__page_content += HtmlPageBuilder.PAGE_HEADER
        self.__page_content += HtmlPageBuilder.add_page_element('h1', 'text-center', 1, "Category Assignment Results :")
        self.__build_jumbotron()
        self.__build_category_table("Category 0", InputRow.COLUMN_NAMES,
                                    self._generate_table_data_for_input_row(Category.NOT_ASSIGNED, self.input_rows))
        self.__build_category_table("Category 1", InputRow.COLUMN_NAMES,
                                    self._generate_table_data_for_input_row(Category.ACCEPTED, self.input_rows))
        self.__build_category_table("Category 2", InputRow.COLUMN_NAMES,
                                    self._generate_table_data_for_input_row(Category.TO_CHECK, self.input_rows))
        self.__build_category_table("Category 3", InputRow.COLUMN_NAMES,
                                    self._generate_table_data_for_input_row(Category.NOT_ACCEPTED, self.input_rows))
        self.__build_detailed_data_about_rows_which_need_to_be_checked()
        self.__page_content += HtmlPageBuilder.PAGE_FOOTER
        return self.__page_content

    def __build_jumbotron(self):
        self.__page_content += HtmlPageBuilder.open_tag('div', 'jumbotron', 1)
        self.__page_content += HtmlPageBuilder.add_page_element('p', 'text-center', 3, "Category 0 (not assigned) : {}"
                                                                .format(self.not_assigned_count))
        self.__page_content += HtmlPageBuilder.add_page_element('p', 'text-center', 3, "Category 1 (accepted) : {}"
                                                                .format(self.accepted_count))
        self.__page_content += HtmlPageBuilder.add_page_element('p', 'text-center', 3, "Category 2 (to check) : {}"
                                                                .format(self.to_check_count))
        self.__page_content += HtmlPageBuilder.add_page_element('p', 'text-center', 3, "Category 3 (not accepted) : {}"
                                                                .format(self.not_accepted_count))
        self.__page_content += HtmlPageBuilder.add_page_element('p', 'text-center', 3, "Execution time : {:.10f} s"
                                                                .format(self.execution_time))
        self.__page_content += HtmlPageBuilder.close_tag('div', 2)

    def __build_category_table(self, category_name, table_headers, table_data):
        self.__page_content += HtmlPageBuilder.add_page_element('h2', 'text-center', 2, category_name)
        self.__page_content += HtmlPageBuilder.open_tag('div', 'row', 2)
        self.__page_content += HtmlPageBuilder.open_tag('div', 'col-xs-12', 3)
        self.__page_content += HtmlPageBuilder.build_table(table_headers, table_data, 4)
        self.__page_content += HtmlPageBuilder.close_tag('div', 3)
        self.__page_content += HtmlPageBuilder.close_tag('div', 2)

    def __build_detailed_data_about_rows_which_need_to_be_checked(self):
        self.__page_content += HtmlPageBuilder.add_page_element('h2', 'text-center', 2, 'Details about entities in category 2')

        for row in self._get_input_rows_with_given_category(Category.TO_CHECK, self.input_rows):
            self.__build_detailed_data_about_one_row_and_its_collections(row)

    def __build_detailed_data_about_one_row_and_its_collections(self, input_row):

        # nie dziala - self.__page_content += HtmlPageBuilder.add_button(css_class='btn btn-info', data_toggle='collapse', data_target='#demo', text='button')
        self.__page_content += HtmlPageBuilder.add_page_element('h3', 'demo', 'text-left', 2, 'Entity: {} NIP: {}'.format(input_row.name, input_row.nip))

        #if input_row.has_any_engagements():
        self.__build_category_table('Engagements : ', Engagement.COLUMN_NAMES,
                                        input_row.get_engagements_column_values())

        #if input_row.has_any_proposals():
        self.__build_category_table('Proposals : ', Proposal.COLUMN_NAMES,
                                        input_row.get_proposals_column_values())

        #if input_row.has_any_bdas():
        self.__build_category_table('BDA : ', BusinessDevelopmentActivities.COLUMN_NAMES,
                                        input_row.get_bda_column_values())

        self.__build_category_table('Campaigns : ', Campaign.COLUMN_NAMES,
                                    input_row.get_campaign_column_values())

