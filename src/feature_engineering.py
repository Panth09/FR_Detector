
import pandas as pd

def add_time_features(df):
    df['hour_of_day'] = df['transaction_dt'].dt.hour
    df['day_of_week'] = df['transaction_dt'].dt.dayofweek
    return df

def add_value_features(df):
    user_avg = df.groupby('user_id')['transaction_amount'].transform('mean')
    df['user_avg_amount'] = user_avg
    df['amount_vs_avg_ratio'] = df['transaction_amount'] / (user_avg + 1e-5)
    return df

def add_frequency_features(df):
    df['transaction_dt'] = pd.to_datetime(df['transaction_dt'])

    df = df.sort_values(by=['user_id', 'transaction_dt'])
    df['user_trans_freq_24h'] = df.groupby('user_id')['transaction_dt'].diff().dt.total_seconds().fillna(999999).apply(lambda x: 1 if x < 86400 else 0).cumsum()

    df = df.sort_values(by=['card_id', 'transaction_dt'])
    df['card_trans_freq_1h'] = df.groupby('card_id')['transaction_dt'].diff().dt.total_seconds().fillna(999999).apply(lambda x: 1 if x < 3600 else 0).cumsum()

    return df
