import Bitrix24
import Database
import tg_bot

import argparse


def main():
    """

    :return:
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('task', choices=['deals_crt', 'deals_mdf',
                                         'user', 'category','source',
                                         'department'])

    args = parser.parse_args()

    if args.task == 'deals_crt':
        get_and_upload_deals_create()

    elif args.task == 'deals_mdf':
        get_and_upload_deal_modify()

    elif args.task == 'user':
        user()

    elif args.task == 'category':
        category()

    elif args.task == 'source':
        source()

    elif args.task == 'department':
        departament()


# deal_id_dc is deal_id
# deal_dc_modify_data is valid data for upload in database
def get_and_upload_deals_create():
    tg_bot.telegram_send_messages("Start: Выгрузка сделок по дате создания.")
    deal_id_dc, deal_dc_modify_data = Bitrix24.get_deals_date_create()
    Database.upload_db_deals_create(deal_dc_modify_data)
    tg_bot.telegram_send_messages("Finish: Выгрузка сделок по дате создания.")

def get_and_upload_deal_modify():
    tg_bot.telegram_send_messages("Start: Выгрузка сделок по дате изменения.")
    deal_id_dm, deal_dm_modify_data = Bitrix24.get_deals_date_modify()
    Database.upload_db_deals_modify(deal_dm_modify_data)
    tg_bot.telegram_send_messages("Finish: Выгрузка сделок по дате изменения.")
    return history_get(deal_id_dm)


def history_get(deal_id_dm):
    tg_bot.telegram_send_messages("Start: Выгрузка истории сделок.")
    history = Bitrix24.get_deal_history_stage(deal_id_dm)
    Database.upload_db_deals_history(history)
    tg_bot.telegram_send_messages("Finish: Выгрузка истории сделок.")


def departament():
    tg_bot.telegram_send_messages("Start: Выгрузка департаментов.")
    dep_info = Bitrix24.get_department()
    Database.department_upload(dep_info)
    tg_bot.telegram_send_messages("Finish: Выгрузка департаментов.")


def user():
    tg_bot.telegram_send_messages("Start: Выгрузка пользователей.")
    users_list = Bitrix24.user_get()
    Database.users_upload(users_list)
    tg_bot.telegram_send_messages("Finish: Выгрузка пользователей.")


def category():
    tg_bot.telegram_send_messages("Start: Выгрузка воронок.")
    category_list, category_id = Bitrix24.get_category()
    Database.category_upload(category_list)
    stage_in_category(category_id)
    tg_bot.telegram_send_messages("Finish: Выгрузка воронок.")


def stage_in_category(category_id):
    tg_bot.telegram_send_messages("Start: Выгрузка стадий воронок.")
    stage= Bitrix24.get_stage(category_id)
    Database.stage_category_upload(stage)
    tg_bot.telegram_send_messages("Finish: Выгрузка стадий воронок.")

def source():
    tg_bot.telegram_send_messages("Start: Выгрузка источников.")
    source_list = Bitrix24.get_source()
    Database.source_upload(source_list)
    tg_bot.telegram_send_messages("Finish: Выгрузка источников.")


if __name__ == "__main__":
    main()
