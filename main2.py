from analyzer.data_loader.postgres_data_loader import PostGreDataLoader
from analyzer.data_loader.crm_data_loader import CrmDataLoader
from analyzer.calculations.strategy import EngagementStrategy
from analyzer.calculations.strategy import InputRowsCategoryAssignmentContext
from analyzer.data_loader.data_loader import CsvDataLoader
from analyzer.data_writer.data_writer import CsvDataWriter
from analyzer.utilities.properties_reader import PropertiesReader


if __name__ == "__main__":

    data_writer = CsvDataWriter()
    # Opening connection to postgres database
    pgs_loader = PostGreDataLoader()
    # Opening connection to CRM
    crm_loader = CrmDataLoader()

    context = InputRowsCategoryAssignmentContext()
    strategy = EngagementStrategy()


    # Loading data from CRM
    crm_loader.load_data_from_crm2()
    # Loading data from postgres database
    pgs_loader.load_data_from_pgs()

    # Currently used strategy
    context.strategy = strategy
    context.input_rows = crm_loader.input_from_csv

    # Assign categories
    context.run_category_assignment()

    # Write to file
    data_writer.input_rows = crm_loader.input_from_csv.values()
    data_writer.write_category_assignment_result_to_file('results.csv')

    # Generate HTML report
    context.reporter.create_report_page()
