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
    deal_id_dc, deal_dc_modify_data = Bitrix24.get_deals_date_create()
    Database.upload_db_deals_create(deal_dc_modify_data)

def get_and_upload_deal_modify():
    deal_id_dm, deal_dm_modify_data = Bitrix24.get_deals_date_modify()
    Database.upload_db_deals_modify(deal_dm_modify_data)
    return history_get(deal_id_dm)


def history_get(deal_id_dm):
    history = Bitrix24.get_deal_history_stage(deal_id_dm)
    Database.upload_db_deals_history(history)


def departament():
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
    stage= Bitrix24.get_stage(category_id)
    Database.stage_category_upload(stage)

def source():
    source_list = Bitrix24.get_source()
    Database.source_upload(source_list)


if __name__ == "__main__":
    main()
