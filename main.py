from analyzer.calculations.strategy import EngagementStrategy
from analyzer.calculations.strategy import InputRowsCategoryAssignmentContext
from analyzer.data_loader.data_loader import CsvDataLoader
from analyzer.data_writer.data_writer import CsvDataWriter


def print_input_record(input_record):
    print("input_record with NIP : {}".format(input_record.nip))
    print(input_record)
    
    print_elements_in_collection("Engagements", input_record.engagements)
    print_elements_in_collection("Proposals", input_record.proposals)
    print_elements_in_collection("BDA", input_record.bda)
    
    print("=" * 50)
    
    
def print_elements_in_collection(collection_name, collection):
    print("{} ({}): ".format(collection_name, len(collection)))
    
    for elem in collection:
        print("\t{}".format(elem))

# Check if this is a main thread
if __name__ == "__main__":

    data_loader = CsvDataLoader()
    data_writer = CsvDataWriter()
    context = InputRowsCategoryAssignmentContext()
    strategy = EngagementStrategy()

    # Loading data from csv files
    data_loader.load_data()

    # Currently used strategy
    context.strategy = strategy
    context.input_rows = data_loader.input_entities

    # Assign categories
    context.run_category_assignment()

    # Print loaded data with category
    for nip in data_loader.input_entities:
        print_input_record(data_loader.input_entities[nip])

    # Write to file
    data_writer.input_rows = data_loader.input_entities.values()
    data_writer.write_category_assignment_result_to_file("result.csv")

    # Generate HTML report
    context.reporter.create_report_page()
