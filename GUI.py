import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from stock_analysis import StockAnalysis  # Import the StockAnalysis class from your analysis module

class StockAnalysisGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Stock Analysis Tool")

        self.label = ttk.Label(master, text="Select a company:")
        self.label.grid(row=0, column=0, padx=10, pady=5)

        self.combo = ttk.Combobox(master, state="readonly", width=30)
        self.combo.grid(row=0, column=1, padx=10, pady=5)

        self.analyze_button = ttk.Button(master, text="Analyze", command=self.analyze_company)
        self.analyze_button.grid(row=1, column=0, columnspan=2, padx=10, pady=5)

        self.stock_data_paths = ["company1.csv", "company2.csv"]  # Replace with actual file paths
        self.combo['values'] = [f"Company {i+1}" for i in range(len(self.stock_data_paths))]

    def analyze_company(self):
        company_index = self.combo.current()
        if company_index == -1:
            messagebox.showerror("Error", "Please select a company.")
            return

        analyzer = StockAnalysis([self.stock_data_paths[company_index]])
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
