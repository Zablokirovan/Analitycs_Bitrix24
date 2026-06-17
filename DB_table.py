"""
This file is needed to create tables
if they were not found during the check.
"""

import logging
import Config

logger = logging.getLogger(__name__)


def init_schema(conn):
    """Create the schema once on startup if it does not exist."""
    with conn.cursor() as cur:
        cur.execute(f"CREATE SCHEMA IF NOT EXISTS {Config.shema};")
    conn.commit()
    logger.info("Schema '%s' initialised.", Config.shema)


def table_for_deals_by_date_created(conn):
    sql_script = f"""
    CREATE TABLE IF NOT EXISTS {Config.shema}.{Config.table_deal_create} (
        deal_id        BIGINT PRIMARY KEY,
        contact_id     BIGINT,
        stage_id       TEXT,
        close_date     DATE,
        date_create    DATE,
        date_modify    DATE,
        category_id    INTEGER,
        source_id      TEXT,
        semantic_id    TEXT,
        created_by_id  BIGINT,
        blank_url      TEXT,
        department_id  BIGINT,
        assigned_by_id BIGINT,
        ai_sulu        TEXT
    );
    COMMENT ON TABLE {Config.shema}.{Config.table_deal_create}
        IS 'Таблица с сделками выгрузенные по дате создания';
    COMMENT ON COLUMN {Config.shema}.{Config.table_deal_create}.deal_id        IS 'ID сделки';
    COMMENT ON COLUMN {Config.shema}.{Config.table_deal_create}.contact_id     IS 'ID клиента';
    COMMENT ON COLUMN {Config.shema}.{Config.table_deal_create}.stage_id       IS 'ID стадии';
    COMMENT ON COLUMN {Config.shema}.{Config.table_deal_create}.close_date     IS 'Дата закрытия (системное поле)';
    COMMENT ON COLUMN {Config.shema}.{Config.table_deal_create}.date_create    IS 'Дата создания';
    COMMENT ON COLUMN {Config.shema}.{Config.table_deal_create}.date_modify    IS 'Дата последнего изменения';
    COMMENT ON COLUMN {Config.shema}.{Config.table_deal_create}.category_id    IS 'ID воронки';
    COMMENT ON COLUMN {Config.shema}.{Config.table_deal_create}.source_id      IS 'ID источника';
    COMMENT ON COLUMN {Config.shema}.{Config.table_deal_create}.semantic_id    IS 'Этап сделки: S=successful, P=production, F=fatal';
    COMMENT ON COLUMN {Config.shema}.{Config.table_deal_create}.created_by_id  IS 'ID сотрудника, создавшего сделку';
    COMMENT ON COLUMN {Config.shema}.{Config.table_deal_create}.blank_url      IS 'Бланк покупателя в формате ссылки';
    COMMENT ON COLUMN {Config.shema}.{Config.table_deal_create}.department_id  IS 'Департамент, к которому относится сделка';
    COMMENT ON COLUMN {Config.shema}.{Config.table_deal_create}.assigned_by_id IS 'Ответственный за сделку';
    COMMENT ON COLUMN {Config.shema}.{Config.table_deal_create}.ai_sulu        IS 'Сделка создана при помощи AiSulu';
    """
    with conn.cursor() as cur:
        cur.execute(sql_script)
    conn.commit()


