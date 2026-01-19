"""
This file need for upload data in database Clickhouse
"""
import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

db_client = psycopg2.connect(
    dbname=os.getenv('DB_NAME'),
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    port=os.getenv("DB_PORT")
)


def upload_db_deals_create(deal_list):
    """
    Loading transaction data exported by creation date into the database
    :param deal_list: List
    :return: none
    """
    with db_client.cursor() as cur:
        cur.executemany(
            f"""
            INSERT INTO {os.getenv('DB_SHEMA')}.deals_on_datecreated (
            deal_id,
            contact_id,
            stage_id,
            close_date,
            date_create, 
            date_modify,
            category_id,
            source_id,
            semantic_id,
            created_by_id,
            blank_url,
            department_id
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, deal_list
        )
        db_client.commit()

def upload_db_deals_modify(deal_list):
    """
    Loading transaction data exported by creation date into the database
    :param deal_list: List
    :return: none
    """
    table = 'bitrix.deals_modify'
    columns = ['deal_id', 'contact_id', 'stage_id', 'close_date',
               'date_create', 'date_modify', 'category_id', 'source_id',
               'semantic_id', 'created_by_id', 'blank_url',
               'department_id', 'version']
    client.insert(table=table, column_names=columns, data=deal_list)


def upload_db_deals_history(history):
    """
    Loading transaction history data into the database
    :param history: list histories
    :return:None
    """
    table = 'bitrix.deal_history_stage'
    columns = ['id_event', 'type_id', 'deal_id',
               'date_modify', 'date', 'category_id', 'stage_id']
    client.insert(table=table, column_names=columns, data=history)


def department_upload(department_list):
    """
    Loading data about the transaction departments into the database
    :param department_list:
    :return:None
    """
    table = 'bitrix.department_bitrix'
    columns = ['id_dep', 'name_dep', 'sort', 'parent', 'uf_head', 'updated_at']
    client.insert(table=table, column_names=columns, data=department_list)


def users_upload(users_list):
    """
    Loading user data into the database
    :param users_list:
    :return: None
    """
    table = 'bitrix.users_bitrix'
    columns = ['user_id', 'xml_id', 'active', 'name', 'last_name',
               'second_name', 'email', 'last_login', 'work_position',
               'department', '1cka_code', 'per_mobile', 'city',
               'work_mobile', 'phone_inner', 'updated_at']
    client.insert(table=table, column_names=columns, data=users_list)

def category_upload(category_list):
    """

    :param category_list:
    :return:
    """
    table = 'bitrix.category_bitrix'
    columns = ['id', 'name', 'sort', 'entityTypeId', 'isDefault',
               'originId', 'originatorId', 'updated_at']
    client.insert(table=table, column_names=columns, data=category_list)


def stage_category_upload(stage_list):
    table = 'bitrix.stage_category'
    columns = ['id', 'entity_id', 'status_id', 'name', 'name_init',
               'sort', 'system', 'category_id', 'updated_at']
    client.insert(table=table, column_names=columns, data=stage_list)
