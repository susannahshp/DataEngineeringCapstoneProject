import configparser


# CONFIG
config = configparser.ConfigParser()
config.read('aws.cfg')

# DROP TABLES
fact_table_drop = "DROP TABLE IF EXISTS fact_table;"
dim_state_table_drop = "DROP TABLE IF EXISTS dim_state_table;"
dim_visa_table_drop = "DROP TABLE IF EXISTS dim_visa_table;"
dim_foreign_table_drop = "DROP TABLE IF EXISTS dim_foreign_table;"


# CREATE TABLES
fact_table_create= ("""
    CREATE TABLE IF NOT EXISTS fact_table (
        fact_id BIGINT,
        state_code VARCHAR(256),
        immigration_count INTEGER,
        white INTEGER,
        asian INTEGER,
        black INTEGER,
        hispanic INTEGER,
        indian INTEGER
    );
""")

dim_state_table_create = ("""
    CREATE TABLE IF NOT EXISTS dim_state_table (
       state_code VARCHAR(256),
       state VARCHAR(256)
    );
""")

dim_visa_table_create = ("""
    CREATE TABLE IF NOT EXISTS dim_visa_table (
        state_code VARCHAR(256),
        B1 INTEGER,
        B2 INTEGER,
        CP INTEGER,
        CPL INTEGER,
        E1 INTEGER,
        E2 INTEGER,
        F1 INTEGER,
        F2 INTEGER,
        GMT INTEGER,
        I INTEGER,
        I1 INTEGER,
        M1 INTEGER,
        M2 INTEGER,
        SBP INTEGER,
        WB INTEGER,
        WT INTEGER
    );
""")

dim_foreign_table_create = ("""
    CREATE TABLE IF NOT EXISTS dim_foreign_table (
        state_code VARCHAR(256),
        state_foreign_born INTEGER
    );
""")


# QUERY LISTS

create_table_queries = [fact_table_create, dim_state_table_create, dim_visa_table_create, dim_foreign_table_create]

drop_table_queries = [fact_table_drop, dim_state_table_drop, dim_visa_table_drop, dim_foreign_table_drop]
