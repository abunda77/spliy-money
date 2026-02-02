"""
GUI components untuk Money Splitter menggunakan CustomTkinter
"""

import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk
from typing import Optional

from .models import SplitResult
from .splitter import MoneySplitter
from .utils import CurrencyFormatter, ValidationUtils


class MoneySpitterGUI:
    """Main GUI class untuk Money Splitter application"""
    
    def __init__(self):
        # Setup Theme
        ctk.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
        ctk.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"
        
        self.root = ctk.CTk()
        self.splitter = MoneySplitter()
        self.selected_parts = ctk.IntVar(value=3)  # Default 3 bagian
        
        self.result_frames = [] # Keep track of result frames
        
        self.setup_ui()
    
    def setup_ui(self):
        """Setup antarmuka pengguna yang modern"""
        # Setup main window
        self.root.title("Money Splitter Pro")
        self.root.geometry("700x650") # Slightly larger for better spacing
        self.root.minsize(600, 500)
        
        # Grid configuration for responsiveness
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=1) # Results expand
        
        # --- Context 1: Header & Input Section ---
        self.main_frame = ctk.CTkFrame(self.root, corner_radius=15, fg_color="transparent")
        self.main_frame.grid(row=0, column=0, padx=20, pady=20, sticky="ew")
        self.main_frame.grid_columnconfigure(0, weight=1)

        # Title
        self.title_label = ctk.CTkLabel(
            self.main_frame, 
            text="Money Splitter", 
            font=ctk.CTkFont(family="Roboto", size=28, weight="bold")
        )
        self.title_label.grid(row=0, column=0, pady=(10, 5))
        
        self.subtitle_label = ctk.CTkLabel(
            self.main_frame,
            text="Bagi uang secara natural dan profesional",
            font=ctk.CTkFont(family="Roboto", size=14),
            text_color="gray"
        )
        self.subtitle_label.grid(row=1, column=0, pady=(0, 20))
        
        # Input Card
        self.input_card = ctk.CTkFrame(self.main_frame, corner_radius=10)
        self.input_card.grid(row=2, column=0, sticky="ew", padx=10)
        self.input_card.grid_columnconfigure(0, weight=1)
        
        # Amount Input
        self.amount_label = ctk.CTkLabel(self.input_card, text="Jumlah Uang (Rp)", font=ctk.CTkFont(size=12, weight="bold"))
        self.amount_label.grid(row=0, column=0, padx=20, pady=(20, 5), sticky="w")
        
        self.amount_entry = ctk.CTkEntry(
            self.input_card, 
            placeholder_text="Contoh: 1.000.000",
            height=40,
            font=ctk.CTkFont(size=16)
        )
        self.amount_entry.grid(row=1, column=0, padx=20, pady=(0, 5), sticky="ew")
        self.amount_entry.bind('<Return>', lambda event: self.on_split_button_click())
        
        # Parts Selection
        self.parts_label = ctk.CTkLabel(self.input_card, text="Jumlah Bagian", font=ctk.CTkFont(size=12, weight="bold"))
        self.parts_label.grid(row=2, column=0, padx=20, pady=(15, 5), sticky="w")
        
        self.parts_segmented = ctk.CTkSegmentedButton(
            self.input_card,
            values=["2", "3", "4", "5", "6"],
            variable=self.selected_parts,
            height=35,
            dynamic_resizing=True
        )
        self.parts_segmented.grid(row=3, column=0, padx=20, pady=(0, 20), sticky="ew")

        # Action Button
        self.split_button = ctk.CTkButton(
            self.main_frame,
            text="BAGI UANG SEKARANG",
            command=self.on_split_button_click,
            height=50,
            font=ctk.CTkFont(size=16, weight="bold"),
            corner_radius=25
        )
        self.split_button.grid(row=3, column=0, pady=20, padx=10, sticky="ew")

        # --- Context 2: Results Section ---
        self.results_container = ctk.CTkFrame(self.root, corner_radius=15) # Container with background
        self.results_container.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="nsew")
        self.results_container.grid_columnconfigure(0, weight=1)
        self.results_container.grid_rowconfigure(1, weight=1)
        
        # Results Header
        self.results_header = ctk.CTkLabel(
            self.results_container, 
            text="Hasil Pembagian", 
            font=ctk.CTkFont(size=18, weight="bold")
        )
        self.results_header.grid(row=0, column=0, padx=20, pady=15, sticky="w")
        
        # Scrollable Frame for Result Items
        self.results_scroll = ctk.CTkScrollableFrame(self.results_container, fg_color="transparent")
        self.results_scroll.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="nsew")
        self.results_scroll.grid_columnconfigure(0, weight=1)
        
        # Summary & Footer
        self.footer_frame = ctk.CTkFrame(self.results_container, fg_color="transparent")
        self.footer_frame.grid(row=2, column=0, padx=20, pady=10, sticky="ew")
        
        self.total_label = ctk.CTkLabel(
            self.footer_frame, 
            text="Total: -",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        self.total_label.pack(side="right")
        
        self.status_label = ctk.CTkLabel(
            self.footer_frame,
            text="Siap",
            text_color="gray",
            font=ctk.CTkFont(size=12)
        )
        self.status_label.pack(side="left")

    def on_split_button_click(self):
        """Handle split button click event"""
        try:
            self.status_label.configure(text="Memproses...", text_color="orange")
            self.root.update()
            
            # Clear previous
            self.clear_results()
            
            # Get input
            input_text = self.amount_entry.get()
            amount = CurrencyFormatter.parse_input(input_text)
            
            if amount is None:
                self.show_error(ValidationUtils.get_error_message("invalid_format"))
                self.status_label.configure(text="Error Input", text_color="red")
                return
            
            # Perform split
            num_parts = self.selected_parts.get()
            result = self.splitter.split_money(amount, num_parts)
            self.display_results(result)
            
            self.status_label.configure(text=f"Sukses! Dibagi menjadi {num_parts} bagian.", text_color="green")
            
        except ValueError as e:
            self.show_error(str(e))
            self.status_label.configure(text="Validasi Gagal", text_color="red")
        except Exception as e:
            self.show_error(ValidationUtils.get_error_message("processing_error") + f"\n{e}")
            self.status_label.configure(text="Error Internal", text_color="red")

    def clear_results(self):
        """Clear previous results"""
        for frame in self.result_frames:
            frame.destroy()
        self.result_frames = []
        self.total_label.configure(text="Total: -")

    def display_results(self, result: SplitResult):
        """Display split results cards"""
        percentages = result.get_percentages()
        
        for i, (split, percentage) in enumerate(zip(result.splits, percentages)):
            self.create_result_card(i + 1, split, percentage)
            
        # Update total
        total_formatted = CurrencyFormatter.format_rupiah(result.get_total())
        self.total_label.configure(text=f"Total: {total_formatted}")

    def create_result_card(self, index, amount, percentage):
        """Create a single result row card with Copy button"""
        card = ctk.CTkFrame(self.results_scroll, corner_radius=10, fg_color=("gray90", "gray20"))
        card.grid(row=len(self.result_frames), column=0, padx=5, pady=5, sticky="ew")
        card.grid_columnconfigure(1, weight=1) # Middle expands
        
        # Index Bubble
        index_label = ctk.CTkLabel(
            card, 
            text=str(index), 
            width=30, 
            height=30, 
            corner_radius=15,
            fg_color=("gray80", "gray30"),
            font=ctk.CTkFont(weight="bold")
        )
        index_label.grid(row=0, column=0, padx=10, pady=10)
        
        # Amount & Percentage
        info_frame = ctk.CTkFrame(card, fg_color="transparent")
        info_frame.grid(row=0, column=1, padx=10, sticky="w")
        
        amount_text = CurrencyFormatter.format_rupiah(amount)
        amount_label = ctk.CTkLabel(
            info_frame, 
            text=amount_text, 
            font=ctk.CTkFont(size=16, weight="bold")
        )
        amount_label.pack(anchor="w")
        
        perc_label = ctk.CTkLabel(
            info_frame, 
            text=f"{percentage:.1f}% dari total", 
            font=ctk.CTkFont(size=12),
            text_color="gray"
        )
        perc_label.pack(anchor="w")
        
        # Copy Button
        copy_btn = ctk.CTkButton(
            card,
            text="Salin",
            width=60,
            height=30,
            font=ctk.CTkFont(size=12),
            fg_color="transparent",
            border_width=1,
            border_color=("gray60", "gray50"),
            text_color=("gray10", "gray90"),
            hover_color=("gray80", "gray30"),
            command=lambda v=amount, b=None: self.copy_to_clipboard(v) 
        )
        # Hack to pass button reference if we wanted to change text temporarily, but let's keep it simple first
        copy_btn.configure(command=lambda v=amount, b=copy_btn: self.copy_to_clipboard(v, b))
        copy_btn.grid(row=0, column=2, padx=15, pady=10)
        
        self.result_frames.append(card)

    def copy_to_clipboard(self, value, btn_widget=None):
        """Copy value (number) to clipboard"""
        self.root.clipboard_clear()
        self.root.clipboard_append(str(value))
        self.root.update() # Required for clipboard
        
        if btn_widget:
            original_text = btn_widget.cget("text")
            btn_widget.configure(text="Disalin!", fg_color=("green", "green"), text_color="white")
            self.root.after(1000, lambda: btn_widget.configure(text=original_text, fg_color="transparent", text_color=("gray10", "gray90")))

    def show_error(self, message: str):
        """Display error messages"""
        messagebox.showerror("Error", message)

    def run(self):
        """Start the GUI application"""
        self.root.mainloop()

if __name__ == "__main__":
    app = MoneySpitterGUI()
    app.run()