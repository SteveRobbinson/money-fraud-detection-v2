import pandas as pd

def downsample_majority(
        df: pd.DataFrame,
        num_samples: int
        ) -> pd.DataFrame:

    df_not_fraud = df[df['is_fraud'] == False]
    df_fraud = df[df['is_fraud'] == True]

    df_not_fraud = df_not_fraud.sample(num_samples, random_state=43)
    df_downsampled = pd.concat([df_not_fraud, df_fraud])

    return df_downsampled.sample(frac=1).reset_index(drop=True)


