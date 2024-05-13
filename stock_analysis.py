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
    dfs (list): A list to store dataframes for each company.
    models (list): A list to store trained models for each company.
    """

    def __init__(self, stock_data_paths):
        """
        Initialize StockAnalysis object with a list of stock data paths.

        Args:
        stock_data_paths (list): A list of paths to CSV files containing historical stock market data.
        """
        self.stock_data_paths = stock_data_paths
        self.dfs = []
        self.models = []

    def collect_data(self):
        """
        Read data for each company from CSV files and store in dataframes.
        """
        for path in self.stock_data_paths:
            df = pd.read_csv(path)
            required_headers = [
                "Company Name", "Series", "OPEN", "HIGH", "LOW", "CLOSE", "LAST",
                "PREVCLOSE", "TOTTRDQTY", "TOTTRDVAL", "TIMESTAMP", "TOTALTRADES",
                "ISIN", "Current Price", "S3", "S2", "S1", "Pivot", "R1", "R2", "R3"
            ]
            if all(header in df.columns for header in required_headers):
                self.dfs.append(df)
            else:
                print(f"CSV file '{path}' is missing required headers. Skipping...")

    def preprocess_data(self):
        """
        Perform comprehensive preprocessing on the data.

        This method performs various preprocessing steps including handling missing values,
        encoding categorical variables, feature engineering, scaling, handling outliers,
        and preparing the data for modeling.
        """
        for df in self.dfs:
            # Select only numeric columns for median calculation
            numeric_cols = df.select_dtypes(include=np.number).columns
            df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].median())  # Impute missing values with column medians

            self.encode_categorical(df)

            df['MA_5'] = df['CLOSE'].rolling(window=5).mean()

            # Scale numeric columns between 0 and 1
            df[numeric_cols] = (df[numeric_cols] - df[numeric_cols].min()) /(df[numeric_cols].max() - df[numeric_cols].min())

            # Clip outliers
            df[numeric_cols] = df[numeric_cols].apply(lambda x: np.clip(
                x,
                x.quantile(0.25) - 1.5 * (x.quantile(0.75) - x.quantile(0.25)),
                x.quantile(0.75) + 1.5 * (x.quantile(0.75) - x.quantile(0.25))
            ))

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
        self.models = [RandomForestRegressor(n_estimators=100, random_state=42).fit(
            df[['MA_5']], df['CLOSE']) for df in self.dfs]

    def evaluate_models(self):
        """
        Evaluate the performance of each model.
        """
        for df, model in zip(self.dfs, self.models):
            x_test, y_test = df[['MA_5']].values, df['CLOSE'].values
            predictions = model.predict(x_test)
            mse = mean_squared_error(y_test, predictions)
            print("Mean Squared Error:", mse)

    def buy_or_sell(self, threshold=0.05):
        """
        Make buying or selling decisions based on predicted future prices.

        Args:
        threshold (float): A threshold for price change percentage to trigger buying or selling. Default is 0.05 (5%).

        Returns:
        dict: A dictionary containing buying or selling decisions for each company.
        """
        decisions = {}
        for i, df in enumerate(self.dfs):
            company_name = df["Company Name"].iloc[0]
            current_price = df["CLOSE"].iloc[-1]
            future_price = self.models[i].predict(df[["MA_5"]].iloc[[-1]])[0]

            price_change = (future_price - current_price) / current_price
            if abs(price_change) >= threshold:
                decision = "Buy" if price_change > 0 else "Sell"
            else:
                decision = "Hold"

            decisions[company_name] = {
                "Current Price": current_price,
                "Future Price": future_price,
                "Price Change": price_change,
                "Decision": decision
            }
        return decisions

    def execute_trades(self):
        """
        Execute buy or sell trades based on the decisions.

        Returns:
        dict: A dictionary containing executed trades for each company.
        """
        trades = {}
        for company, decision_data in self.buy_or_sell().items():
            decision = decision_data["Decision"]
            current_price = decision_data["Current Price"]
            future_price = decision_data["Future Price"]

            if decision == "Buy":
                # Execute buy trade
                trades[company] = {
                    "Action": "Buy",
                    "Price": current_price,
                    "Future Price": future_price
                }
                # You can add your trading logic here, such as placing a buy order.
            elif decision == "Sell":
                # Execute sell trade
                trades[company] = {
                    "Action": "Sell",
                    "Price": current_price,
                    "Future Price": future_price
                }
                # You can add your trading logic here, such as placing a sell order.
        return trades
