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
    COMMENT ON TABLE bitrix.{Config.table_deal_create}
        IS 'Таблица с сделками выгрузенные по дате создания';
        
        COMMENT ON COLUMN bitrix.{Config.table_deal_create}.deal_id
        IS 'ID сделки';
        
        COMMENT ON COLUMN bitrix.{Config.table_deal_create}.contact_id
        IS 'Тип события (ID клиента) ';
        
        COMMENT ON COLUMN bitrix.{Config.table_deal_create}.stage_id
        IS 'ID Стадии на которой находится сделка';
        
        COMMENT ON COLUMN bitrix.{Config.table_deal_create}.close_date
        IS 'Дата закрытия (Системное поле от Битрикса)';
        
        COMMENT ON COLUMN bitrix.{Config.table_deal_create}.date_create
        IS 'Дата создания';
        
        COMMENT ON COLUMN bitrix.{Config.table_deal_create}.date_modify
        IS 'Дата последнего изменения';
        
        COMMENT ON COLUMN bitrix.{Config.table_deal_create}.category_id
        IS 'ID воронки в которой находится сделка';
        
        COMMENT ON COLUMN bitrix.{Config.table_deal_create}.source_id
        IS 'ID источника сделки';
        
        COMMENT ON COLUMN bitrix.{Config.table_deal_create}.semantic_id
        IS 'ID показывающая этап делки. # S=successful,
                            # P=production, F=fatal';
    
        COMMENT ON COLUMN bitrix.{Config.table_deal_create}.created_by_id
        IS 'ID сотрудника создавшего сделку';
        
        COMMENT ON COLUMN bitrix.{Config.table_deal_create}.blank_url
        IS 'Бланк покупателя в формате ссылки';
        
        COMMENT ON COLUMN bitrix.{Config.table_deal_create}.department_id
        IS 'Департамент к которому относится сделка';
        
    """

    with db_client.cursor() as cur:
        cur.execute(sql_script)

    db_client.commit()


def table_for_deals_by_date_modify():
    sql_script = f"""
        CREATE SCHEMA IF NOT EXISTS bitrix;

        CREATE TABLE IF NOT EXISTS bitrix.{Config.table_deal_modify} (
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
        COMMENT ON TABLE bitrix.{Config.table_deal_modify}
        IS 'Таблица с сделками выгрузенные по дате изменения';
        
        COMMENT ON COLUMN bitrix.{Config.table_deal_modify}.deal_id
        IS 'ID сделки';
        
        COMMENT ON COLUMN bitrix.{Config.table_deal_modify}.contact_id
        IS 'Тип события (ID клиента) ';
        
        COMMENT ON COLUMN bitrix.{Config.table_deal_modify}.stage_id
        IS 'ID Стадии на которой находится сделка';
        
        COMMENT ON COLUMN bitrix.{Config.table_deal_modify}.close_date
        IS 'Дата закрытия (Системное поле от Битрикса)';
        
        COMMENT ON COLUMN bitrix.{Config.table_deal_modify}.date_create
        IS 'Дата создания';
        
        COMMENT ON COLUMN bitrix.{Config.table_deal_modify}.date_modify
        IS 'Дата последнего изменения';
        
        COMMENT ON COLUMN bitrix.{Config.table_deal_modify}.category_id
        IS 'ID воронки в которой находится сделка';
        
        COMMENT ON COLUMN bitrix.{Config.table_deal_modify}.source_id
        IS 'ID источника сделки';
        
        COMMENT ON COLUMN bitrix.{Config.table_deal_modify}.semantic_id
        IS 'ID показывающая этап делки. # S=successful,
                            # P=production, F=fatal';
    
        COMMENT ON COLUMN bitrix.{Config.table_deal_modify}.created_by_id
        IS 'ID сотрудника создавшего сделку';
        
        COMMENT ON COLUMN bitrix.{Config.table_deal_modify}.blank_url
        IS 'Бланк покупателя в формате ссылки';
        
        COMMENT ON COLUMN bitrix.{Config.table_deal_modify}.department_id
        IS 'Департамент к которому относится сделка';
        
        """

    with db_client.cursor() as cur:
        cur.execute(sql_script)

    db_client.commit()


def table_for_stage_history_by_deal():
    query = f"""
        CREATE SCHEMA IF NOT EXISTS bitrix;

        CREATE TABLE IF NOT EXISTS bitrix.{Config.table_deal_history} (
            id_event    BIGINT,
            type_id     BIGINT,
            deal_id     BIGINT NOT NULL,
            date_modify TIMESTAMPTZ,
            date        DATE,
            category_id INTEGER,
            stage_id    TEXT NOT NULL,

            CONSTRAINT uq_deal_stage UNIQUE (deal_id, stage_id)
        );
        COMMENT ON TABLE bitrix.{Config.table_deal_history}
        IS 'Таблица с историей передвижения сделки по стадиям';
        
        COMMENT ON COLUMN bitrix.{Config.table_deal_history}.id_event
        IS 'Id события';
        
        COMMENT ON COLUMN bitrix.{Config.table_deal_history}.type_id
        IS 'Тип события (создание элемента, перевод на стадию, 
        финальная стадия, смена воронки) ';
        
        COMMENT ON COLUMN bitrix.{Config.table_deal_history}.deal_id
        IS 'ID сделки';
        
        COMMENT ON COLUMN bitrix.{Config.table_deal_history}.date_modify
        IS 'Дата изменения';
        
        COMMENT ON COLUMN bitrix.{Config.table_deal_history}.date
        IS 'Дата изменения без UTC';
        
        COMMENT ON COLUMN bitrix.{Config.table_deal_history}.category_id
        IS 'Воронка к которой привязана стадия';
        
        COMMENT ON COLUMN bitrix.{Config.table_deal_history}.stage_id
        IS 'ID стадии из битрикса';
    """

    with db_client.cursor() as cur:
        cur.execute(query)

    db_client.commit()


def table_for_department():
    query = f"""
    CREATE SCHEMA IF NOT EXISTS bitrix;

    CREATE TABLE IF NOT EXISTS bitrix.{Config.table_department} (
    id_dep     BIGINT PRIMARY KEY,
    name_dep   TEXT NOT NULL,
    sort       BIGINT,
    parent     BIGINT,
    uf_head    BIGINT);
    
    COMMENT ON TABLE bitrix.{Config.table_department}
    IS 'Таблица с департаментами из Битрикса';
    
    COMMENT ON COLUMN bitrix.{Config.table_department}.id_dep
    IS 'Id департамента';
    
    COMMENT ON COLUMN bitrix.{Config.table_department}.name_dep
    IS 'Название департамента';
    
    COMMENT ON COLUMN bitrix.{Config.table_department}.sort
    IS 'Порядок сортировки в Битриксе';
    
    COMMENT ON COLUMN bitrix.{Config.table_department}.parent
    IS 'Родитель департамента';
    
    COMMENT ON COLUMN bitrix.{Config.table_department}.uf_head
    IS 'ID Руководителя департамента';

    """
    with db_client.cursor() as cur:
        cur.execute(query)

    db_client.commit()

def table_for_user():
    query = f"""
     CREATE SCHEMA IF NOT EXISTS bitrix;
     
     CREATE TABLE IF NOT EXISTS bitrix.{Config.table_user}(
        user_id        BIGINT PRIMARY KEY,
        xml_id         TEXT,
        active         Integer,
        name           TEXT,
        last_name      TEXT,
        second_name    TEXT,
        email          TEXT,
        last_login     DATE,
        work_position  TEXT,
        department     BIGINT,
        code_1cka      TEXT,
        per_mobile     TEXT,
        work_mobile    TEXT,
        city           TEXT,
        phone_inner    TEXT);
        
        COMMENT ON TABLE bitrix.{Config.table_user}
        IS 'Таблица c сотрудниками из Битрикса';
        
        COMMENT ON COLUMN bitrix.{Config.table_user}.user_id
        IS 'Id пользователя';
        
        COMMENT ON COLUMN bitrix.{Config.table_user}.xml_id
        IS 'Внутренее ID';
        
        COMMENT ON COLUMN bitrix.{Config.table_user}.active
        IS 'Активный сотрудник или уволен';
        
        COMMENT ON COLUMN bitrix.{Config.table_user}.name
        IS 'Имя сотрудника';
        
        COMMENT ON COLUMN bitrix.{Config.table_user}.last_name
        IS 'Фамилия сотрудника';
        
        COMMENT ON COLUMN bitrix.{Config.table_user}.second_name
        IS 'Отчество сотрудника';
        
        COMMENT ON COLUMN bitrix.{Config.table_user}.email
        IS 'Электронная почта сотрудника';
        
        COMMENT ON COLUMN bitrix.{Config.table_user}.last_login
        IS 'Дата последнего входа';
        
        COMMENT ON COLUMN bitrix.{Config.table_user}.work_position
        IS 'Должность';
        
        COMMENT ON COLUMN bitrix.{Config.table_user}.department
        IS 'ID департамента к которому привязан сотрудник ';
        
        COMMENT ON COLUMN bitrix.{Config.table_user}.code_1cka
        IS 'Код сотрудника в 1СКА (не точные даныне)';
        
        COMMENT ON COLUMN bitrix.{Config.table_user}.per_mobile
        IS 'Персональный номер телефона';
        
        COMMENT ON COLUMN bitrix.{Config.table_user}.work_mobile
        IS 'Рабочий номер телефона';
        
        COMMENT ON COLUMN bitrix.{Config.table_user}.city
        IS 'Город сотрудника';
        
        COMMENT ON COLUMN bitrix.{Config.table_user}.phone_inner
        IS 'Не известные данные';
    """
    with db_client.cursor() as cur:
        cur.execute(query)

    db_client.commit()


def table_for_category():
    query = f"""
     CREATE SCHEMA IF NOT EXISTS bitrix;
     
     CREATE TABLE IF NOT EXISTS bitrix.{Config.table_category}(
            id BIGINT PRIMARY KEY,
            name TEXT ,
            sort INTEGER,
            entityTypeId INTEGER,
            isDefault TEXT,
            originId TEXT,
            originatorId TEXT);
            
        COMMENT ON TABLE bitrix.{Config.table_category}
        IS 'Таблица c воронками из Битрикса';
        
        COMMENT ON COLUMN bitrix.{Config.table_category}.id
        IS 'Id  Воронки';
        
        COMMENT ON COLUMN bitrix.{Config.table_category}.sort
        IS 'Сортировка';
        
        COMMENT ON COLUMN bitrix.{Config.table_category}.entityTypeId
        IS 'Показать что воронка для сделок';
        
        COMMENT ON COLUMN bitrix.{Config.table_category}.isDefault
        IS 'Является ли воронка по молчанию в Битриксе (Розница)';
        
        COMMENT ON COLUMN bitrix.{Config.table_category}.originId
        IS 'Источник воронки (Заполняется если воронка создавалась сервисами)';
        
        COMMENT ON COLUMN bitrix.{Config.table_category}.originatorId
        IS 'Создатель воронки (Заполняется если воронка создавалась сервисами)';
