with source_data as (
  select * from {{ ref('fct_time') }}
)

select
  day_of_week
from
  source_data
where
  day_of_week in (6, 7)
  and
  is_weekend = 0
