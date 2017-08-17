from data_loader.data_loader import DataLoader

# Check if this is a main thread
if __name__ == "__main__":
    data_loader = DataLoader()
    data_loader.read_calculations_targets_from_source()

    # Display source objects
    for v in data_loader.calculations_target:
        print(data_loader.calculations_target.get(v))

    data_loader.read_engagements_from_file()

    # Display engagements objects
    for v in data_loader.calculations_target:
        print(str(data_loader.calculations_target.get(v).engagements))
