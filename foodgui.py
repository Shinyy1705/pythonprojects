import customtkinter as ctk
from tkinter import Listbox, messagebox
import csv
import os

try:
    import pyperclip
    CLIPBOARD_AVAILABLE = True
except ImportError:
    CLIPBOARD_AVAILABLE = False

# CustomTkinter GUI Application
class FoodApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Window settings
        self.title("Food Manager")
        self.geometry("550x350")
        ctk.set_appearance_mode("dark")  # Light or dark mode
        ctk.set_default_color_theme("blue")  # Options: "blue", "green", "dark-blue"

        # Grid layout configuration
        self.grid_columnconfigure(0, weight=1)  # Left side (Inputs)
        self.grid_columnconfigure(1, weight=1)  # Right side (Buttons)

        # Labels & Entry fields (LEFT SIDE)
        ctk.CTkLabel(self, text="Category:").grid(row=0, column=0, sticky="w", padx=10, pady=5)
        self.category_entry = ctk.CTkEntry(self)
        self.category_entry.grid(row=0, column=1, sticky="we", padx=10, pady=5)

        ctk.CTkLabel(self, text="Food Name:").grid(row=1, column=0, sticky="w", padx=10, pady=5)
        self.food_entry = ctk.CTkEntry(self)
        self.food_entry.grid(row=1, column=1, sticky="we", padx=10, pady=5)

        ctk.CTkLabel(self, text="Food URL:").grid(row=2, column=0, sticky="w", padx=10, pady=5)
        self.url_entry = ctk.CTkEntry(self)
        self.url_entry.grid(row=2, column=1, sticky="we", padx=10, pady=5)

        # Buttons (RIGHT SIDE)
        ctk.CTkButton(self, text="Add Food", command=self.add_food).grid(row=0, column=2, padx=10, pady=5)
        ctk.CTkButton(self, text="List Foods", command=self.list_items).grid(row=1, column=2, padx=10, pady=5)
        ctk.CTkButton(self, text="Delete Food", command=self.delete_food).grid(row=2, column=2, padx=10, pady=5)

        # Listbox Container (Frame)
        self.list_frame = ctk.CTkFrame(self)
        self.list_frame.grid(row=4, column=0, columnspan=3, sticky="we", padx=10, pady=10)

        # Tkinter Listbox (For Clickable Rows)
        self.listbox = Listbox(self.list_frame, height=8, selectmode="single", bg="#2b2b2b", fg="white", relief="flat")
        self.listbox.pack(fill="both", expand=True)

        # Bind click event to copy URL
        self.listbox.bind("<Double-Button-1>", self.copy_food)

    def add_food(self):
        category = self.category_entry.get().capitalize().strip()
        food_name = self.food_entry.get().capitalize().strip()
        food_url = self.url_entry.get().strip().lower()

        if not category or not food_name or not food_url:
            messagebox.showerror("Error", "All fields are required!")
            return

        with open("foodlinks.csv", mode="a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([category, food_name, food_url])

        messagebox.showinfo("Success", f"Added {food_name} under {category}.")
        self.clear_entries()
        self.list_items()

    def list_items(self):
        self.listbox.delete(0, "end")

        if not os.path.exists("foodlinks.csv"):
            messagebox.showerror("Error", "No data found!")
            return

        with open("foodlinks.csv", mode="r") as file:
            reader = csv.reader(file)
            for row in reader:
                if len(row) == 3:
                    category, food_name, food_url = row
                    self.listbox.insert("end", f"{category} - {food_name} ({food_url})")

    def delete_food(self):
        selected_index = self.listbox.curselection()
        if not selected_index:
            messagebox.showerror("Error", "Please select a food item to delete.")
            return

        selected_text = self.listbox.get(selected_index)
        food_name = selected_text.split(" - ")[1].split(" (")[0]

        if not os.path.exists("foodlinks.csv"):
            messagebox.showerror("Error", "No file found!")
            return

        with open("foodlinks.csv", mode="r") as file:
            reader = csv.reader(file)
            rows = list(reader)

        updated_rows = [row for row in rows if row[1] != food_name]

        with open("foodlinks.csv", mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerows(updated_rows)

        messagebox.showinfo("Success", f"Deleted {food_name}.")
        self.list_items()

    def copy_food(self, event=None):
        selected_index = self.listbox.curselection()
        if not selected_index:
            messagebox.showerror("Error", "Please select a food item to copy.")
            return

        selected_text = self.listbox.get(selected_index)
        food_url = selected_text.rpartition(" (")[2].rstrip(")")

        if CLIPBOARD_AVAILABLE:
            pyperclip.copy(food_url)
            messagebox.showinfo("Success", f"Copied {food_url} to clipboard!")
        else:
            messagebox.showerror("Error", "Clipboard not available.")

    def clear_entries(self):
        """ Clears input fields """
        self.category_entry.delete(0, ctk.END)
        self.food_entry.delete(0, ctk.END)
        self.url_entry.delete(0, ctk.END)

# Run the CustomTkinter application
if __name__ == "__main__":
    app = FoodApp()
    app.mainloop()
