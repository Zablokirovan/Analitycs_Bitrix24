"""
This file need for upload data in database Postgres
"""
import logging
import os

import psycopg2
from dotenv import load_dotenv

import Config
import DB_table
import tg_bot

load_dotenv()

logger = logging.getLogger(__name__)

db_client = psycopg2.connect(
    dbname=os.getenv('DB_NAME'),
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    port=os.getenv("DB_PORT"),
)

DB_table.init_schema(db_client)

_DEAL_COLUMNS = """(
    deal_id, contact_id, stage_id, close_date, date_create,
    date_modify, category_id, source_id, semantic_id, created_by_id,
    blank_url, department_id, assigned_by_id, ai_sulu
)"""

_DEAL_UPSERT = f"""
    INSERT INTO {{schema}}.{{table}} {_DEAL_COLUMNS}
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    ON CONFLICT (deal_id) DO UPDATE SET
        contact_id     = EXCLUDED.contact_id,
        stage_id       = EXCLUDED.stage_id,
        close_date     = EXCLUDED.close_date,
        date_create    = EXCLUDED.date_create,
        date_modify    = EXCLUDED.date_modify,
        category_id    = EXCLUDED.category_id,
        source_id      = EXCLUDED.source_id,
        semantic_id    = EXCLUDED.semantic_id,
        created_by_id  = EXCLUDED.created_by_id,
        blank_url      = EXCLUDED.blank_url,
        department_id  = EXCLUDED.department_id,
        assigned_by_id = EXCLUDED.assigned_by_id,
        ai_sulu        = EXCLUDED.ai_sulu;
"""


def _upsert_deals(table: str, deal_list: list) -> None:
    """Shared UPSERT logic for both deal tables."""
    query = _DEAL_UPSERT.format(schema=Config.shema, table=table)
    try:
        with db_client.cursor() as cur:
            cur.executemany(query, deal_list)
        db_client.commit()
        logger.info("Upserted %d deals into %s.%s", len(deal_list), Config.shema, table)
    except Exception as e:
        db_client.rollback()
        tg_bot.telegram_send_messages(f"ERROR:_upsert_deals({table}) {e}")
        raise


def upload_db_deals_create(deal_list: list) -> None:
    """Loading transaction data exported by creation date into the database."""
    DB_table.table_for_deals_by_date_created(db_client)
    _upsert_deals(Config.table_deal_create, deal_list)


def upload_db_deals_modify(deal_list: list) -> None:
    """Load deal data into the database using deal modification date (UPSERT)."""
    DB_table.table_for_deals_by_date_modify(db_client)
    _upsert_deals(Config.table_deal_modify, deal_list)


def upload_db_deals_history(history: list) -> None:
    """Loading transaction history data into the database."""
    DB_table.table_for_stage_history_by_deal(db_client)
    query = f"""
        INSERT INTO {Config.shema}.{Config.table_deal_history} (
            id_event, type_id, deal_id, date_modify, date, category_id, stage_id
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (deal_id, stage_id) DO NOTHING;
    """
    try:
        with db_client.cursor() as cur:
            cur.executemany(query, history)
        db_client.commit()
        logger.info("Inserted %d history records.", len(history))
    except Exception as e:
        db_client.rollback()
        tg_bot.telegram_send_messages(f"ERROR:upload_db_deals_history {e}")
        raise


def department_upload(department_list: list) -> None:
    """Loading data about departments into the database."""
    DB_table.table_for_department(db_client)
    query = f"""
        INSERT INTO {Config.shema}.{Config.table_department} (
            id_dep, name_dep, sort, parent, uf_head
        )
        VALUES (%s, %s, %s, %s, %s)
        ON CONFLICT (id_dep) DO UPDATE SET
            name_dep = EXCLUDED.name_dep,
            sort     = EXCLUDED.sort,
            parent   = EXCLUDED.parent,
            uf_head  = EXCLUDED.uf_head;
    """
    try:
        with db_client.cursor() as cur:
            cur.executemany(query, department_list)
        db_client.commit()
        logger.info("Upserted %d departments.", len(department_list))
    except Exception as e:
        db_client.rollback()
        tg_bot.telegram_send_messages(f"ERROR:department_upload {e}")
        raise


