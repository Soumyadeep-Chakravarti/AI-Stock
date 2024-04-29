"""
module: stock_analysis

This module provides a class for performing analysis on stock market data.

Classes:
    StockAnalysis: A class for performing analysis on stock market data.

Example usage:
    if __name__ == "__main__":
        stock_data_paths = ["company1.csv", "company2.csv"]
        resistance_points = [[10, 20, 30], [15, 25, 35]]
        support_points = [[5, 15, 25], [8, 18, 28]]

        analyzer = StockAnalysis(stock_data_paths, resistance_points, support_points)
        analyzer.collect_data()
        analyzer.preprocess_data()
        analyzer.build_models()
        analyzer.evaluate_models()
        new_data = [...]  # New data for prediction
        predictions = analyzer.predict_future_prices(new_data)
"""

import pandas as pd
import numpy as np
import logger as log
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import mean_squared_error

class StockAnalysis:
    """
    A class to perform analysis on stock market data.

    Attributes:
    stock_data_paths (list): A list of paths to CSV files containing historical stock market data for different companies.
    resistance_points (list): A list of lists containing resistance points for each company.
    support_points (list): A list of lists containing support points for each company.
    dfs (list): A list to store dataframes for each company.
    models (list): A list to store trained models for each company.
    """

    def __init__(self, stock_data_paths, resistance_points=None, support_points=None):
        """
        Initialize StockAnalysis object with a list of stock data paths.

        Args:
        stock_data_paths (list): A list of paths to CSV files containing historical stock market data.
        resistance_points (list): A list of lists containing resistance points for each company.
        support_points (list): A list of lists containing support points for each company.
        """
        self.stock_data_paths = stock_data_paths
        self.resistance_points = resistance_points
        self.support_points = support_points
        self.dfs = []
        self.models = []
        self.logger = log.Logger()  # Initialize logger object

    def collect_data(self):
        """
        Read data for each company from CSV files and store in dataframes.
        """
        for path in self.stock_data_paths:
            df = pd.read_csv(path)
            self.dfs.append(df)

    def preprocess_data(self):
        """
        Perform comprehensive preprocessing on the data.

        This method performs various preprocessing steps including handling missing values,
        encoding categorical variables, feature engineering, scaling, handling outliers,
        and preparing the data for modeling.
        """
        for df_index, df in enumerate(self.dfs):
            self.logger.log(f"Preprocessing data for DataFrame {df_index + 1}")
            # Handle missing values
            df.fillna(df.median(), inplace=True)  # Impute missing values with median
            self.logger.log("Missing values handled")

            # Encode categorical variables
            self.encode_categorical(df)
            self.logger.log("Categorical variables encoded")

            # Feature engineering
            df['MA_5'] = df['Close'].rolling(window=5).mean()  # Moving average of 5 days
            self.logger.log("Feature engineering completed")

            # Add resistance and support points
            if self.resistance_points and self.support_points:
                df['Resistance1'] = self.resistance_points[df_index][0]
                df['Resistance2'] = self.resistance_points[df_index][1]
                df['Resistance3'] = self.resistance_points[df_index][2]
                df['Support1'] = self.support_points[df_index][0]
                df['Support2'] = self.support_points[df_index][1]
                df['Support3'] = self.support_points[df_index][2]
                self.logger.log("Resistance and support points added")

            # Scale numeric features using Min-Max scaling
            numeric_cols = df.select_dtypes(include=np.number).columns
            df[numeric_cols] = (df[numeric_cols] - df[numeric_cols].min()) / \
                               (df[numeric_cols].max() - df[numeric_cols].min())
            self.logger.log("Numeric features scaled")

            # Handle outliers
            self.handle_outliers(df)
            self.logger.log("Outliers handled")

            # Data cleaning (optional)
            # Example: df.drop_duplicates(inplace=True)
            self.logger.log("Data cleaning completed (if any)")

    def encode_categorical(self, df):
        """
        Encode categorical variables in the DataFrame.

        Args:
        df (DataFrame): DataFrame containing historical stock market data.
        """
        categorical_cols = df.select_dtypes(include=['object']).columns
        label_encoders = {}
        for col in categorical_cols:
            label_encoders[col] = LabelEncoder()
            df[col] = label_encoders[col].fit_transform(df[col])

    def handle_outliers(self, df):
        """
        Handle outliers in the DataFrame.

        Args:
        df (DataFrame): DataFrame containing historical stock market data.
        """
        numeric_cols = df.select_dtypes(include=np.number).columns
        for col in numeric_cols:
            q1 = df[col].quantile(0.25)
            q3 = df[col].quantile(0.75)
            iqr = q3 - q1
            lower_bound = q1 - 1.5 * iqr
            upper_bound = q3 + 1.5 * iqr
            df[col] = np.clip(df[col], lower_bound, upper_bound)

    def engineer_features(self):
        """
        Engineer features for each company's data.
        """
        for df in self.dfs:
            df['MA_5'] = df['Close'].rolling(window=5).mean()

    def build_models(self):
        """
        Train a separate model for each company.
        """
        for df in self.dfs:
            X = df[['MA_5']].values
            y = df['Close'].values

            X_train, _, y_train, _ = train_test_split(X, y, test_size=0.2, random_state=42)

            model = RandomForestRegressor(n_estimators=100, random_state=42)
            model.fit(X_train, y_train)

            self.models.append(model)

    def evaluate_models(self):
        """
        Evaluate the performance of each model.
        """
        for df, model in zip(self.dfs, self.models):
            X_test = df[['MA_5']].values
            y_test = df['Close'].values
            
            predictions = model.predict(X_test)
            mse = mean_squared_error(y_test, predictions)
            print("Mean Squared Error:", mse)

    def predict_future_prices(self, new_data):
        """
        Predict the future prices for each company.

        Args:
        new_data (list): A list of arrays containing new data for each company.

        Returns:
        list: A list of arrays containing predicted prices for each company.
        """
        predicted_prices = []
        for i, data in enumerate(new_data):
            predictions = self.models[i].predict(data)
            predicted_prices.append(predictions)
        return predicted_prices
