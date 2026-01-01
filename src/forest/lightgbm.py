import pandas as pd
import lightgbm as lgb
import pathlib as Path
import joblib
import config

def train_model(
        connection: Session,
        training_table: str,
        validation_table: str) -> str:

    train_set = connection.table(f"{training_table}_table").to_pandas()
    validation_set = connection.table(f"{validation_table}_table").to_pandas()
    
    train_data = lgb.Dataset(train_set.drop(['IS_FRAUD'], axis=1),
                             label=train_set['IS_FRAUD'])

    validation_data = lgb.Dataset(validation_set.drop(['IS_FRAUD'], axis=1),
                                  label=validation_set['IS_FRAUD'],
                                  reference=train_data)

    results = {}
    
    model = lgb.train(
        params = config.get_config(connection, pwd="hehe")['lightgbm_config'],
        train_set = train_data,
        valid_sets = [validation_data],
        valid_names = ['valid'],
        num_boost_round = 300,
        callbacks = [
            lgb.log_evaluation(20),
            lgb.early_stopping(50),
            lgb.record_evaluation(results)
        ]
    )
  

    model_name = '/tmp/fraud_model.joblib'

    joblib.dump(model, model_name)

    connection.file.put(model_name, '@ml_stage', overwrite=True)
    
    return 'Chyba pykło'