def users_upload(users_list: list) -> None:
    """Loading user data into the database."""
    DB_table.table_for_user(db_client)
    query = f"""
        INSERT INTO {Config.shema}.{Config.table_user} (
            user_id, xml_id, active, name, last_name, second_name,
            email, last_login, work_position, department, code_1cka,
            per_mobile, work_mobile, city, phone_inner
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (user_id) DO UPDATE SET
            xml_id        = EXCLUDED.xml_id,
            active        = EXCLUDED.active,
            name          = EXCLUDED.name,
            last_name     = EXCLUDED.last_name,
            second_name   = EXCLUDED.second_name,
            email         = EXCLUDED.email,
            last_login    = EXCLUDED.last_login,
            work_position = EXCLUDED.work_position,
            department    = EXCLUDED.department,
            code_1cka     = EXCLUDED.code_1cka,
            per_mobile    = EXCLUDED.per_mobile,
            work_mobile   = EXCLUDED.work_mobile,
            city          = EXCLUDED.city,
            phone_inner   = EXCLUDED.phone_inner;
    """
    try:
        with db_client.cursor() as cur:
            cur.executemany(query, users_list)
        db_client.commit()
        logger.info("Upserted %d users.", len(users_list))
    except Exception as e:
        db_client.rollback()
        tg_bot.telegram_send_messages(f"ERROR:users_upload {e}")
        raise


def category_upload(category_list: list) -> None:
    """Loading funnel (category) data into the database."""
    DB_table.table_for_category(db_client)
    query = f"""
        INSERT INTO {Config.shema}.{Config.table_category} (
            id, name, sort, entityTypeId, isDefault, originId, originatorId
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (id) DO UPDATE SET
            name         = EXCLUDED.name,
            sort         = EXCLUDED.sort,
            entityTypeId = EXCLUDED.entityTypeId,
            isDefault    = EXCLUDED.isDefault,
            originId     = EXCLUDED.originId,
            originatorId = EXCLUDED.originatorId;
    """
    try:
        with db_client.cursor() as cur:
            cur.executemany(query, category_list)
        db_client.commit()
        logger.info("Upserted %d categories.", len(category_list))
    except Exception as e:
        db_client.rollback()
        tg_bot.telegram_send_messages(f"ERROR:category_upload {e}")
        raise


def stage_category_upload(stage_list: list) -> None:
    """Loading stage data into the database."""
    DB_table.table_for_category_stage(db_client)
    query = f"""
        INSERT INTO {Config.shema}.{Config.table_category_stage} (
            id, entity_id, status_id, name, name_init, sort, system, category_id
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (id) DO UPDATE SET
            entity_id   = EXCLUDED.entity_id,
            status_id   = EXCLUDED.status_id,
            name        = EXCLUDED.name,
            name_init   = EXCLUDED.name_init,
            sort        = EXCLUDED.sort,
            system      = EXCLUDED.system,
            category_id = EXCLUDED.category_id;
    """
    try:
        with db_client.cursor() as cur:
            cur.executemany(query, stage_list)
        db_client.commit()
        logger.info("Upserted %d stages.", len(stage_list))
    except Exception as e:
        db_client.rollback()
        tg_bot.telegram_send_messages(f"ERROR:stage_category_upload {e}")
        raise


def source_upload(source: list) -> None:
    """Loading source data into the database."""
    DB_table.table_for_source(db_client)
    query = f"""
        INSERT INTO {Config.shema}.{Config.table_source} (
            id, entity_id, status_id, name, name_init, sort, category_id
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (id) DO UPDATE SET
            entity_id   = EXCLUDED.entity_id,
            status_id   = EXCLUDED.status_id,
            name        = EXCLUDED.name,
            name_init   = EXCLUDED.name_init,
            sort        = EXCLUDED.sort,
            category_id = EXCLUDED.category_id;
    """
    try:
        with db_client.cursor() as cur:
            cur.executemany(query, source)
        db_client.commit()
        logger.info("Upserted %d sources.", len(source))
    except Exception as e:
        db_client.rollback()
        tg_bot.telegram_send_messages(f"ERROR:source_upload {e}")
        raise
