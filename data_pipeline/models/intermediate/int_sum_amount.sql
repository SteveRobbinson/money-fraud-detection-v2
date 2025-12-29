{% set dimensions_full = ['sender_account', 'receiver_account', 'device_hash', 'ip_address'] %}

with transaction_counts as (
  select * from {{ ref('stg_transactions') }}
),

{# dla sender, receiver, device, ip licze sumę transakcji wykonanych w danym oknie czasowym #}
{# dodatkowo dla sender licze średnią i odchylenie dla okna czasowego = 30dni #}


sum_avg_sd as (
  select
    transaction_id
    {% for dim in dimensions_full %}
      {% for i in range(var('time_frames')|length) %}
        , sum(amount) over(
          partition by {{ dim }}
          order by timestamp
          range between interval '{{ var("time_frames")[i] }}' preceding and current row
        ) as {{ dim.split('_')[0] }}_sum_trx_{{ var('time_suffix')[i] }}
      {% endfor %}

      {% if dim == 'sender_account' %}
        , avg(amount) over(
            partition by {{ dim }}
            order by timestamp
            range between interval '30 day' preceding and current row
          ) as sender_mean_trx_30d
          
        , (coalesce(stddev(amount) over(
            partition by {{ dim }}
            order by timestamp
            range between interval '30 day' preceding and current row
          ), 0) as sender_stddev_trx_30d
      {% endif %} 
    {% endfor %}
  from transaction_counts
)

select * from sum_avg_sd
