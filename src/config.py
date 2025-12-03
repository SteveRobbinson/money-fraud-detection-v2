from pathlib import Path

data_dir = Path('data')

raw_dir = data_dir / 'raw' 
raw_path = raw_dir / 'raw_data.csv'

processed_dir = data_dir / 'processed'
processed_path = processed_dir / 'processed.csv'

models_dir = data_dir / 'models'
model_path = models_dir / 'models.joblib'


get_features = ['sender_account',
                'receiver_account',
                'ip_address',
                'device_hash'
                ]


drop_list = [*get_features,
             'transaction_id',
             'fraud_type',
             'time_since_last_transaction',
             'timestamp'
             ]


dummies = ['transaction_type',
           'merchant_category',
           'location',
           'device_used',
           'payment_channel'
           ]





