from .common_imports import *
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from datetime import datetime
from autosklearn.classification import AutoSklearnClassifier
from autosklearn.regression import AutoSklearnRegressor
from autosklearn.metrics import roc_auc, average_precision, accuracy, f1, precision, recall, log_loss
import joblib
import pandas as pd


class AutoMl:
    def __init__(self, data, target_column, objective, folder_path,
                 time_left_for_this_task=None, per_run_time_limit=None, ensemble_size=None, n_jobs=None):
        self.data = data
        self.target_column = target_column
        self.objective = objective
        self.folder_path = folder_path

        # Optional parameters with default values
        self.time_left_for_this_task = time_left_for_this_task
        self.per_run_time_limit = per_run_time_limit
        self.ensemble_size = ensemble_size
        self.n_jobs = n_jobs

        self.main_function(self.data)

    def main_function(self, df):
        self.df = df
        self.features, self.label, self.num_list, self.cat_list = self.data_preprocessing(self.df)
        self.X_train, self.X_test, self.y_train, self.y_test = self.train_test_data(self.features, self.label)

        # Save Train, Test data
        self.save_train_test_data()

        # Feature encoding
        self.training_features = self.feature_encoding(self.X_train, self.num_list, self.cat_list)
        self.training_label = self.y_train[[self.target_column]].to_numpy()

        # Check if Regression or Classification Problem
        if self.objective.lower() == 'classification':
            model_type = 'classifier'
        else:
            model_type = 'regressor'

        # Train model
        model = self.train_model(model_type, self.training_features, self.training_label)

        # Save model
        self.save_model(model, model_type)

    def save_train_test_data(self):
        print("Saving train and test data for calculating accuracy score")
        self.X_train.to_csv(f'{self.folder_path}/X_train.csv', index=False)
        print("X_train is Saved")
        self.X_test.to_csv(f'{self.folder_path}/X_test.csv', index=False)
        print("X_test is Saved")
        self.y_train.to_csv(f'{self.folder_path}/y_train.csv', index=False)
        print("y_train is Saved")
        self.y_test.to_csv(f'{self.folder_path}/y_test.csv', index=False)
        print("y_test is Saved")

    def data_preprocessing(self, df):
        print('Starting Data Preprocessing')
        df = df.drop_duplicates()

        label = df[[self.target_column]]
        feature = df.drop(columns=self.target_column)

        num_df = feature.select_dtypes(include=['float64', 'int64'])
        obj_df = feature.select_dtypes(exclude=['float64', 'int64'])

        date_df = pd.DataFrame()
        cat_df = pd.DataFrame()

        for col in obj_df.columns:
            if obj_df[col].dtype == 'object':
                try:
                    date_df[col] = pd.to_datetime(obj_df[col])
                except ValueError:
                    cat_df[col] = obj_df[col]
            if obj_df[col].dtype == 'datetime64[ns]':
                try:
                    date_df[col] = pd.to_datetime(obj_df[col])
                except ValueError:
                    cat_df[col] = obj_df[col]
            if obj_df[col].dtype == 'bool_':
                try:
                    cat_df[col] = obj_df[col].map({True: 'True', False: 'False'})
                except ValueError:
                    cat_df[col] = obj_df[col]

        for col in num_df.columns:
            if num_df[col].nunique() <= 5:
                try:
                    cat_df[col] = num_df[col].astype(str)
                    num_df.drop(col, inplace=True, axis=1)
                except ValueError:
                    pass

        for col in date_df:
            cat_df[col + '_YEAR'] = date_df[col].dt.year.astype(str)
            cat_df[col + '_MONTH'] = date_df[col].dt.month.astype(str)

        features = pd.concat([num_df, cat_df], axis=1)

        num_list = num_df.columns.tolist()
        cat_list = cat_df.columns.tolist()
        date_list = date_df.columns.tolist()

        joblib.dump(num_list, f'{self.folder_path}/numeric_column_list')
        joblib.dump(cat_list, f'{self.folder_path}/categorical_column_list')
        joblib.dump(date_list, f'{self.folder_path}/date_column_list')
        joblib.dump(features.columns.tolist(), f'{self.folder_path}/feature_column_order')

        print('Data Preprocessing Completed')
        return features, label, num_list, cat_list

    def feature_encoding(self, train_features, num_list, cat_list):
        print('Starting Feature Encoding')

        num_pipeline = Pipeline([
            ('imputer', SimpleImputer(strategy='median')),
            ('std_scaler', StandardScaler())
        ])

        cat_pipeline = Pipeline([
            ('imputer', SimpleImputer(strategy='most_frequent')),
            ('one-hot', OneHotEncoder(handle_unknown='ignore', sparse=False))
        ])

        transformers = []
        if num_list:
            transformers.append(('numerical', num_pipeline, num_list))
        if cat_list:
            transformers.append(('categorical', cat_pipeline, cat_list))

        if not transformers:
            raise ValueError("Both Numeric and Categorical Variables are missing")

        full_pipeline = ColumnTransformer(transformers)
        training_features = full_pipeline.fit_transform(train_features)
        joblib.dump(full_pipeline, f'{self.folder_path}/transformer_pipeline')

        print('Feature Encoding Completed and Transformer Pipeline Saved')
        return training_features

    def train_test_data(self, feature, label):
        print('Splitting Data into Test and Train datasets')
        X_train, X_test, y_train, y_test = train_test_split(feature, label, test_size=0.2, random_state=42)
        return X_train, X_test, y_train, y_test

    def train_model(self, model_type, X_train, y_train):
        print('Model Training Started')

        # Use the provided parameters or fall back to default values
        time_left_for_this_task = self.time_left_for_this_task or (30 * 60 if model_type == 'classifier' else 15 * 60)
        per_run_time_limit = self.per_run_time_limit or (6 * 60 if model_type == 'classifier' else 4 * 60)
        ensemble_size = self.ensemble_size or 5
        n_jobs = self.n_jobs or 8

        if model_type == 'classifier':
            automl_model = AutoSklearnClassifier(
                time_left_for_this_task=time_left_for_this_task,
                per_run_time_limit=per_run_time_limit,
                ensemble_kwargs={"ensemble_size": ensemble_size},
                n_jobs=n_jobs,
                scoring_functions=[roc_auc, average_precision, accuracy, f1, precision, recall, log_loss]
            )
        else:
            automl_model = AutoSklearnRegressor(
                time_left_for_this_task=time_left_for_this_task,
                per_run_time_limit=per_run_time_limit,
                ensemble_kwargs={"ensemble_size": ensemble_size},
                n_jobs=n_jobs
            )

        automl_model.fit(X_train, y_train)
        print('Model Training Completed')
        return automl_model

    def save_model(self, model, model_type):
        now = datetime.now().strftime('%Y%m%d%H%M%S')
        file_name = f'automl_{model_type}_{now}'
        joblib.dump(model, f'{self.folder_path}/{file_name}')
        print(f'{model_type.capitalize()} model saved - {file_name}')
        self.file_name = file_name
