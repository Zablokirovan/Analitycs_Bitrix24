"""
This file need for upload data in database Postgres
"""
import os
import tg_bot
import psycopg2

import Config
import DB_table

from dotenv import load_dotenv

load_dotenv()

# Postgres connect
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
    # Table name
    table = Config.table_deal_create

    # Existence check
    DB_table.table_for_deals_by_date_created()
    # Script
    query = f"""
                    INSERT INTO {Config.shema}.{table} (
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
                         ON CONFLICT (deal_id)
                         DO UPDATE SET
                            contact_id = EXCLUDED.contact_id,
                            stage_id = EXCLUDED.stage_id,
                            close_date = EXCLUDED.close_date,
                            date_create = EXCLUDED.date_create, 
                            date_modify = EXCLUDED.date_modify,
                            category_id = EXCLUDED.category_id,
                            source_id = EXCLUDED.source_id,
                            semantic_id = EXCLUDED.semantic_id,
                            created_by_id = EXCLUDED.created_by_id,
                            blank_url = EXCLUDED.blank_url,
                            department_id = EXCLUDED.department_id;
                         """

    with db_client.cursor() as cur:
        cur.executemany(query, deal_list)
    db_client.commit()


def upload_db_deals_modify(deal_list):
    """
    Load deal data into the database using deal modification date (UPSERT).
    :param deal_list: list[tuple]
    :return: None
     """
    # Table name
    table = Config.table_deal_modify

    # Existence check
    DB_table.table_for_deals_by_date_modify()
    try:
        # Script
        query = f"""
                INSERT INTO {Config.shema}.{table} (
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
                     ON CONFLICT (deal_id)
                     DO UPDATE SET
                        contact_id = EXCLUDED.contact_id,
                        stage_id = EXCLUDED.stage_id,
                        close_date = EXCLUDED.close_date,
                        date_create = EXCLUDED.date_create, 
                        date_modify = EXCLUDED.date_modify,
                        category_id = EXCLUDED.category_id,
                        source_id = EXCLUDED.source_id,
                        semantic_id = EXCLUDED.semantic_id,
                        created_by_id = EXCLUDED.created_by_id,
                        blank_url = EXCLUDED.blank_url,
                        department_id = EXCLUDED.department_id;
                     """
        with db_client.cursor() as cur:
            cur.executemany(query, deal_list)

        db_client.commit()
    except Exception as e:
        tg_bot.telegram_send_messages(f"ERROR:upload_db_deals_modify {e} ")



def upload_db_deals_history(history):
    """
    Loading transaction history data into the database
    :param history: list histories
    :return:None
    """
    # Table for history stage by deal
    table = Config.table_deal_history

    # Check exist table
    DB_table.table_for_stage_history_by_deal()
    try:
        query = f"""
           INSERT INTO {Config.shema}.{table} (
                id_event,
                type_id,
                deal_id,
                date_modify,
                date,
                category_id, 
                stage_id
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (deal_id, stage_id)
                DO NOTHING
                """
        with db_client.cursor() as  cur:
            cur.executemany(query, history)

    except Exception as e:
        tg_bot.telegram_send_messages(f"ERROR:upload_db_deals_modify {e} ")

    db_client.commit()




def department_upload(department_list):
    """
    Loading data about the transaction departments into the database
    :param department_list:
    :return:None
    """
    # Table for department
    table = Config.table_department
    # Check exist table
    DB_table.table_for_department()
    try:
        query = f"""
        INSERT INTO {Config.shema}.{table}(
                id_dep,
                name_dep,
                sort,
                parent,
                uf_head
                )
        VALUES (%s, %s, %s, %s, %s)
        ON CONFLICT (id_dep)
        DO UPDATE SET
                name_dep = EXCLUDED.name_dep,
                sort     = EXCLUDED.sort,
                parent   = EXCLUDED.parent,
                uf_head  = EXCLUDED.uf_head;"""

        with db_client.cursor() as cur:
            cur.executemany(query,department_list)

    except Exception as e:
        tg_bot.telegram_send_messages(f"ERROR:department_upload {e} ")

    db_client.commit()



