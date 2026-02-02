"""
Unit tests untuk utility functions
"""

import pytest
from money_splitter.utils import CurrencyFormatter, ValidationUtils


class TestCurrencyFormatter:
    """Test cases untuk CurrencyFormatter"""
    
    def test_format_rupiah_basic(self):
        """Test format_rupiah method dengan input dasar"""
        assert CurrencyFormatter.format_rupiah(1000000) == "Rp 1.000.000"
        assert CurrencyFormatter.format_rupiah(1500000) == "Rp 1.500.000"
        assert CurrencyFormatter.format_rupiah(10000) == "Rp 10.000"
        assert CurrencyFormatter.format_rupiah(0) == "Rp 0"
    
    def test_format_rupiah_negative(self):
        """Test format_rupiah dengan angka negatif"""
        assert CurrencyFormatter.format_rupiah(-1000000) == "Rp -1.000.000"
        assert CurrencyFormatter.format_rupiah(-500000) == "Rp -500.000"
    
    def test_format_rupiah_large_numbers(self):
        """Test format_rupiah dengan angka besar"""
        assert CurrencyFormatter.format_rupiah(1000000000) == "Rp 1.000.000.000"
        assert CurrencyFormatter.format_rupiah(123456789) == "Rp 123.456.789"
    
    def test_format_rupiah_type_error(self):
        """Test format_rupiah dengan tipe data yang salah"""
        with pytest.raises(TypeError):
            CurrencyFormatter.format_rupiah("1000000")
        with pytest.raises(TypeError):
            CurrencyFormatter.format_rupiah(1000000.5)
    
    def test_parse_input_valid_formats(self):
        """Test parse_input dengan berbagai format valid"""
        assert CurrencyFormatter.parse_input("1000000") == 1000000
        assert CurrencyFormatter.parse_input("1.000.000") == 1000000
        assert CurrencyFormatter.parse_input("Rp 1.000.000") == 1000000
        assert CurrencyFormatter.parse_input("1,000,000") == 1000000
        assert CurrencyFormatter.parse_input("  1000000  ") == 1000000
        assert CurrencyFormatter.parse_input("IDR 1.500.000") == 1500000
        assert CurrencyFormatter.parse_input("rp 2000000") == 2000000
    
    def test_parse_input_negative_numbers(self):
        """Test parse_input dengan angka negatif"""
        assert CurrencyFormatter.parse_input("-1000000") == -1000000
        assert CurrencyFormatter.parse_input("Rp -500.000") == -500000
    
    def test_parse_input_invalid(self):
        """Test parse_input dengan input invalid"""
        assert CurrencyFormatter.parse_input("") is None
        assert CurrencyFormatter.parse_input("   ") is None
        assert CurrencyFormatter.parse_input("abc") is None
        assert CurrencyFormatter.parse_input("Rp") is None
        assert CurrencyFormatter.parse_input(None) is None
        assert CurrencyFormatter.parse_input(123) is None  # Not a string
    
    def test_format_with_percentage(self):
        """Test format_with_percentage method"""
        assert CurrencyFormatter.format_with_percentage(1000000, 5000000) == "Rp 1.000.000 (20.0%)"
        assert CurrencyFormatter.format_with_percentage(750000, 3000000) == "Rp 750.000 (25.0%)"
        assert CurrencyFormatter.format_with_percentage(1000000, 0) == "Rp 1.000.000 (0.0%)"
    
    def test_validate_format_consistency(self):
        """Test validate_format_consistency method"""
        assert CurrencyFormatter.validate_format_consistency([1000000, 2000000, 3000000]) is True
        assert CurrencyFormatter.validate_format_consistency([]) is True
        assert CurrencyFormatter.validate_format_consistency([1000000, "invalid", 3000000]) is False
        assert CurrencyFormatter.validate_format_consistency([1000000, 2000000.5]) is False


class TestValidationUtils:
    """Test cases untuk ValidationUtils"""
    
    def test_is_valid_amount(self):
        """Test is_valid_amount method"""
        assert ValidationUtils.is_valid_amount(10000) is True
        assert ValidationUtils.is_valid_amount(1000000) is True
        assert ValidationUtils.is_valid_amount(9999) is False
        assert ValidationUtils.is_valid_amount(0) is False
        assert ValidationUtils.is_valid_amount(-1000) is False
        assert ValidationUtils.is_valid_amount("10000") is False  # String input
    
    def test_get_error_message(self):
        """Test get_error_message method"""
        assert "lebih besar dari 0" in ValidationUtils.get_error_message("negative_or_zero")
        assert "10.000" in ValidationUtils.get_error_message("too_small")
        assert "angka yang valid" in ValidationUtils.get_error_message("invalid_format")
        assert "tidak diketahui" in ValidationUtils.get_error_message("unknown_error")
        assert "berupa angka" in ValidationUtils.get_error_message("type_error")
    
    def test_validate_input_string(self):
        """Test validate_input_string method"""
        is_valid, _ = ValidationUtils.validate_input_string("1000000")
        assert is_valid is True
        
        is_valid, _ = ValidationUtils.validate_input_string("Rp 1.000.000")
        assert is_valid is True
        
        is_valid, error = ValidationUtils.validate_input_string("")
        assert is_valid is False
        assert "angka yang valid" in error
        
        is_valid, error = ValidationUtils.validate_input_string("abc")
        assert is_valid is False
        
        is_valid, error = ValidationUtils.validate_input_string(None)
        assert is_valid is False
    
    def test_is_reasonable_amount(self):
        """Test is_reasonable_amount method"""
        assert ValidationUtils.is_reasonable_amount(1000000) is True
        assert ValidationUtils.is_reasonable_amount(0) is True
        assert ValidationUtils.is_reasonable_amount(1000000000) is True
        assert ValidationUtils.is_reasonable_amount(1000000001) is False
        assert ValidationUtils.is_reasonable_amount(-1) is False