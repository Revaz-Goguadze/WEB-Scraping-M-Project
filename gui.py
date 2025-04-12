"""
gui.py
Modified GUI
Simple Tkinter GUI to display scraped book data with matplotlib charts.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import json
from utils.analyzer import count_books_per_category, average_price_per_category, get_unavailable_books
from models.data_models import Book


class ScraperGUI(tk.Tk):
    def __init__(self, json_path="data/books.json"):
        super().__init__()
        self.title("Book Scraper Data Viewer")
        self.geometry("800x600")
        self.books = self.load_books(json_path)

        self.create_widgets()
        self.create_charts()

    def load_books(self, json_path):
        try:
            with open(json_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            return [Book(**item) for item in data]
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load data: {e}")
            return []

    def create_widgets(self):
        tabs = ttk.Notebook(self)
        tabs.pack(fill=tk.BOTH, expand=1)

        tab1 = ttk.Frame(tabs)
        tab2 = ttk.Frame(tabs)
        tabs.add(tab1, text="Books")
        tabs.add(tab2, text="Charts")

        # Book list
        columns = ("Title", "Price", "Category", "Availability")
        tree = ttk.Treeview(tab1, columns=columns, show="headings")
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, anchor="center")
        for book in self.books:
            tree.insert("", tk.END, values=(book.title, book.price, book.category, book.availability))
        tree.pack(fill=tk.BOTH, expand=1)

        # Text summaries
        summary = tk.Text(tab1, height=8)
        summary.pack(fill=tk.X)
        summary.insert(tk.END, "Category Counts:\n")
        for k, v in count_books_per_category(self.books).items():
            summary.insert(tk.END, f"{k}: {v}\n")
        summary.insert(tk.END, "\nAverage Price per Category:\n")
        for k, v in average_price_per_category(self.books).items():
            summary.insert(tk.END, f"{k}: £{v:.2f}\n")
        summary.insert(tk.END, "\nUnavailable Books:\n")
        for book in get_unavailable_books(self.books):
            summary.insert(tk.END, f"{book.title}\n")

        summary.configure(state=tk.DISABLED)

        # Charts tab placeholder - filled in next method
        self.chart_frame = ttk.Frame(tab2)
        self.chart_frame.pack(fill=tk.BOTH, expand=1)

    def create_charts(self):
        counts = count_books_per_category(self.books)
        prices = average_price_per_category(self.books)

        fig, axs = plt.subplots(1, 2, figsize=(8, 4))
        fig.suptitle("Scraped Book Data Summary")

        # Book count per category
        axs[0].bar(counts.keys(), counts.values(), color="skyblue")
        axs[0].set_title("Books per Category")
        axs[0].set_xticklabels(counts.keys(), rotation=45, ha='right')

        # Average price per category
        axs[1].bar(prices.keys(), prices.values(), color="orange")
        axs[1].set_title("Average Price (£)")
        axs[1].set_xticklabels(prices.keys(), rotation=45, ha='right')

        plt.tight_layout()

        canvas = FigureCanvasTkAgg(fig, master=self.chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=1)


if __name__ == "__main__":
    app = ScraperGUI()
    app.mainloop()