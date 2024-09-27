
-- Use the `ref` function to select from other models

{{
    config(materialized='table')
}}

select 'somedatahere' as col1, current_timestamp as updated_at
from generate_series(1,5000000)
