"""
This file is required to modify the data downloaded from Bitrix24.
 For further loading into the Database
"""

from datetime import datetime
from zoneinfo import ZoneInfo

def data_modify_for_deals(deal_list, with_version: bool = False):
    # deal_ids
    deal_id = []
    # valid data for deals
    date_for_upload = []

    load_at = datetime.now()
    version = int(load_at.timestamp()) if with_version else None

    for deal in deal_list:
        deal_id.append(deal['ID'])

        row = [int(deal['ID']),
               int(deal['CONTACT_ID']) if deal.get('CONTACT_ID') else None,
               deal['STAGE_ID'],
               datetime.fromisoformat(deal['CLOSEDATE']).date(),
               datetime.fromisoformat(deal['DATE_CREATE']).date(),
               datetime.fromisoformat(deal['DATE_MODIFY']).date(),
               int(deal['CATEGORY_ID']),
               deal['SOURCE_ID'],
               deal['STAGE_SEMANTIC_ID'],
               int(deal['CREATED_BY_ID']) if
               deal.get('CREATED_BY_ID') else None,
               None if deal['UF_CRM_1569388305'] is None else
               deal['UF_CRM_1569388305']['downloadUrl'],
               int(deal['UF_CRM_5F3F5BECDFC07']) if deal.get(
                   'UF_CRM_5F3F5BECDFC07'
               ) else None]
        # Since the same error handling logic is used for deals loaded by
        # creation date and date modified, for deals loaded by creation date,
        # the with_version flag will be set to true, and a version record will
        # be added to the shared array. For deals loaded by date modified only
        if with_version:
            row.append(version)

        date_for_upload.append(tuple(row))

    return deal_id, date_for_upload


def modify_date(date):
    dt = datetime.fromisoformat(date)
    return  dt.astimezone(ZoneInfo("Asia/Almaty"))


def modify_history_data(history):
    result = []

    for i in history:
        dt = modify_date(i['CREATED_TIME'])

        result.append((
            i['ID'],
            i['TYPE_ID'],
            i['OWNER_ID'],
            dt,
            dt.date(),
            i["CATEGORY_ID"],
            i["STAGE_ID"]
        ))

    return result


def department(department_list):
    dep_m = []
    for i in department_list:
        dep_m.append((
            int(i['ID']),
            i["NAME"],
            i["SORT"],
            int(i['CREATED_BY_ID']) if i.get("CREATED_BY_ID") else None,
            int(i['UF_HEAD']) if i.get("UF_HEAD") else None,
            datetime.now()
        ))
    return dep_m

def user_modify(users_list):
    user_m = []
    for user in users_list:
        user_m.append((
            int(user['ID']),
            int(user['XML_ID']),
            1 if user['ACTIVE'] == True else 0,
            user.get('NAME') or None,
            user['LAST_NAME'] if user['LAST_NAME'] else None,
            user['SECOND_NAME'] if user.get('SECOND_NAME') else None,
            user['EMAIL'] if user['EMAIL'] else None,
            modify_date(user['LAST_LOGIN']).date() if user.get('LAST_LOGIN') else None,
            user['WORK_POSITION'] if user.get('WORK_POSITION') else None,
            None if user['UF_DEPARTMENT'] is None
            else user['UF_DEPARTMENT'][0],
            user['UF_USR_EMPLOYEE_1CKA_CODE'] if user.get('UF_USR_EMPLOYEE_1CKA_CODE')
            else None,
            user['PERSONAL_MOBILE'] if user.get('PERSONAL_MOBILE') else None,
            user['PERSONAL_CITY'] if user.get('PERSONAL_CITY') else None,
            user['WORK_PHONE'] if user.get('WORK_PHONE') else None,
            int(user['UF_PHONE_INNER']) if user.get('UF_PHONE_INNER') else None,
            datetime.now()
        ))
    return user_m
