"""
This file is needed to create tables
if they were not found during the check.
"""

import os
import psycopg2
import Config

from dotenv import load_dotenv

load_dotenv()

#Client on Postgres
db_client = psycopg2.connect(
    dbname=os.getenv('DB_NAME'),
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    port=os.getenv("DB_PORT")
)

# existence check
def table_for_deals_by_date_created():
    """
    Create table if it does not exist
    """
    sql_script = f"""
    CREATE SCHEMA IF NOT EXISTS bitrix;

    CREATE TABLE IF NOT EXISTS bitrix.{Config.table_deal_create} (
        deal_id BIGINT PRIMARY KEY,
        contact_id BIGINT,
        stage_id TEXT,
        close_date DATE,
        date_create DATE,
        date_modify DATE,
        category_id INTEGER,
        source_id TEXT,
        semantic_id TEXT,
        created_by_id BIGINT,
        blank_url TEXT,
        department_id BIGINT
    );
    """

    with db_client.cursor() as cur:
        cur.execute(sql_script)

    db_client.commit()
