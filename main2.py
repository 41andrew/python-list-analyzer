from analyzer.data_loader.postgres_data_loader import PostGreDataLoader


if __name__ == "__main__":

    data_loader = PostGreDataLoader()


    # Loading data from csv files
    data_loader.load_data()