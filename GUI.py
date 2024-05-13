import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import imp_items
from stock_analysis import StockAnalysis

class StockAnalysisGUI:
    """
    StockAnalysisGUI: A class to create the GUI for the stock analysis tool.

    This class provides a graphical user interface (GUI) for the stock analysis tool using Tkinter. It allows users
    to search for a company by entering its name in a search bar and analyze it, displaying trade information in a
    message box.

    Attributes:
        master (Tk): The Tkinter root window.

    Methods:
        __init__(self, master): Initializes the GUI with labels, search bar, and analyze button.
        analyze_company(self): Performs analysis on the selected company and displays trade information.
    """

    def __init__(self, master):
        self.master = master
        self.master.title("Stock Analysis Tool")

        self.label = ttk.Label(master, text="Search for a company:")
        self.label.grid(row=0, column=0, padx=10, pady=5)

        self.search_entry = ttk.Entry(master, width=30)
        self.search_entry.grid(row=0, column=1, padx=10, pady=5)

        self.analyze_button = ttk.Button(master, text="Analyze", command=self.analyze_company)
        self.analyze_button.grid(row=1, column=0, columnspan=2, padx=10, pady=5)

        self.stock_data_paths = imp_items.find_csv_files("C:\\Users\\bunas\\ドキュメント\\stock_ai\\data\\company_wise_data")
        print(self.stock_data_paths)
        
    def analyze_company(self):
        company_name = self.search_entry.get().strip()
        if not company_name:
            messagebox.showerror("Error", "Please enter a company name.")
            return

        # Search for the company name in the CSV file paths
        matching_paths = [path for path in self.stock_data_paths if company_name.lower() in path.lower()]
        if not matching_paths:
            messagebox.showerror("Error", f"No CSV files found for company '{company_name}'.")
            return

        analyzer = StockAnalysis(matching_paths)
        analyzer.collect_data()
        analyzer.preprocess_data()
        analyzer.build_models()
        analyzer.evaluate_models()

        # Execute trades
        executed_trades = analyzer.execute_trades()
        trade_info = ""
        for company, trade_data in executed_trades.items():
            trade_info += f"Company: {company}\n"
            trade_info += f"Action: {trade_data['Action']}\n"
            trade_info += f"Price: {trade_data['Price']}\n"
            trade_info += f"Future Price: {trade_data['Future Price']}\n\n"

        messagebox.showinfo("Trade Information", trade_info)

def main():
    root = tk.Tk()
    app = StockAnalysisGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
