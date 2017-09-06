from analyzer.data_loader.postgres_data_loader import PostGreDataLoader
from analyzer.data_loader.crm_data_loader import CrmDataLoader
from analyzer.calculations.strategy import EngagementStrategy
from analyzer.calculations.strategy import InputRowsCategoryAssignmentContext
from analyzer.data_loader.data_loader import CsvDataLoader
from analyzer.data_writer.data_writer import CsvDataWriter
from analyzer.utilities.properties_reader import PropertiesReader
from analyzer.calculations.strategy import RestrictedServicesStrategy
from analyzer.calculations.strategy import CampaignStrategy


if __name__ == "__main__":

    data_writer = CsvDataWriter()
    # Opening connection to CRM
    crm_loader = CrmDataLoader()
    # Opening connection to postgres database
    pgs_loader = PostGreDataLoader()


    context = InputRowsCategoryAssignmentContext()
    strategy = CampaignStrategy()


    # Loading data from CRM
    crm_loader.load_data_from_crm2()
    # Loading data from postgres database
    pgs_loader.set_input_from_csv(crm_loader.input_from_csv)
    pgs_loader.load_data_from_pgs()

    ###############################
    # Add input from CRM to postgres
    ###############################


    # Currently used strategy
    context.strategy = strategy
    context.input_rows = crm_loader.input_from_csv

    # Assign categories
    context.run_category_assignment()

    # Write to file
    data_writer.input_rows = crm_loader.input_from_csv.values()
    data_writer.write_category_assignment_result_to_file('results.csv')

    context.reporter.engagement_year = crm_loader.engagements_date
    context.reporter.proposal_year = crm_loader.proposals_date
    context.reporter.bd_year = crm_loader.bd_date
    context.reporter.campaign_start = pgs_loader.start_date
    context.reporter.campaign_end = pgs_loader.end_date

    # Generate HTML report
    context.reporter.create_report_page()
