{% snapshot second_model_snapshot %}

{{
    config(
      unique_key='col1',
      target_schema='snapshots', 
      strategy='timestamp',
      updated_at='updated_at',
    )
}}

select * from {{ ref('my_second_dbt_model') }} limit 1

{% endsnapshot %}