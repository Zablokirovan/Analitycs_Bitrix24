import os
from fast_bitrix24 import Bitrix

from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv

import ModifyData

load_dotenv()

# Webhook in Bitrix24
webhook = os.getenv('BITRIX_WEBHOOK')
# Waits the required amount of time between
# requests to avoid exceeding Bitrix24 limits
b_time_delay = Bitrix(webhook, respect_velocity_policy=True)

# Asia/Almaty time zone
tz = timezone(timedelta(hours=5))
# now date in Asia/Almaty
date_now = datetime.now(tz)

start_date = (date_now - timedelta(days=1)).strftime('%Y-%m-%dT00:00:00+05:00')
end_date = (date_now - timedelta(days=1)).strftime('%Y-%m-%dT23:59:59+05:00')


def get_deals_date_create():
    """
    A function for conducting deals from Bitrix24 by creation
     date with filters across all funnels
    :return:
    """
    try:
        with b_time_delay.slow(max_concurrent_requests=5):
            return ModifyData.data_modify_for_deals(
                b_time_delay.get_all(
                    'crm.deal.list',
                    params={
                        # DATE_CREATE to get created trades on this day
                        'filter': {
                            '>=DATE_CREATE': start_date,
                            '<=DATE_CREATE': end_date,
                        },
                        'select': [
                            'ID',  # Deal_id
                            'STAGE_ID',  # STAGE IN FLUE
                            'CURRENCY_ID',  # CURRENCY = KZT
                            'OPPORTUNITY',  # PRICE
                            'CONTACT_ID',  # CLIENT
                            'CLOSEDATE',
                            'DATE_CREATE',
                            'DATE_MODIFY',
                            'CATEGORY_ID',  # FUNNEL ID
                            'SOURCE_ID',
                            'UF_CRM_1569388305',  # URL_BLANK
                            'UF_CRM_5F3F5BECDFC07',  # DEPARTMENT
                            'STAGE_SEMANTIC_ID',  # S=successful,
                            # P=production, F=fatal
                            'CREATED_BY_ID']  # employe created deals
                    }))
    except Exception as e:
        print(e)


def get_deals_date_modify():
    """
    A function for conducting deals from Bitrix24 by creation
     date with filters across all funnels
    :return:
    """
    try:
        with b_time_delay.slow(max_concurrent_requests=5):
            return ModifyData.data_modify_for_deals(
                b_time_delay.get_all(
                    'crm.deal.list',
                    params={
                        'filter': {
                            # DATE_MODIFY to get the relevance of transactions.
                            '>=DATE_MODIFY': start_date,
                            '<=DATE_MODIFY': end_date
                        },
                        'select': [
                            'ID',  # Deal_id
                            'STAGE_ID',  # STAGE IN FLUE
                            'CURRENCY_ID',  # CURRENCY = KZT
                            'OPPORTUNITY',  # PRICE
                            'CONTACT_ID',  # CLIENT
                            'CLOSEDATE',
                            'DATE_CREATE',
                            'DATE_MODIFY',
                            'CATEGORY_ID',  # FUNNEL ID
                            'SOURCE_ID',
                            'UF_CRM_1569388305',  # URL_BLANK
                            'UF_CRM_5F3F5BECDFC07',  # DEPARTMENT
                            'STAGE_SEMANTIC_ID',  # S=successful,
                            # P=production, F=fatal
                            'CREATED_BY_ID']  # Employe created deals
                    }))

    except Exception as e:
        print(e)


def chunks(lst, size):
    """
    A function for generating batch requests to Bitrix24
     for reliability and to avoid blocking
    :param lst: list of deal IDs
    :param size: 50 transactions guarantee reliability and stability
    :return: None A list of information on the transaction's history by stage,
     with each stage in a separate dictionary
    """
    for i in range(0, len(lst), size):
        yield lst[i:i + size]


def get_deal_history_stage(deal_id, batch_size=50):
    """
    Function for obtaining information about the history of transaction
     progress by stages from Bitrix24
    :param deal_id:  list of deal IDs
    :param batch_size:size: 50 transactions guarantee reliability and stability
    :return: List[Dict] A list of information on the transaction's
    history by stage, with each stage in a separate dictionary
    """
    result = []

    for batch in chunks(deal_id, batch_size):

        with b_time_delay.slow(max_concurrent_requests=5):

            res = b_time_delay.get_all(
                'crm.stagehistory.list',
                params={
                    "entityTypeId": 2,
                    'filter': {
                        'OWNER_ID': batch
                    }
                })
            result.extend(res)

    return ModifyData.modify_history_data(result)


def get_department():
    """
    function for downloading information about user workstations
    :return: list
    """
    return ModifyData.department(b_time_delay.get_all('department.get'))


def user_get():
    """
    Downloading user information
    :return: list(dict[])
    """
    return ModifyData.user_modify(b_time_delay.get_all(
        'user.get', params={'filter': {'Active': True}}))

def get_category():
    """
    Downloading category information
    :return: list(dict[])
    """
    return ModifyData.category_modify(b_time_delay.get_all(
        'crm.category.list', params={'entityTypeId': 2 }))


def get_stage(category_list):
    """
    Downloading stage by category information and source
    :param category_list:
    :return: stage_list->list()
            source_list-> list(list(dict[]))
    """
    stage_list = []

    source_list = []

    res = b_time_delay.get_all('crm.status.list', params={
        "filter":
            {"ENTITY_ID": "SOURCE"}
    })

    source_list.append(res)

    for category in category_list:

        if category == 0:

            stage_list.append((b_time_delay.get_all(
                'crm.status.list', params={'filter':
                                               {'ENTITY_ID': "DEAL_STAGE"}
                                           })))
        else:
            res = b_time_delay.get_all('crm.status.list', params={
                'filter': {'ENTITY_ID': f"DEAL_STAGE_{category}"}
            })
            stage_list.append(res)

    return (ModifyData.stage_modify(stage_list),
            ModifyData.source_modify(source_list))
