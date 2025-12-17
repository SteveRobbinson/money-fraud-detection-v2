from forest.downsample_majority import downsample_majority 
from forest import config

def test_downsampling(preprocessed_df):
    
    df_downsampled = downsample_majority(preprocessed_df, config.num_samples_test)
    
    assert len(df_downsampled) < len(preprocessed_df)

    before = (preprocessed_df['is_fraud'] == True).sum()
    after = (df_downsampled['is_fraud'] == True).sum()
    assert before == after
