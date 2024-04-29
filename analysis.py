"""
Module: stock_analysis

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

    def collect_data(self):
        """
        Read data for each company from CSV files and store in dataframes.
        """
        for path in self.stock_data_paths:
            df = pd.read_csv(path, usecols=[
                                                "Series", 
                                                "OPEN",
                                                "HIGH",
                                                "LOW",
                                                "CLOSE",
                                                "LAST",
                                                "PREVCLOSE",
                                                "TOTTRDQTY",
                                                "TOTTRDVAL",
                                                "TIMESTAMP",
                                                "TOTALTRADES",
                                                "ISIN",
                                                "Current Price",
                                                "S3",
                                                "S2",
                                                "S1",
                                                "Pivot",
                                                "R1",
                                                "R2",
                                                "R3"
                                            ]
                            )


            self.dfs.append(df)


    def preprocess_data(self):
        """
        Perform comprehensive preprocessing on the data.

        This method performs various preprocessing steps including handling missing values,
        encoding categorical variables, feature engineering, scaling, handling outliers,
        and preparing the data for modeling.
        """
        for df_index, df in enumerate(self.dfs):
            df.fillna(df.median(), inplace=True)  # Impute missing values with median

            self.encode_categorical(df)

            df['MA_5'] = df['Close'].rolling(window=5).mean()

            if self.resistance_points and self.support_points:
                rp, sp = self.resistance_points[df_index], self.support_points[df_index]
                df[['Resistance1', 'Resistance2', 'Resistance3']] = pd.DataFrame([rp], index=df.index)
                df[['Support1', 'Support2', 'Support3']] = pd.DataFrame([sp], index=df.index)

            numeric_cols = df.select_dtypes(include=np.number).columns.tolist()
            df[numeric_cols] = (df[numeric_cols] - df[numeric_cols].min()) / \
                               (df[numeric_cols].max() - df[numeric_cols].min())

            df[numeric_cols] = df[numeric_cols].apply(lambda x: np.clip(x, x.quantile(0.25) - 1.5 * (x.quantile(0.75) - x.quantile(0.25)),
                                                                         x.quantile(0.75) + 1.5 * (x.quantile(0.75) - x.quantile(0.25))))

    def encode_categorical(self, df):
        """
        Encode categorical variables in the DataFrame.

        Args:
        df (DataFrame): DataFrame containing historical stock market data.
        """
        categorical_cols = df.select_dtypes(include=['object']).columns
        label_encoders = {col: LabelEncoder() for col in categorical_cols}
        for col, le in label_encoders.items():
            df[col] = le.fit_transform(df[col])

    def build_models(self):
        """
        Train a separate model for each company.
        """
        self.models = [RandomForestRegressor(n_estimators=100, random_state=42).fit(*train_test_split(df[['MA_5']].values, df['Close'].values, test_size=0.2, random_state=42)) for df in self.dfs]

    def evaluate_models(self):
        """
        Evaluate the performance of each model.
        """
        for df, model in zip(self.dfs, self.models):
            x_test, y_test = df[['MA_5']].values, df['Close'].values
            predictions = model.predict(x_test)
            mse = mean_squared_error(y_test, predictions)#type:ignore
            print("Mean Squared Error:", mse)

    def predict_future_prices(self, new_data):
        """
        Predict the future prices for each company.

        Args:
        new_data (list): A list of arrays containing new data for each company.

        Returns:
        list: A list of arrays containing predicted prices for each company.
        """
        return [model.predict(data) for model, data in zip(self.models, new_data)]
