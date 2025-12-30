with staging_data as (
  select * from {{ ref('stg_transactions') }}
),

city_counts as (
  select
    transaction_id,
    count(*) over(
    partition by sender_account, location
    order by timestamp
    rows between unbounded preceding and 1 preceding
    ) as location_frequency
  from staging_data
)

select * from city_counts