def table_for_deals_by_date_modify(conn):
    sql_script = f"""
    CREATE TABLE IF NOT EXISTS {Config.shema}.{Config.table_deal_modify} (
        deal_id        BIGINT PRIMARY KEY,
        contact_id     BIGINT,
        stage_id       TEXT,
        close_date     DATE,
        date_create    DATE,
        date_modify    DATE,
        category_id    INTEGER,
        source_id      TEXT,
        semantic_id    TEXT,
        created_by_id  BIGINT,
        blank_url      TEXT,
        department_id  BIGINT,
        assigned_by_id BIGINT,
        ai_sulu        TEXT
    );
    COMMENT ON TABLE {Config.shema}.{Config.table_deal_modify}
        IS 'Таблица с сделками выгрузенные по дате изменения';
    COMMENT ON COLUMN {Config.shema}.{Config.table_deal_modify}.deal_id        IS 'ID сделки';
    COMMENT ON COLUMN {Config.shema}.{Config.table_deal_modify}.contact_id     IS 'ID клиента';
    COMMENT ON COLUMN {Config.shema}.{Config.table_deal_modify}.stage_id       IS 'ID стадии';
    COMMENT ON COLUMN {Config.shema}.{Config.table_deal_modify}.close_date     IS 'Дата закрытия (системное поле)';
    COMMENT ON COLUMN {Config.shema}.{Config.table_deal_modify}.date_create    IS 'Дата создания';
    COMMENT ON COLUMN {Config.shema}.{Config.table_deal_modify}.date_modify    IS 'Дата последнего изменения';
    COMMENT ON COLUMN {Config.shema}.{Config.table_deal_modify}.category_id    IS 'ID воронки';
    COMMENT ON COLUMN {Config.shema}.{Config.table_deal_modify}.source_id      IS 'ID источника';
    COMMENT ON COLUMN {Config.shema}.{Config.table_deal_modify}.semantic_id    IS 'Этап сделки: S=successful, P=production, F=fatal';
    COMMENT ON COLUMN {Config.shema}.{Config.table_deal_modify}.created_by_id  IS 'ID сотрудника, создавшего сделку';
    COMMENT ON COLUMN {Config.shema}.{Config.table_deal_modify}.blank_url      IS 'Бланк покупателя в формате ссылки';
    COMMENT ON COLUMN {Config.shema}.{Config.table_deal_modify}.department_id  IS 'Департамент, к которому относится сделка';
    COMMENT ON COLUMN {Config.shema}.{Config.table_deal_modify}.assigned_by_id IS 'Ответственный за сделку';
    COMMENT ON COLUMN {Config.shema}.{Config.table_deal_modify}.ai_sulu        IS 'Сделка создана при помощи AiSulu';
    """
    with conn.cursor() as cur:
        cur.execute(sql_script)
    conn.commit()


def table_for_stage_history_by_deal(conn):
    query = f"""
    CREATE TABLE IF NOT EXISTS {Config.shema}.{Config.table_deal_history} (
        id_event    BIGINT,
        type_id     BIGINT,
        deal_id     BIGINT NOT NULL,
        date_modify TIMESTAMPTZ,
        date        DATE,
        category_id INTEGER,
        stage_id    TEXT NOT NULL,

        CONSTRAINT uq_deal_stage UNIQUE (deal_id, stage_id)
    );
    COMMENT ON TABLE {Config.shema}.{Config.table_deal_history}
        IS 'Таблица с историей передвижения сделки по стадиям';
    COMMENT ON COLUMN {Config.shema}.{Config.table_deal_history}.id_event    IS 'Id события';
    COMMENT ON COLUMN {Config.shema}.{Config.table_deal_history}.type_id     IS 'Тип события (создание, перевод, финальная стадия, смена воронки)';
    COMMENT ON COLUMN {Config.shema}.{Config.table_deal_history}.deal_id     IS 'ID сделки';
    COMMENT ON COLUMN {Config.shema}.{Config.table_deal_history}.date_modify IS 'Дата изменения';
    COMMENT ON COLUMN {Config.shema}.{Config.table_deal_history}.date        IS 'Дата изменения без UTC';
    COMMENT ON COLUMN {Config.shema}.{Config.table_deal_history}.category_id IS 'Воронка, к которой привязана стадия';
    COMMENT ON COLUMN {Config.shema}.{Config.table_deal_history}.stage_id    IS 'ID стадии из Битрикса';
    """
    with conn.cursor() as cur:
        cur.execute(query)
    conn.commit()


