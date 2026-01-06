import Bitrix24
import Database

#deal_id_dc = deal_id
#deal_dc_modify_data = valid data for upload in database
deal_id_dc, deal_dc_modify_data = Bitrix24.get_deals_date_create()
Database.upload_db_deals_create(deal_dc_modify_data)




