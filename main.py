#!/usr/bin/env python3
"""
Main entry point untuk Money Splitter application

Aplikasi ini membagi sejumlah uang menjadi 5 atau 6 bagian secara acak
dengan tampilan yang natural untuk keperluan transaksi tunai.
"""

import sys
import logging
import traceback
from pathlib import Path
from typing import Optional

from money_splitter.gui import MoneySpitterGUI


def setup_logging() -> None:
    """Setup logging configuration untuk aplikasi"""
    # Create logs directory if it doesn't exist
    logs_dir = Path("logs")
    logs_dir.mkdir(exist_ok=True)
    
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(logs_dir / "money_splitter.log"),
            logging.StreamHandler(sys.stdout)
        ]
    )


def check_dependencies() -> bool:
    """Check if all required dependencies are available"""
    try:
        import tkinter
        from money_splitter.gui import MoneySpitterGUI
        from money_splitter.splitter import MoneySplitter
        from money_splitter.utils import CurrencyFormatter, ValidationUtils
        from money_splitter.models import SplitResult
        return True
    except ImportError as e:
        logging.error(f"Missing dependency: {e}")
        print(f"Error: Missing required dependency - {e}")
        print("Please ensure all required modules are installed.")
        return False


def handle_exception(exc_type, exc_value, exc_traceback) -> None:
    """Global exception handler untuk uncaught exceptions"""
    if issubclass(exc_type, KeyboardInterrupt):
        # Handle Ctrl+C gracefully
        logging.info("Application interrupted by user")
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return
    
    # Log the exception
    logging.critical(
        "Uncaught exception",
        exc_info=(exc_type, exc_value, exc_traceback)
    )
    
    # Show user-friendly error message
    error_msg = (
        "Terjadi kesalahan yang tidak terduga dalam aplikasi.\n"
        "Silakan restart aplikasi atau hubungi support jika masalah berlanjut.\n\n"
        f"Error: {exc_value}"
    )
    
    try:
        import tkinter as tk
        from tkinter import messagebox
        
        # Create a temporary root window for the error dialog
        root = tk.Tk()
        root.withdraw()  # Hide the main window
        messagebox.showerror("Error Aplikasi", error_msg)
        root.destroy()
    except:
        # Fallback to console output if GUI is not available
        print(f"\nFATAL ERROR: {error_msg}")


def main() -> int:
    """
    Main function untuk menjalankan aplikasi
    
    Returns:
        int: Exit code (0 for success, 1 for error)
    """
    # Setup logging
    setup_logging()
    logger = logging.getLogger(__name__)
    
    # Set global exception handler
    sys.excepthook = handle_exception
    
    logger.info("Starting Money Splitter application")
    
    try:
        # Check dependencies
        if not check_dependencies():
            logger.error("Dependency check failed")
            return 1
        
        logger.info("All dependencies available")
        
        # Create and run the application
        logger.info("Initializing GUI application")
        app = MoneySpitterGUI()
        
        logger.info("Starting application main loop")
        app.run()
        
        logger.info("Application closed normally")
        return 0
        
    except KeyboardInterrupt:
        logger.info("Application interrupted by user (Ctrl+C)")
        return 0
        
    except Exception as e:
        logger.critical(f"Fatal error during application startup: {e}")
        logger.critical(traceback.format_exc())
        
        # Show error to user if possible
        error_msg = (
            f"Gagal memulai aplikasi Money Splitter.\n\n"
            f"Error: {str(e)}\n\n"
            f"Silakan periksa log file untuk detail lebih lanjut."
        )
        
        try:
            import tkinter as tk
            from tkinter import messagebox
            
            root = tk.Tk()
            root.withdraw()
            messagebox.showerror("Startup Error", error_msg)
            root.destroy()
        except:
            print(f"\nSTARTUP ERROR: {error_msg}")
        
        return 1


def cleanup() -> None:
    """Cleanup function yang dipanggil saat aplikasi akan ditutup"""
    logger = logging.getLogger(__name__)
    logger.info("Performing application cleanup")
    
    # Add any cleanup tasks here if needed
    # For example: closing database connections, saving state, etc.
    
    logger.info("Cleanup completed")


if __name__ == "__main__":
    try:
        exit_code = main()
        cleanup()
        sys.exit(exit_code)
    except SystemExit:
        # Handle sys.exit() calls
        cleanup()
        raise
    except:
        # Handle any other exceptions during cleanup
        logging.critical("Error during cleanup", exc_info=True)
        sys.exit(1)