def users_upload(users_list):
    """
    Loading user data into the database
    :param users_list:
    :return: None
    """
    # Table for data by user
    table = Config.table_user
    # Check exist table
    DB_table.table_for_user()
    try:
        query = f"""
            INSERT INTO {Config.shema}.{table}(
                    user_id,
                    xml_id,
                    active,
                    name,
                    last_name,
                    second_name,
                    email,
                    last_login,
                    work_position,
                    department,
                    code_1cka,
                    per_mobile,
                    work_mobile,
                    city,
                    phone_inner) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (user_id)
            DO UPDATE SET
                    xml_id = EXCLUDED.xml_id,
                    active = EXCLUDED.active,
                    name = EXCLUDED.name,
                    last_name = EXCLUDED.last_name,
                    second_name = EXCLUDED.second_name,
                    email = EXCLUDED.email,
                    last_login = EXCLUDED.last_login,
                    work_position = EXCLUDED.work_position,
                    department = EXCLUDED.department,
                    code_1cka = EXCLUDED.code_1cka,
                    per_mobile = EXCLUDED.per_mobile,
                    work_mobile = EXCLUDED.work_mobile,
                    city = EXCLUDED.city,
                    phone_inner = EXCLUDED.phone_inner;
            """
        with db_client.cursor() as cur:
            cur.executemany(query,users_list)

    except Exception as e:
        tg_bot.telegram_send_messages(f"ERROR:users_upload {e} ")

    db_client.commit()

def category_upload(category_list):
    """

    :param category_list:
    :return:
    """
    # Table for fuel information
    table = Config.table_category
    # Chek exist table
    DB_table.table_for_category()
    try:
        query = f"""
        INSERT INTO {Config.shema}.{table}(
                id,
                name,
                sort,
                entityTypeId,
                isDefault,
                originId,
                originatorId)
        
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT(id)
        
        DO UPDATE SET
                id = EXCLUDED.id,
                name = EXCLUDED.name,
                sort = EXCLUDED.sort,
                entityTypeId = EXCLUDED.entityTypeId,
                isDefault = EXCLUDED.isDefault,
                originId = EXCLUDED.originId,
                originatorId = EXCLUDED.originatorId;
            """

        with db_client.cursor() as cur:
            cur.executemany(query,category_list)

    except Exception as e:
        tg_bot.telegram_send_messages(f"ERROR:category_upload {e} ")
    db_client.commit()



def stage_category_upload(stage_list):
    """

    :param stage_list:
    :return:
    """
    # Table for stage_history by deal
    table = Config.table_category_stage
    # Chek exist table
    DB_table.table_for_category_stage()

    try:
        query = f"""
        INSERT INTO {Config.shema}.{table}(
            id,
            entity_id,
            status_id,
            name,
            name_init,
            sort, 
            system,
            category_id)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT(id)
        DO UPDATE SET
            entity_id = EXCLUDED.entity_id,
            status_id = EXCLUDED.status_id,
            name = EXCLUDED.name,
            name_init = EXCLUDED.name_init,
            sort = EXCLUDED.sort, 
            system = EXCLUDED.system,
            category_id = EXCLUDED.category_id
        """
        with db_client.cursor() as cur:
            cur.executemany(query, stage_list)

    except Exception as e:
        tg_bot.telegram_send_messages(f"ERROR:stage_category_upload {e} ")

    db_client.commit()


def source_upload(source):
    """

    :param source:
    :return:
    """
    # Table for source data
    table = Config.table_source
    # Check exist table
    DB_table.table_for_source()

    try:
        query = f"""
        INSERT INTO {Config.shema}.{table}(
                id ,
                entity_id ,
                status_id ,
                name ,
                name_init ,
                sort , 
                category_id)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT(id)
        DO UPDATE SET
            entity_id = EXCLUDED.entity_id,
            status_id = EXCLUDED.status_id,
            name = EXCLUDED.name,
            name_init = EXCLUDED.name_init,
            sort = EXCLUDED.sort,
            category_id = EXCLUDED.category_id
        """
        with db_client.cursor() as cur:
            cur.executemany(query, source)

    except Exception as e:
        tg_bot.telegram_send_messages(f"ERROR:source_upload {e} ")

    db_client.commit()