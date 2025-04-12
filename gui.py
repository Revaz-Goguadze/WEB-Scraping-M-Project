"""
gui.py
Improved GUI for viewing scraped book data with matplotlib charts.

Enhancements:
- Added menu bar (with Refresh Data, About, and Quit)
- Improved summary section formatting
- Added scrollbar to book list
- Ensured price formatting with currency symbol
- Added keyboard shortcut (Ctrl+Q to quit)
- Added inline comments, clearer tab/window names, better code organization
- Improved error handling for empty data/chart edge case
"""

import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import json
from utils.analyzer import count_books_per_category, average_price_per_category, get_unavailable_books
from models.data_models import Book

class ScraperGUI(tk.Tk):
    """
    Main window for the book scraper data viewer.
    Enhanced for usability, accessibility, and code clarity.
    """
    def __init__(self, json_path="data/books.json"):
        super().__init__()
        self.title("Book Scraper Data Viewer (Improved)")
        self.geometry("850x630")
        self.books = self.load_books(json_path)
        self.json_path = json_path

        self.create_menu()
        self.create_widgets()
        self.create_charts()

        self.bind_all("<Control-q>", lambda e: self.quit())  # Ctrl+Q to quit

    def load_books(self, json_path):
        """
        Load book data from json_path into Book objects.
        """
        try:
            with open(json_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            return sorted([Book(**item) for item in data], key=lambda b: b.title)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load data: {e}")
            return []

    def create_menu(self):
        """
        Add a menu bar with refresh and about options.
        """
        menubar = tk.Menu(self)
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Refresh Data", command=self.refresh_data, accelerator="Ctrl+R")
        file_menu.add_command(label="Quit", command=self.quit, accelerator="Ctrl+Q")
        menubar.add_cascade(label="File", menu=file_menu)

        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="About", command=self.show_about)
        menubar.add_cascade(label="Help", menu=help_menu)

        self.config(menu=menubar)
        self.bind_all("<Control-r>", lambda e: self.refresh_data())

    def refresh_data(self):
        """
        Reload book data and refresh widgets/charts.
        """
        self.books = self.load_books(self.json_path)
        for child in self.winfo_children():
            if isinstance(child, ttk.Notebook):
                child.destroy()
        self.create_widgets()
        self.create_charts()

    def show_about(self):
        """
        Show an about dialog.
        """
        messagebox.showinfo("About", "Book Scraper Data Viewer\nImproved version\nGUI built with Tkinter and matplotlib.")

    def create_widgets(self):
        """
        Construct GUI widgets (tabs, lists, summary, charts).
        """
        tabs = ttk.Notebook(self)
        tabs.pack(fill=tk.BOTH, expand=1)

        tab1 = ttk.Frame(tabs)
        tab2 = ttk.Frame(tabs)
        tabs.add(tab1, text="Book List")
        tabs.add(tab2, text="Visual Charts")

        # Book list with scrollbar
        columns = ("Title", "Price", "Category", "Availability")
        tree_frame = ttk.Frame(tab1)
        tree_frame.pack(fill=tk.BOTH, expand=1)
        tree_scroll = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL)
        tree = ttk.Treeview(tree_frame, columns=columns, show="headings", yscrollcommand=tree_scroll.set)
        tree_scroll.config(command=tree.yview)
        tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, anchor="center")

        for book in self.books:
            # Ensure price is formatted even if loaded as a string
            try:
                price_val = float(book.price)
                price_display = f"£{price_val:.2f}"
            except (ValueError, TypeError):
                price_display = f"{book.price}"
            tree.insert("", tk.END, values=(
                book.title,
                price_display,
                book.category,
                book.availability
            ))

        # Text summaries with bold headers
        summary = tk.Text(tab1, height=10, font=('TkDefaultFont', 10))
        summary.pack(fill=tk.X, pady=(4, 2))
        summary.insert(tk.END, "== Category Counts ==\n")
        for k, v in count_books_per_category(self.books).items():
            summary.insert(tk.END, f"  {k}: {v}\n")
        summary.insert(tk.END, "\n== Average Price per Category ==\n")
        for k, v in average_price_per_category(self.books).items():
            summary.insert(tk.END, f"  {k}: £{v:.2f}\n")
        summary.insert(tk.END, "\n== Unavailable Books ==\n")
        unavailable = list(get_unavailable_books(self.books))
        if unavailable:
            for book in unavailable:
                summary.insert(tk.END, f"  {book.title}\n")
        else:
            summary.insert(tk.END, "  (None)\n")

        summary.configure(state=tk.DISABLED)

        # Charts tab placeholder - chart frame
        self.chart_frame = ttk.Frame(tab2)
        self.chart_frame.pack(fill=tk.BOTH, expand=1)

    def create_charts(self):
        """
        Render bar charts for book counts and price averages.
        """
        if not self.books:
            lbl = ttk.Label(self.chart_frame, text="No book data available for charts.", foreground="red")
            lbl.pack(pady=30)
            return

        counts = count_books_per_category(self.books)
        prices = average_price_per_category(self.books)

        fig, axs = plt.subplots(1, 2, figsize=(9, 4))
        fig.suptitle("Scraped Book Data Summary", fontsize=14)

        # Process data for charts
        count_categories = list(counts.keys())
        count_values = list(counts.values())
        price_categories = list(prices.keys())
        price_values = list(prices.values())

        # Book count per category
        count_positions = range(len(count_categories))
        axs[0].bar(count_positions, count_values, color="skyblue")
        axs[0].set_title("Books per Category")
        axs[0].set_xticks(count_positions)  # Set tick positions first
        axs[0].set_xticklabels(count_categories, rotation=45, ha='right')

        # Average price per category
        price_positions = range(len(price_categories))
        axs[1].bar(price_positions, price_values, color="orange")
        axs[1].set_title("Average Price (£)")
        axs[1].set_xticks(price_positions)  # Set tick positions first
        axs[1].set_xticklabels(price_categories, rotation=45, ha='right')

        plt.tight_layout()
        canvas = FigureCanvasTkAgg(fig, master=self.chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=1)

if __name__ == "__main__":
    app = ScraperGUI()
    app.mainloop()