from math import remainder


def serialize_product(product):
    return {
        "product_id": product[0],
        "product_name": product[1],
        "product_limit": product[2],
        "product_unit": product[3],
        "product_url": product[4],
        "product_price": product[5],
        "product_default": product[6],
        "product_status": product[7],        
    }


def serialize_pricing(pricing):
    return {
        "product_name": pricing[0],
        "product_limit": pricing[1],
        "product_unit": pricing[2],        
        "product_price": pricing[3],
        "product_category": pricing[4],
        "product_class": pricing[5],        
        "product_term": pricing[6],
    }

def serialize_recommendation(recommendation):
    return {
        "file_upload_id": recommendation[0],
        "exchange_query_status_id": recommendation[1],
        "file_email_address": recommendation[2],        
        "exchange_query_id": recommendation[3],
        "cli": recommendation[4],
        "site_postcode": recommendation[5],        
        "exchange_name": recommendation[6],
        "exchange_code": recommendation[7],
        "avg_data_usage": recommendation[8],
        "stop_sell_date": recommendation[9],
        "switch_off_date": recommendation[10],
        "redis_cache_result_key": recommendation[11],
    }

def serialize_price_recommendations(recommendations):
    return {
        "file_upload_id": recommendations["file_upload_id"],
        "exchange_query_status_id": recommendations["exchange_query_status_id"],
        "file_email_address": recommendations["file_email_address"],        
        "exchange_query_id": recommendations["exchange_query_id"],
        "cli": recommendations["cli"],
        "site_postcode": recommendations["site_postcode"],        
        "exchange_name": recommendations["exchange_name"],
        "exchange_code": recommendations["exchange_code"],
        "avg_data_usage": recommendations["avg_data_usage"],
        "stop_sell_date": recommendations["stop_sell_date"],
        "switch_off_date": recommendations["switch_off_date"],
        "redis_cache_result_key": recommendations["redis_cache_result_key"],
        "product_pricing": recommendations["product_pricing"],        
    }    

def serialize_map_location(location):
    return {
        "address_components": location["address_components"],
        "formatted_address": location["formatted_address"],
        "geometry": location["geometry"],
        "place_id": location["place_id"],
        "types": location["types"],
    }


def serialize_fttp_exchange(exchange):
    return {
        "id": exchange[0],
        "site_no": exchange[1],
        "exchange_name": exchange[2],
        "exchange_location": exchange[3],
        "exchange_code": exchange[4],
        "implementation_date": exchange[5],
        "last_amended_date": str(exchange[6]),
        "tranche": exchange[7],
        "created_at": exchange[8],
    }


def serialize_sam_exchange(exchange):
    return {
        "exchange_name": exchange[0],
        "exchange_code": exchange[1],
        "exchange_county": exchange[2],
        "exchange_region": exchange[3],
    }


def serialize_sam_exchange_location(exchange):
    return {
        "exchange_name": exchange["Exchange name"],
        "exchange_code": exchange["Exchange code"],
        "exchange_location": exchange["Location"],
        "exchange_postcode": exchange["Postcode"],
        "exchange_maps": exchange["Maps"],
        "exchange_serves": exchange["Serves (approx)"],
    }
