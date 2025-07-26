
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from imblearn.over_sampling import SMOTE
import joblib

def train_model(df, target_col='is_fraud'):
    X = df.drop(columns=[target_col, 'transaction_id', 'transaction_dt'])
    y = df[target_col]

    X_train, X_test, y_train, y_test = train_test_split(X, y, stratify=y, test_size=0.2, random_state=42)

    sm = SMOTE(random_state=42)
    X_res, y_res = sm.fit_resample(X_train, y_train)

    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_res, y_res)

    joblib.dump(model, 'models/model.pkl')
    return model, X_test, y_test
