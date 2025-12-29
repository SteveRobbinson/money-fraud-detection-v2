{% set dimensions_full = ['sender_account', 'receiver_account', 'device_hash', 'ip_address'] %}
{% set time_windows = ['1 hour', '24 hour', '30 day'] %}
with staging_data as (
  select * from {{ ref('stg_transactions') }}
),

{# dla sender, receiver, device, ip licze liczbe transakcji wykonanych w danym oknie czasowym #}

windows_computed as (
  select
    transaction_id
    {% for dim in dimensions_full %}
      {% for i in range(time_windows|length) %}
        , count(*) over(
          partition by {{ dim }}
          order by timestamp
          range between interval '{{ time_windows[i] }}' preceding and current row
        ) as {{ dim.split('_')[0] }}_num_trx_{{ var('time_suffix')[i] }}
      {% endfor %}
    {% endfor %}
    from staging_data
  )

select * from windows_computed


