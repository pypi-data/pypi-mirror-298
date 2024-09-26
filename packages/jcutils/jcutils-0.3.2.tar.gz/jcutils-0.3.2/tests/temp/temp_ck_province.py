from src.api.conn import ck1_client

table_list = [
    "ads_coordination_purchase_supplier",
    "ads_coupon_apportion_detail_day",
    "ads_coupon_apportion_district_month",
    "ads_coupon_use_information",
    "ads_crm_tp_shop_member_first_c",
    "ads_fresh_shop_sales",
    "ads_item_subclass_sale",
    "ads_itemprice_sales_section",
    "ads_jd_erp_sales_ou_or",
    "ads_kefu_gq_claim",
    "ads_member_consumption_order",
    "ads_member_coupon_detail",
    "ads_member_coupon_get_use_detail",
    "ads_member_frequency_month",
    "ads_member_label_distribution",
    "ads_national_sales_comparison",
    "ads_operate_sales_details",
    "ads_order_center_recon_total",
    "ads_orderprice_sales_section",
    "ads_popularize_member_detail",
    "ads_report_enter_order_detailed",
    "ads_sales_channel_details",
    "ads_sales_item_shop_di",
    "ads_sales_item_shop_gross_profit",
    "ads_sales_shop_channel_etl",
    "ads_sales_shop_notdis",
    "ads_shop_empowerment_sale_stream_unique",
    "ads_shop_hour_ordernums",
    "ads_shop_item_sku",
    "ads_shop_member_energize",
    "ads_shop_member_rank_info",
    "ads_shop_stock_current",
    "ads_shop_stock_item_current",
    "ads_shop_yp_channel_sales",
    "ads_t_cus_account_info",
    "dim_jd_erp_shop",
    "dm_member_info_label",
    "supply_chain_stock_screen_stream",
    "ads_popularize_order_info",
]

for table in table_list:
    if "_unique" in table:
        sql = f"select count(1) as count from {table} final"
    else:
        sql = f"select count(1) as count from {table}"
    count1 = ck1_client.query(sql)[0][0]
    print(table + "  " + str(count1))
    # break
