"""
This file need for upload data in database Clickhouse
"""
import os
import clickhouse_connect
from dotenv import load_dotenv

load_dotenv()

client = clickhouse_connect.get_client(
    host=os.getenv('DB_HOST'),
    database=os.getenv('DB_DATABASE'),
    username=os.getenv('DB_USERNAME'),
    password=os.getenv('DB_PASSWORD'),
    port=int(os.getenv('DB_PORT')),
    #connect in https, not http
    secure=True,
    #Disables server SSL certificate verification.
    verify=False
)


def upload_db_deals_create(deal_list):
    """
    Loading transaction data exported by creation date into the database
    :param deal_list: List
    :return: none
    """
    table = 'bitrix.deals_created'
    columns=['deal_id', 'contact_id','stage_id', 'close_date', 'date_create',
             'date_modify', 'category_id', 'source_id', 'semantic_id',
             'created_by_id', 'blank_url', 'department_id' ]
    client.insert(table=table, column_names=columns, data=deal_list)


def upload_db_deals_modify(deal_list):
    """
    Loading transaction data exported by creation date into the database
    :param deal_list: List
    :return: none
    """
    table = 'bitrix.deals_modify'
    columns=['deal_id', 'contact_id','stage_id', 'close_date', 'date_create',
             'date_modify', 'category_id', 'source_id', 'semantic_id',
             'created_by_id', 'blank_url', 'department_id', 'version' ]
    client.insert(table=table, column_names=columns, data=deal_list)


def upload_db_deals_history(history):
    """

    :param history:
    :return:
    """
    table = 'bitrix.deal_history_stage'
    columns = [
        'id_event', 'type_id', 'deal_id', 'date_modify', 'date', 'category_id',
        'stage_id']
    client.insert(table=table, column_names=columns, data=history)


def department_upload(department_list):
    """

    :param department_list:
    :return:
    """
    table = 'bitrix.department_bitrix'
    columns = ['id_dep', 'name_dep', 'sort', 'parent', 'uf_head']
    client.insert(table=table, column_names=columns, data=department_list)