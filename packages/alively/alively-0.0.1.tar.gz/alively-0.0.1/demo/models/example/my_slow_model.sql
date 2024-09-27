{{
    config(materialized='table')
}}

select 'somedatahere'
from generate_series(1,10000000)