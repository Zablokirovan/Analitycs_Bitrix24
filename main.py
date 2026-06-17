import logging
import argparse

import Bitrix24
import Database
import tg_bot

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
)

logger = logging.getLogger(__name__)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('task', choices=[
        'deals_crt', 'deals_mdf',
        'user', 'category', 'source', 'department',
    ])
    args = parser.parse_args()

    handlers = {
        'deals_crt': get_and_upload_deals_create,
        'deals_mdf': get_and_upload_deal_modify,
        'user':       user,
        'category':   category,
        'source':     source,
        'department': department,
    }

    logger.info("Running task: %s", args.task)
    try:
        handlers[args.task]()
    except Exception as e:
        tg_bot.telegram_send_messages(f"FATAL: task '{args.task}' failed: {e}")
        raise


def get_and_upload_deals_create():
    deal_id_dc, deal_dc_modify_data = Bitrix24.get_deals_date_create()
    Database.upload_db_deals_create(deal_dc_modify_data)


def get_and_upload_deal_modify():
    # 1. История стадий за сегодня → уникальные ID сделок
    history, deal_ids = Bitrix24.get_history_by_date(
        Bitrix24.start_date_m, Bitrix24.end_date_m
    )
    if not deal_ids:
        logger.info("No stage transitions today — nothing to upload.")
        return

    # 2. Полные данные по этим сделкам
    _, deals = Bitrix24.get_deals_by_ids(deal_ids)

    # 3. Загрузка в БД
    Database.upload_db_deals_modify(deals)
    Database.upload_db_deals_history(history)


def department():
    dep_info = Bitrix24.get_department()
    Database.department_upload(dep_info)


def user():
    users_list = Bitrix24.user_get()
    Database.users_upload(users_list)


def category():
    category_list, category_id = Bitrix24.get_category()
    Database.category_upload(category_list)
    stage_in_category(category_id)


def stage_in_category(category_id):
    stage = Bitrix24.get_stage(category_id)
    Database.stage_category_upload(stage)


def source():
    source_list = Bitrix24.get_source()
    Database.source_upload(source_list)


if __name__ == "__main__":
    main()
