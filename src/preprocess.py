
import pandas as pd
from sklearn.preprocessing import StandardScaler

def load_data(file_path):
    df = pd.read_csv(file_path)
    return df

def clean_data(df):
    df['transaction_dt'] = pd.to_datetime(df['transaction_dt'], errors='coerce')
    df.fillna({
        'merchant_category': 'Unknown',
        'transaction_amount': df['transaction_amount'].median()
    }, inplace=True)
    return df

def scale_features(df, feature_columns):
    scaler = StandardScaler()
    df[feature_columns] = scaler.fit_transform(df[feature_columns])
    return df, scaler
