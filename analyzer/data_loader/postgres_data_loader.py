import psycopg2

class PostGreDataLoader:

    CAMPAIGN_ID_LIST = [10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28,
                        29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47,
                        48, 49, 50, 51]

    all_campaigns = []

    try:
        conn = psycopg2.connect("dbname='ContactDirect' user='master' host='10.162.2.152' password='test'")
    except Exception as e:
        print (e)

    cursor = conn.cursor()

    sql = """SELECT * FROM "Custom"."GetRecordsToExport"((%s), '2017-08-01', '2017-08-10'"""

    for x in CAMPAIGN_ID_LIST:
        cursor.execute(sql, (x))
        all_campaigns.extend(cursor.fetchall())


