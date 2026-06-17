import logging
import os

import ModifyData
import tg_bot

from fast_bitrix24 import Bitrix

from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv


load_dotenv()

logger = logging.getLogger(__name__)

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

start_date_m = date_now.strftime('%Y-%m-%dT00:00:00+05:00')
end_date_m = date_now.strftime('%Y-%m-%dT23:59:59+05:00')

_DEAL_SELECT = [
    'ID',
    'STAGE_ID',
    'CURRENCY_ID',
    'OPPORTUNITY',
    'CONTACT_ID',
    'CLOSEDATE',
    'DATE_CREATE',
    'DATE_MODIFY',
    'CATEGORY_ID',
    'SOURCE_ID',
    'UF_CRM_1569388305',    # URL_BLANK
    'UF_CRM_5F3F5BECDFC07', # DEPARTMENT
    'STAGE_SEMANTIC_ID',    # S=successful, P=production, F=fatal
    'CREATED_BY_ID',
    'ASSIGNED_BY_ID',
    'UF_CRM_1779339829',    # создана через айсулу
]


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
                    '   ',
                    params={
                        'filter': {
                            '>=DATE_CREATE': '2026-05-31',  # start_date_m
                            '<=DATE_CREATE': '2026-06-01',  # end_date_m
                            'CATEGORY_ID': '0',
                        },
                        'select': _DEAL_SELECT,
                    }))
    except Exception as e:
        tg_bot.telegram_send_messages(f"Error:get_deals_date_create {e}")
        raise


def get_deals_date_modify():
    """
    A function for conducting deals from Bitrix24 by modification
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
                            '>=DATE_MODIFY': '2026-06-05',  # start_date_m
                            '<=DATE_MODIFY': '2026-06-10',  # end_date_m
                            'CATEGORY_ID': '0',
                            'UF_CRM_1779339829': '1',
                        },
                        'select': _DEAL_SELECT,
                    }))
    except Exception as e:
        tg_bot.telegram_send_messages(f"Error:get_deals_date_modify {e}")
        raise


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

    try:
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

    except Exception as e:
        tg_bot.telegram_send_messages(f"Error:get_deal_history_stage {e}")
        raise


def get_history_by_date(start: str, end: str):
    """
    Get stage history filtered by CREATED_TIME for a date range.
    Used as the primary driver for the daily modified-deals pipeline:
    instead of filtering deals by DATE_MODIFY (which captures any field
    change, including old deals), we filter by when a stage transition
    actually happened.

    :param start: ISO-8601 datetime string, range start (inclusive)
    :param end:   ISO-8601 datetime string, range end   (inclusive)
    :return: tuple(history_data: list[tuple], deal_ids: list[str])
    """
    try:
        with b_time_delay.slow(max_concurrent_requests=5):
            raw = b_time_delay.get_all(
                'crm.stagehistory.list',
                params={
                    'entityTypeId': 2,
                    'filter': {
                        '>=CREATED_TIME': start,
                        '<=CREATED_TIME': end,
                    },
                })

        history_data = ModifyData.modify_history_data(raw)
        # OWNER_ID is at index 2 in each tuple (see modify_history_data)
        deal_ids = list({row[2] for row in history_data})
        logger.info(
            "Stage history: %d records, %d unique deals (%s → %s)",
            len(history_data), len(deal_ids), start, end,
        )
        return history_data, deal_ids

    except Exception as e:
        tg_bot.telegram_send_messages(f"Error:get_history_by_date {e}")
        raise


def get_deals_by_ids(deal_ids: list, batch_size: int = 50):
    """
    Fetch full deal data for a specific list of IDs (batched).
    Returns the same structure as get_deals_date_create /
    get_deals_date_modify so it can be passed directly to the DB layer.

    :param deal_ids:   list of deal ID strings
    :param batch_size: IDs per API request (50 is safe for Bitrix24)
    :return: tuple(deal_ids: list, deals: list[tuple])
    """
    raw = []
    try:
        for batch in chunks(deal_ids, batch_size):
            with b_time_delay.slow(max_concurrent_requests=5):
                res = b_time_delay.get_all(
                    'crm.deal.list',
                    params={
                        'filter': {'ID': batch},
                        'select': _DEAL_SELECT,
                    })
                raw.extend(res)

        logger.info("Fetched %d deals by ID.", len(raw))
        return ModifyData.data_modify_for_deals(raw)

    except Exception as e:
        tg_bot.telegram_send_messages(f"Error:get_deals_by_ids {e}")
        raise


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
        'crm.category.list', params={'entityTypeId': 2}))


def get_stage(category_list):
    """
    Downloading stage by category information and source
    :param category_list:
    :return: stage_list->list()
            source_list-> list(list(dict[]))
    """
    stage_list = []

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

    return ModifyData.stage_modify(stage_list)


def get_source():
    """
       Downloading stage by source information
       :param :
       :return: source_list-> list(dict[])
    """
    return ModifyData.source_modify(
        b_time_delay.get_all('crm.status.list',
                             params={"filter": {"ENTITY_ID": "SOURCE"}
                                     }))
