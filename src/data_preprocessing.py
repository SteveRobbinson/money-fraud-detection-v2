from pathlib import Path
import pandas as pd

def load_raw_data(path: Path) -> pd.DataFrame:
    return pd.read_csv(path)


def encode_time(df: pd.DataFrame, column_name: str) -> pd.DataFrame:
    col = pd.to_datetime(df[column_name], format='mixed')

    df[column_name] = col
    df['hour'] = col.dt.hour
    df['weekday'] = col.dt.weekday
    df['day'] = col.dt.day
    df['is_weekend'] = df['weekday'].isin([5, 6]).astype(int)

    return df


def create_features(df: pd.DataFrame, features: list[str]) -> pd.DataFrame:

    df.sort_values(['timestamp'], inplace=True)
    
    for col in features:
        g = df.groupby(col)
        
        df['transactions_made_by_' + col] = g.transform('size')
        df['avg_amount_by_' + col] = g['amount'].transform('mean')
        df['min_amount_by_' + col] = g['amount'].transform('min')
        df['max_amount_by_' + col] = g['amount'].transform('max')
        df['median_amount_by_' + col] = g['amount'].transform('median')


        # NaNy, czyli transakcje wykonane poraz pierwszy wypełniam cyfrą -1
        df['time_since_last_transaction_by_' + col] = (
            g['timestamp']
                .diff()
                .dt.total_seconds()
                .fillna(-1)
        )
        
        # Czy dana transakcja była pierwszą z danej cechy?
        df['is_first_transaction_on_' + col] = (
            (df['time_since_last_transaction_by_' + col] == -1)
            .astype(int)
        )

    return df
    

def get_dummies(df: pd.DataFrame, dummies: list[str]) -> pd.DataFrame:
    return pd.get_dummies(df, columns=dummies, dtype=int)


def drop_columns(df: pd.DataFrame, column_names: list[str]) -> pd.DataFrame:
    return df.drop(column_names, axis=1, errors='ignore')


def preprocess(
    path: Path,
    features: list[str],
    dummies: list[str],
    column_names: list[str]
) -> pd.DataFrame:
    
    df = load_raw_data(path)
    df = encode_time(df, 'timestamp')
    df = create_features(df, features)
    df = get_dummies(df, dummies)
    df = drop_columns(df, column_names)

    return df

def split_features_target(df: pd.DataFrame, target_column: str) -> tuple[pd.DataFrame, pd.Series]:
    if target_column not in df.columns:
        raise ValueError(
            f"Target column: '{target_column}' does not exist in Dataframe"
        )

    X = df.drop(target_column, axis=1)
    y = df[target_column]

    return X, y
        

def save_data(df: pd.DataFrame, path: Path):
    path.mkdir(parents=True, exist_ok=True)

    output_path = path / 'processed.csv'
    df.to_csv(output_path, index=False)