def table_for_department(conn):
    query = f"""
    CREATE TABLE IF NOT EXISTS {Config.shema}.{Config.table_department} (
        id_dep   BIGINT PRIMARY KEY,
        name_dep TEXT NOT NULL,
        sort     BIGINT,
        parent   BIGINT,
        uf_head  BIGINT
    );
    COMMENT ON TABLE {Config.shema}.{Config.table_department}
        IS 'Таблица с департаментами из Битрикса';
    COMMENT ON COLUMN {Config.shema}.{Config.table_department}.id_dep   IS 'Id департамента';
    COMMENT ON COLUMN {Config.shema}.{Config.table_department}.name_dep IS 'Название департамента';
    COMMENT ON COLUMN {Config.shema}.{Config.table_department}.sort     IS 'Порядок сортировки в Битриксе';
    COMMENT ON COLUMN {Config.shema}.{Config.table_department}.parent   IS 'Родитель департамента';
    COMMENT ON COLUMN {Config.shema}.{Config.table_department}.uf_head  IS 'ID руководителя департамента';
    """
    with conn.cursor() as cur:
        cur.execute(query)
    conn.commit()


def table_for_user(conn):
    query = f"""
    CREATE TABLE IF NOT EXISTS {Config.shema}.{Config.table_user} (
        user_id       BIGINT PRIMARY KEY,
        xml_id        TEXT,
        active        INTEGER,
        name          TEXT,
        last_name     TEXT,
        second_name   TEXT,
        email         TEXT,
        last_login    DATE,
        work_position TEXT,
        department    BIGINT,
        code_1cka     TEXT,
        per_mobile    TEXT,
        work_mobile   TEXT,
        city          TEXT,
        phone_inner   TEXT
    );
    COMMENT ON TABLE {Config.shema}.{Config.table_user}
        IS 'Таблица c сотрудниками из Битрикса';
    COMMENT ON COLUMN {Config.shema}.{Config.table_user}.user_id       IS 'Id пользователя';
    COMMENT ON COLUMN {Config.shema}.{Config.table_user}.xml_id        IS 'Внутреннее ID';
    COMMENT ON COLUMN {Config.shema}.{Config.table_user}.active        IS 'Активный сотрудник или уволен';
    COMMENT ON COLUMN {Config.shema}.{Config.table_user}.name          IS 'Имя сотрудника';
    COMMENT ON COLUMN {Config.shema}.{Config.table_user}.last_name     IS 'Фамилия сотрудника';
    COMMENT ON COLUMN {Config.shema}.{Config.table_user}.second_name   IS 'Отчество сотрудника';
    COMMENT ON COLUMN {Config.shema}.{Config.table_user}.email         IS 'Электронная почта сотрудника';
    COMMENT ON COLUMN {Config.shema}.{Config.table_user}.last_login    IS 'Дата последнего входа';
    COMMENT ON COLUMN {Config.shema}.{Config.table_user}.work_position IS 'Должность';
    COMMENT ON COLUMN {Config.shema}.{Config.table_user}.department    IS 'ID департамента';
    COMMENT ON COLUMN {Config.shema}.{Config.table_user}.code_1cka     IS 'Код сотрудника в 1СКА';
    COMMENT ON COLUMN {Config.shema}.{Config.table_user}.per_mobile    IS 'Персональный номер телефона';
    COMMENT ON COLUMN {Config.shema}.{Config.table_user}.work_mobile   IS 'Рабочий номер телефона';
    COMMENT ON COLUMN {Config.shema}.{Config.table_user}.city          IS 'Город сотрудника';
    COMMENT ON COLUMN {Config.shema}.{Config.table_user}.phone_inner   IS 'Внутренний номер телефона';
    """
    with conn.cursor() as cur:
        cur.execute(query)
    conn.commit()


