"""
This file is required to modify the data downloaded from Bitrix24.
 For further loading into the Database
"""

from datetime import datetime, date

def data_modify_for_deals(deal_list):
    deal_id=[]
    date_for_upload = []

    for deal in deal_list:
        deal_id.append(deal['ID'])
        date_for_upload.append((
            int(deal['ID']),
            int(deal['CONTACT_ID']) if deal.get('CONTACT_ID') else None,
            deal['STAGE_ID'],
            datetime.fromisoformat(deal['CLOSEDATE']).strftime("%Y-%m-%d"),
            datetime.fromisoformat(deal['DATE_CREATE']).strftime("%Y-%m-%d"),
            datetime.fromisoformat(deal['DATE_MODIFY']).strftime("%Y-%m-%d"),
            int(deal['CATEGORY_ID']),
            deal['SOURCE_ID'],
            deal['STAGE_SEMANTIC_ID'],
            int(deal['CREATED_BY_ID']) if deal.get('CREATED_BY_ID') else None,
            None if deal['UF_CRM_1569388305'] is None else
            deal['UF_CRM_1569388305']['downloadUrl'],
            int(deal['UF_CRM_5F3F5BECDFC07']) if deal.get(
                'UF_CRM_5F3F5BECDFC07'
            ) else None
        ))
    return deal_id, date_for_upload