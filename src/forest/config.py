from pathlib import Path
import os

# Bezpiecznik dla importu dotenv
try:
    from dotenv import load_dotenv
except ImportError:
    load_dotenv = None

def get_config(session=None, pwd=None) -> dict:

    if session is not None:
        password = pwd
        import _snowflake
            
        return {
            'snowflake_info': {
                "SNOWFLAKE_USER": session.get_current_user(),
              # "SNOWFLAKE_PASSWORD": _snowflake.get_generic_secret_string('snowflake_access'),
                "SNOWFLAKE_PASSWORD": password,
                "SNOWFLAKE_ACCOUNT": session.get_current_account() ,
                "SNOWFLAKE_WAREHOUSE": session.get_current_warehouse(),
                "SNOWFLAKE_DATABASE": session.get_current_database(),
                "SNOWFLAKE_SCHEMA": session.get_current_schema()
            },
            'lightgbm_config': lightgbm_parameters
        }
        

    from dotenv import load_dotenv
    load_dotenv()

    return {
        'connection_parameters': {
            "account": os.getenv('SNOWFLAKE_ACCOUNT'),
            "user": os.getenv('SNOWFLAKE_USER'),
            "password": os.getenv('SNOWFLAKE_PASSWORD'),
            "role": os.getenv('SNOWFLAKE_ROLE'),
            "warehouse": os.getenv('SNOWFLAKE_WAREHOUSE'),
            "database": os.getenv('SNOWFLAKE_DATABASE'),
            "schema": os.getenv('SNOWFLAKE_SCHEMA')
        },

        'lightgbm_config': lightgbm_parameters,
    }

lightgbm_parameters = {
            'objective': 'binary',
            'metric': 'auc',
            'boosting_type': 'gbdt',
            'learning_rate': 0.01, 
            'num_leaves': 31,     
            'max_depth': -1,      
            'min_data_in_leaf': 2000, 
            'feature_fraction': 0.9,
            'is_unbalance': True,
            'bagging_fraction': 0.8,
            'bagging_freq': 5,
            'seed': 42,
            'verbosity': -1,
            'boost_from_average': True
}
