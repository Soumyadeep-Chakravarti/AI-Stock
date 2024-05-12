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
    stock_data_paths (list): 
        A list of paths to CSV files containing historical stock market data for different companies.
    dfs (list): 
        A list to store dataframes for each company.
    models (list):
        A list to store trained models for each company.
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
            df.fillna(df.median(), inplace=True)  # Impute missing values with median

            self.encode_categorical(df)

            df['MA_5'] = df['CLOSE'].rolling(window=5).mean()

            numeric_cols = df.select_dtypes(include=np.number).columns.tolist()
            df[numeric_cols] = (df[numeric_cols] - df[numeric_cols].min()) /(df[numeric_cols].max() - df[numeric_cols].min())

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
            *train_test_split(df[['MA_5']].values, df['CLOSE'].values, test_size=0.2, random_state=42)) for df in self.dfs]

    def evaluate_models(self):
        """
        Evaluate the performance of each model.
        """
        for df, model in zip(self.dfs, self.models):
            x_test, y_test = df[['MA_5']].values, df['CLOSE'].values
            predictions = model.predict(x_test)
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
        return [model.predict(data) for model, data in zip(self.models, new_data)]

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

if __name__ == "__main__":
    stock_data_paths = ["company1.csv", "company2.csv"]
    analyzer = StockAnalysis(stock_data_paths)
    analyzer.collect_data()
    analyzer.preprocess_data()
    analyzer.build_models()
    analyzer.evaluate_models()

    # Make buying or selling decisions
    decisions = analyzer.buy_or_sell()
    for company, decision_data in decisions.items():
        print(f"Company: {company}")
        print(f"Current Price: {decision_data['Current Price']}")
        print(f"Future Price: {decision_data['Future Price']}")
        print(f"Price Change: {decision_data['Price Change']}")
        print(f"Decision: {decision_data['Decision']}")
        print()