"""


    with db_client.cursor() as cur:
        cur.execute(query)

    db_client.commit()

def table_for_category_stage():
    query = f"""
    CREATE SCHEMA IF NOT EXISTS bitrix;
     
     CREATE TABLE IF NOT EXISTS bitrix.{Config.table_category_stage}(
        id BIGINT PRIMARY KEY,
        entity_id TEXT,
        status_id TEXT,
        name TEXT,
        name_init TEXT,
        sort INTEGER, 
        system TEXT,
        category_id TEXT DEFAULT 0);
        
        COMMENT ON TABLE bitrix.{Config.table_category_stage}
        IS 'Таблица c стадиями воронок';
        
        COMMENT ON COLUMN bitrix.{Config.table_category_stage}.id
        IS 'Id стадии внури битрикса';
        
        COMMENT ON COLUMN bitrix.{Config.table_category_stage}.entity_id
        IS 'Id сущности к которой привязана стадия (Воронка со сделками)';
        
        COMMENT ON COLUMN bitrix.{Config.table_category_stage}.status_id
        IS 'Id  статуса стадии внутри битрикса';
        
        COMMENT ON COLUMN bitrix.{Config.table_category_stage}.name
        IS 'Название стадии';
        
        COMMENT ON COLUMN bitrix.{Config.table_category_stage}.name_init
        IS 'Инициализация названия стадии в Битриксе';
        
        COMMENT ON COLUMN bitrix.{Config.table_category_stage}.sort
        IS 'ID сортировки в Битриксе';
        
        COMMENT ON COLUMN bitrix.{Config.table_category_stage}.system
        IS 'Признак системной стадии';
        
        COMMENT ON COLUMN bitrix.{Config.table_category_stage}.category_id
        IS 'ID воронки к которой привязана стадия';
    """
    with db_client.cursor() as cur:
        cur.execute(query)

    db_client.commit()