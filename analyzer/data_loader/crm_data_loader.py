import pyodbc

class CrmDataLoader:

    try:
        conn = pyodbc.connect(r'DRIVER={SQL Server};SERVER=plwawdb20,1113;DATABASE=MARS4_API;Trusted_Connection=yes;')
    except:
        print ("Unable to connect to the database")

    cursor = conn.cursor()

