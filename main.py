import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
from catboost import CatBoostRegressor
from scipy import stats


def train_model():
    global random_forest_model
    housing_df = pd.read_csv("./lol/data2.csv", sep=';')
    for col in housing_df.columns:
        if housing_df[col].dtype == 'object':
            housing_df[col] = housing_df[col].str.replace(',', '.').astype(float)
    housing_df.dropna(inplace=True)
    housing_df = housing_df.sample(frac=1).reset_index(drop=True)
    columns = housing_df.select_dtypes(include=['float64', 'int64']).columns
    housing_df[columns] = housing_df[columns].astype('int32')
    z_threshold = 5
    # Calculate Z-scores for each column
    z_scores = stats.zscore(housing_df)
    # Find rows where any column has a Z-score greater than the threshold
    outlier_rows = (z_scores > z_threshold).any(axis=1)
    # Remove outliers by keeping rows where all columns have Z-scores within the threshold
    cleaned_df = housing_df[~outlier_rows]
    # clean outliers which are above 150000000 price
    cleaned_df = cleaned_df[cleaned_df["Цена"] > 0]
    X = cleaned_df.iloc[:, 1:]
    y = cleaned_df['Цена']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    random_forest_model = RandomForestRegressor(n_estimators=150, random_state=42)
    random_forest_model.fit(X_train, y_train)


train_model()

def get_price(params):
    kv_pred = random_forest_model.predict([list(params.values())])
    return int(kv_pred[0])

