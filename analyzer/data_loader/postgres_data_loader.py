import psycopg2
from ..utilities.properties_reader import PropertiesReader
from .data_loader import CsvDataLoader
from ..model.engagement import Engagement
from ..model.proposal import Proposal
from ..model.bda import BusinessDevelopmentActivities
from ..model.entity import Entity
from ..model.campaign import Campaign
import os
import tkinter as tk
from tkinter import filedialog


class PostGreDataLoader:

    CAMPAIGN_ID_LIST = [16, 17, 18, 19,
                        20, 21, 23, 24, 27, 28, 29,
                        30, 31, 33, 34, 35, 36, 37,
                        40, 41, 42, 43, 44, 46, 47,
                        48, 49, 50, 51, 52, 53, 54,
                        55]

    all_campaigns = []

    def __init__(self):
        root = tk.Tk()
        root.withdraw()
        self.props = PropertiesReader.get_properties_file_as_dict()
        # Tutaj nadpisywales input
        # self.input_from_csv = CsvDataLoader().get_input_rows_as_dict()
        self.input_from_csv = {}
        self.conn = None
        self.camapign_list_input = filedialog.askopenfilename(title='Wybierz plik kampaniami',
                                                          filetypes=(('csv files', '*.csv'),))
        self.start_date = input("Podaj datę początkową kampanii w formacie YYYY-MM-DD\n")
        self.end_date = input("Podaj datę końcową kampanii YYYY-MM-DD\n")

    def read_lines_from_campaign_file(self):
        try:
            with open(self.camapign_list_input, 'r', encoding='windows-1250', errors='ignore') as source_file:
                return source_file.readlines()
        except FileNotFoundError as e:
            print(e)
            self.error_messages.add("File {} not found".format(self.camapign_list_input))

    def create_campaign_list(self):

        for line in self.read_lines_from_campaign_file():
            PostGreDataLoader.CAMPAIGN_ID_LIST.append(line[0])

    def set_input_from_csv(self, input_from_crm):
        self.input_from_csv = input_from_crm

    def connect_to_pgsql(self):
        try:
            self.conn = psycopg2.connect("dbname='ContactDirect' user='master' host='{}' password='{}'"
                                         .format(self.props['host'], self.props['pass']))
        except Exception as e:
            print("Exception while connecting with database")
            print("Error message : {}".format(e))

    def load_data_from_pgs(self):

        self.connect_to_pgsql()

        cursor = self.conn.cursor()

        sql = """SELECT * FROM "Custom"."GetRecordsToExport"((%s), %s, %s)"""

        for x in self.CAMPAIGN_ID_LIST:
            cursor.execute(sql, (x, self.start_date, self.end_date))
            self.all_campaigns.extend(cursor.fetchall())

        for nip in self.input_from_csv:

            for campaign_row in self.all_campaigns:

                if nip == campaign_row[2]:

                    campaign = Campaign(campaign_id=campaign_row[0],
                                        campaign_name=campaign_row[1],
                                        nip=campaign_row[2],
                                        name=campaign_row[3],
                                        last_call=campaign_row[4],
                                        last_comment=[5])
                    self.input_from_csv[nip].campaigns.append(campaign)


        #print(self.all_campaigns)