def table_for_category(conn):
    query = f"""
    CREATE TABLE IF NOT EXISTS {Config.shema}.{Config.table_category} (
        id           BIGINT PRIMARY KEY,
        name         TEXT,
        sort         INTEGER,
        entityTypeId INTEGER,
        isDefault    TEXT,
        originId     TEXT,
        originatorId TEXT
    );
    COMMENT ON TABLE {Config.shema}.{Config.table_category}
        IS 'Таблица c воронками из Битрикса';
    COMMENT ON COLUMN {Config.shema}.{Config.table_category}.id           IS 'Id воронки';
    COMMENT ON COLUMN {Config.shema}.{Config.table_category}.sort         IS 'Сортировка';
    COMMENT ON COLUMN {Config.shema}.{Config.table_category}.entityTypeId IS 'Признак воронки для сделок';
    COMMENT ON COLUMN {Config.shema}.{Config.table_category}.isDefault    IS 'Воронка по умолчанию (Розница)';
    COMMENT ON COLUMN {Config.shema}.{Config.table_category}.originId     IS 'Источник воронки';
    COMMENT ON COLUMN {Config.shema}.{Config.table_category}.originatorId IS 'Создатель воронки';
    """
    with conn.cursor() as cur:
        cur.execute(query)
    conn.commit()


def table_for_category_stage(conn):
    query = f"""
    CREATE TABLE IF NOT EXISTS {Config.shema}.{Config.table_category_stage} (
        id          BIGINT PRIMARY KEY,
        entity_id   TEXT,
        status_id   TEXT,
        name        TEXT,
        name_init   TEXT,
        sort        INTEGER,
        system      TEXT,
        category_id TEXT DEFAULT '0'
    );
    COMMENT ON TABLE {Config.shema}.{Config.table_category_stage}
        IS 'Таблица c стадиями воронок';
    COMMENT ON COLUMN {Config.shema}.{Config.table_category_stage}.id          IS 'Id стадии внутри Битрикса';
    COMMENT ON COLUMN {Config.shema}.{Config.table_category_stage}.entity_id   IS 'Id сущности, к которой привязана стадия';
    COMMENT ON COLUMN {Config.shema}.{Config.table_category_stage}.status_id   IS 'Id статуса стадии внутри Битрикса';
    COMMENT ON COLUMN {Config.shema}.{Config.table_category_stage}.name        IS 'Название стадии';
    COMMENT ON COLUMN {Config.shema}.{Config.table_category_stage}.name_init   IS 'Инициализация названия стадии';
    COMMENT ON COLUMN {Config.shema}.{Config.table_category_stage}.sort        IS 'Порядок сортировки';
    COMMENT ON COLUMN {Config.shema}.{Config.table_category_stage}.system      IS 'Признак системной стадии';
    COMMENT ON COLUMN {Config.shema}.{Config.table_category_stage}.category_id IS 'ID воронки, к которой привязана стадия';
    """
    with conn.cursor() as cur:
        cur.execute(query)
    conn.commit()


def table_for_source(conn):
    query = f"""
    CREATE TABLE IF NOT EXISTS {Config.shema}.{Config.table_source} (
        id          BIGINT PRIMARY KEY,
        entity_id   TEXT,
        status_id   TEXT,
        name        TEXT,
        name_init   TEXT,
        sort        INTEGER,
        category_id TEXT DEFAULT '0'
    );
    COMMENT ON TABLE {Config.shema}.{Config.table_source}
        IS 'Таблица c источниками из Битрикса';
    COMMENT ON COLUMN {Config.shema}.{Config.table_source}.id          IS 'Id источника';
    COMMENT ON COLUMN {Config.shema}.{Config.table_source}.entity_id   IS 'Тип сущности';
    COMMENT ON COLUMN {Config.shema}.{Config.table_source}.status_id   IS 'Статус сущности';
    COMMENT ON COLUMN {Config.shema}.{Config.table_source}.name        IS 'Название источника';
    COMMENT ON COLUMN {Config.shema}.{Config.table_source}.name_init   IS 'Инициализация названия источника';
    COMMENT ON COLUMN {Config.shema}.{Config.table_source}.sort        IS 'Порядок сортировки';
    COMMENT ON COLUMN {Config.shema}.{Config.table_source}.category_id IS 'ID воронки, к которой привязан источник';
    """
    with conn.cursor() as cur:
        cur.execute(query)
    conn.commit()
