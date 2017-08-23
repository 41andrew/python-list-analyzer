from analyzer.data_loader.postgres_data_loader import PostGreDataLoader
from analyzer.data_loader.crm_data_loader import CrmDataLoader


if __name__ == "__main__":

    data_loader = PostGreDataLoader()

    data_loader2 = CrmDataLoader()


    # Loading data from csv files
    data_loader.load_data_from_pgs()

    data_loader2.load_engagements_from_crm()