import psycopg2
import os
import sys

db_dir = f"{os.path.realpath(__file__)[:-14]}\\..\\..\\..\\DB_Schema"
db_schema = open(db_dir + "\\WMGTSS_QA_SCHEMA.sql", 'r')
db_test_schema = open(db_dir + "\\WMGTSS_QA_SCHEMA_TEST.sql", 'r')

try:
    print(f"Found schema for: {db_schema.name} and {db_test_schema.name}")

    conn = psycopg2.connect(f"dbname=WMGTSS_QA user={sys.argv[1]} password={sys.argv[2]}")

    cur = conn.cursor()

    query = "".join(db_schema.readlines())

    cur.execute(query)

    conn.commit()
except Exception as e:
    print(e)

try:
    print("WMGTSS_QA created")

    conn = psycopg2.connect(f"dbname=WMGTSS_QA_TEST user={sys.argv[1]} password={sys.argv[2]}")

    cur = conn.cursor()

    query = "".join(db_test_schema.readlines())

    cur.execute(query)

    conn.commit()

    print("WMGTSS_QA_TEST created")
except Exception as e:
    print(e)

db_schema.close()
db_test_schema.close()