from data_loader.data_loader import CsvDataLoader

# Check if this is a main thread
if __name__ == "__main__":
    data_loader = CsvDataLoader()
    data_loader.load_data()

    # Test if data is loaded
    for nip in data_loader.input_entities:
        print(data_loader.input_entities[nip])
        print(data_loader.input_entities[nip].assign_category())
        print("Engagements : ")
        for engagement in data_loader.input_entities[nip].engagements:
            print("\t{}".format(engagement))
        print("Proposals : ")
        for proposal in data_loader.input_entities[nip].proposals:
            print("\t{}".format(proposal))
        print("bda : ")
        for bda in data_loader.input_entities[nip].bda:
            print("\t{}".format(bda))
        print("=" * 150)
