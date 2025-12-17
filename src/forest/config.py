from pathlib import Path

base_dir = Path(__file__).parents[2]

data_dir = base_dir / 'data'
test_path = data_dir / 'test' / '1k_sample.csv'

raw_dir = data_dir / 'raw' 
raw_path = raw_dir / 'raw_data.csv'

processed_dir = data_dir / 'processed'
processed_path = processed_dir / 'processed.csv'

models_dir = data_dir / 'models'
model_path = models_dir / 'models.joblib'

num_samples = 1000000
num_samples_test = 100

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

parametry_rf = {
        'n_estimators': 500,
        'batch_size': 70000,
        'max_depth': 13,
        'max_features': 10,
        'min_samples_split': 15000,
        'min_samples_leaf': 70
}

model_path = base_dir / 'models' / 'random_forest_model.pkl'



