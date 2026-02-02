"""
Utility functions untuk Money Splitter application
"""

import re
from typing import Optional


class CurrencyFormatter:
    """Utility class untuk formatting mata uang Indonesia"""
    
    @staticmethod
    def format_rupiah(amount: int) -> str:
        """
        Format amount sebagai Rupiah Indonesia dengan pemisah ribuan yang konsisten.
        
        Args:
            amount: Jumlah dalam integer (dalam Rupiah)
            
        Returns:
            String dengan format "Rp X.XXX.XXX" menggunakan titik sebagai pemisah ribuan
            
        Examples:
            >>> CurrencyFormatter.format_rupiah(1000000)
            'Rp 1.000.000'
            >>> CurrencyFormatter.format_rupiah(1500000)
            'Rp 1.500.000'
        """
        if not isinstance(amount, int):
            raise TypeError("Amount harus berupa integer")
        
        # Handle negative numbers
        if amount < 0:
            formatted = f"{abs(amount):,}".replace(",", ".")
            return f"Rp -{formatted}"
        
        # Format dengan pemisah ribuan menggunakan titik (standar Indonesia)
        formatted = f"{amount:,}".replace(",", ".")
        return f"Rp {formatted}"
    
    @staticmethod
    def parse_input(input_str: str) -> Optional[int]:
        """
        Parse user input menjadi integer, mendukung berbagai format input.
        
        Args:
            input_str: String input dari pengguna
            
        Returns:
            Integer value atau None jika parsing gagal
            
        Examples:
            >>> CurrencyFormatter.parse_input("1.000.000")
            1000000
            >>> CurrencyFormatter.parse_input("Rp 1,500,000")
            1500000
            >>> CurrencyFormatter.parse_input("1500000")
            1500000
        """
        if not input_str or not isinstance(input_str, str) or not input_str.strip():
            return None
        
        # Normalisasi input: hapus whitespace di awal dan akhir
        cleaned_input = input_str.strip()
        
        # Hapus prefix "Rp" atau "IDR" (case insensitive)
        cleaned_input = re.sub(r'^(rp|idr)\s*', '', cleaned_input, flags=re.IGNORECASE)
        
        # Hapus semua karakter non-digit kecuali minus di awal
        # Pertahankan tanda minus jika ada di awal
        is_negative = cleaned_input.startswith('-')
        cleaned = re.sub(r'[^\d]', '', cleaned_input)
        
        if not cleaned:
            return None
        
        try:
            result = int(cleaned)
            return -result if is_negative else result
        except (ValueError, OverflowError):
            return None
    
    @staticmethod
    def format_with_percentage(amount: int, total: int) -> str:
        """
        Format amount dengan persentase dari total.
        
        Args:
            amount: Jumlah bagian
            total: Total keseluruhan
            
        Returns:
            String dengan format "Rp X.XXX.XXX (XX.X%)"
        """
        if total == 0:
            percentage = 0.0
        else:
            # Use integer arithmetic to avoid floating point precision errors
            # Calculate percentage as (amount * 1000) // total / 10.0
            # This gives us 1 decimal place precision using integer operations
            percentage = (amount * 1000 // total) / 10.0
        
        formatted_amount = CurrencyFormatter.format_rupiah(amount)
        return f"{formatted_amount} ({percentage:.1f}%)"
    
    @staticmethod
    def validate_format_consistency(amounts: list) -> bool:
        """
        Validasi bahwa semua amounts dapat diformat secara konsisten.
        
        Args:
            amounts: List of integer amounts
            
        Returns:
            True jika semua amounts valid untuk formatting
        """
        if not amounts:
            return True
        
        try:
            for amount in amounts:
                if not isinstance(amount, int):
                    return False
                # Test formatting
                CurrencyFormatter.format_rupiah(amount)
            return True
        except (TypeError, ValueError):
            return False


class ValidationUtils:
    """Utility class untuk validasi input dan format"""
    
    @staticmethod
    def is_valid_amount(amount: int) -> bool:
        """
        Validasi apakah jumlah cocok untuk dibagi.
        
        Args:
            amount: Jumlah dalam integer
            
        Returns:
            True jika amount valid untuk pembagian
        """
        return isinstance(amount, int) and amount > 0 and amount >= 10000  # Minimal 10 ribu
    
    @staticmethod
    def get_error_message(error_type: str) -> str:
        """
        Mendapatkan pesan error yang sesuai dalam bahasa Indonesia.
        
        Args:
            error_type: Tipe error yang terjadi
            
        Returns:
            String pesan error yang sesuai
        """
        error_messages = {
            "negative_or_zero": "Jumlah harus lebih besar dari 0",
            "too_small": "Jumlah minimal untuk dibagi adalah Rp 10.000",
            "invalid_format": "Masukkan angka yang valid (contoh: 1000000 atau 1.000.000)",
            "processing_error": "Terjadi kesalahan dalam pembagian, silakan coba lagi",
            "memory_error": "Jumlah terlalu besar untuk diproses",
            "type_error": "Input harus berupa angka",
            "overflow_error": "Angka terlalu besar untuk diproses"
        }
        return error_messages.get(error_type, "Terjadi kesalahan yang tidak diketahui")
    
    @staticmethod
    def validate_input_string(input_str: str) -> tuple[bool, str]:
        """
        Validasi string input sebelum parsing.
        
        Args:
            input_str: String input dari pengguna
            
        Returns:
            Tuple (is_valid, error_message)
        """
        if not input_str or not isinstance(input_str, str):
            return False, ValidationUtils.get_error_message("invalid_format")
        
        if not input_str.strip():
            return False, ValidationUtils.get_error_message("invalid_format")
        
        # Check if contains any digits
        if not re.search(r'\d', input_str):
            return False, ValidationUtils.get_error_message("invalid_format")
        
        return True, ""
    
    @staticmethod
    def is_reasonable_amount(amount: int, max_amount: int = 1_000_000_000) -> bool:
        """
        Validasi apakah amount dalam range yang wajar.
        
        Args:
            amount: Jumlah untuk divalidasi
            max_amount: Batas maksimal (default 1 miliar)
            
        Returns:
            True jika amount dalam range wajar
        """
        return 0 <= amount <= max_amount