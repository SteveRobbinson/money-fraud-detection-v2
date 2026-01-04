import pandas as pd
import lightgbm as lgb
import pathlib as Path
import joblib
import config
from snowflake.snowpark import Session

def train_model(
        connection: Session,
        training_table: str,
        validation_table: str,
        fraud_label: str,
        stage_location: str) -> str:

    train_set = connection.table(f"{training_table}_table").to_pandas()
    validation_set = connection.table(f"{validation_table}_table").to_pandas()
    
    train_set = lgb.Dataset(train_set.drop([fraud_label], axis=1),
                             label=train_set[fraud_label])

    validation_set = lgb.Dataset(validation_set.drop([fraud_label], axis=1),
                                  label=validation_set[fraud_label],
                                  reference=train_set)

    results = {}
    
    model = lgb.train(
        params = config.get_config(connection)['lightgbm_config'],
        train_set = train_set,
        valid_sets = [validation_set],
        valid_names = ['valid'],
        num_boost_round = config.get_config(connection)['num_boost_round'],
        callbacks = config.get_config(connection)['callbacks']
    )
  

    model_name = '/tmp/fraud_model.joblib'

    joblib.dump(model, model_name)

    connection.file.put(model_name, '@ml_stage', overwrite=True)

    return "Chyba pykło"
