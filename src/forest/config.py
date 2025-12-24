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


drop_list = ['transaction_id',
             'fraud_type',
             'time_since_last_transaction'
             ]


dummies = ['transaction_type',
           'merchant_category',
           'location',
           'device_used',
           'payment_channel'
           ]

params_lightgbm = {
    'objective': 'binary',
    'boosting_type': 'gbdt' ,
    'learning_rate': 0.02,
    'num_leaves': 48,
    'max_depth': 8,
    'min_data_in_leaf': 1000,
    'scale_pos_weight': 25,
    'feature_fraction': 0.7,
    'seed': 42,
    'verbosity': -1
}

parametry_rf_test = {
        'n_estimators': 1,
        'batch_size': 100,
        'max_depth': 13,
        'max_features': 3,
        'min_samples_split': 2,
        'min_samples_leaf': 1
}
model_path = base_dir / 'models' / 'random_forest_model.pkl'



