from data_loader.data_loader import CsvDataLoader


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
    data_loader.load_data()

    # Print loaded data
    for nip in data_loader.input_entities:
        print_input_record(data_loader.input_entities[nip])

