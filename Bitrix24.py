import os
from fast_bitrix24 import Bitrix

from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv

load_dotenv()

#Webhook in Bitrix24
webhook = os.getenv('BITRIX_WEBHOOK')
# Waits the required amount of time between
# requests to avoid exceeding Bitrix24 limits
b_time_delay = Bitrix(webhook, respect_velocity_policy=True)

#Asia/Almaty time zone
tz = timezone(timedelta(hours=5))
#now date in Asia/Almaty
date_now = datetime.now(tz)

start_date = (date_now - timedelta(days=1)).strftime('%Y-%m-%dT00:00:00+05:00')
end_date   = (date_now - timedelta(days=1)).strftime('%Y-%m-%dT23:59:59+05:00')

def get_deals_date_create():
    """
    A function for conducting deals from Bitrix24 by creation date with filters across all funnels
    :return: dict
    """
    try:
        with b_time_delay.slow(max_concurent_request=5):
            return b_time_delay.get_all('crm.deal.list', params={
                'filter':{
                    '>=DATE_MODIFY': start_date,
                    '<=DATE_MODIFY': end_date,
                },
                'select':{
                    'ID',# deal_id
                    'STAGE_ID',#STAGE IN FLUE
                    'CURRENCY_ID'#CURRENCY = KZT ,
                    'OPPORTUNITY', #PRICE
                    'CONTACT_ID', #CLIENT,
                    'CLOSEDATE',
                    'DATE_CREATE',
                    'DATE_MODIFY',
                    'CATEGORY_ID',#FUNNEL ID
                    'SOURCE_ID',
                    'UF_CRM_1569388305', #URL_BLANK
                    'UF_CRM_5F3F5BECDFC07', #DEPARTMENT
                    'STAGE_SEMANTIC_ID'#S = successful, P = production, F = fatal
                }
            })
    except Exception as e:
        print(e)