```mermaid
    
    erDiagram       
        file_query |{--|| exchange_product: relates
        file_query |{--|| file_stage: represents
        file_stage ||--|{ file_stage_status: has
        exchange_product |{--|| exchange_product_status : has
        exchange_product |{--|| exchange_product_term : has
        file_query{
            int file_query_id
            string cli
            string site_postcode
            string exchange_name
            string exchange_code
            string exchange_postcode
            int avg_data_usage
            string stop_sell_date
            int file_stage_fk
            int exchange_product_fk
        }        
        exchange_product{
            int exchange_product_id
            string exchange_product_name
            int exchange_product_limit
            string exchange_product_unit
            string exchange_product_url
            decimal exchange_product_price            
            bit exchange_product_default
            int exchange_product_term_fk
            string exchange_product_status_fk
        }
        exchange_product_term{
            int exchange_product_term_id
        }                
        file_stage{
            int file_stage_id
            string email_address
            string file_name
            string file_path
            string file_size
            string file_modified_date
            string file_stage_status_fk
            string created_at
        }
        file_stage_status{
            string file_stage_status_id
        }
        exchange_product_status{
            string exchange_product_status_id
        }
        exchange_decom{
            int exchange_decom_id
            string site_no
            string exchange_name
            string exchange_location
            string exchange_code
            string implementation_date
            date last_amended_date
            string tranche
            timestamp created_at
        }  


        