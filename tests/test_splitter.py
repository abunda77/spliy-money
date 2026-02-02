"""
Unit tests untuk MoneySplitter business logic
"""

import pytest
from money_splitter.splitter import MoneySplitter
from money_splitter.models import SplitResult


class TestMoneySplitter:
    """Test cases untuk MoneySplitter"""
    
    def setup_method(self):
        """Setup untuk setiap test"""
        self.splitter = MoneySplitter()
    
    def test_split_money_valid_input(self):
        """Test split_money dengan input valid"""
        result = self.splitter.split_money(10000000)
        
        assert isinstance(result, SplitResult)
        assert result.original_amount == 10000000
        assert result.num_parts in [5, 6]
        assert len(result.splits) == result.num_parts
        assert result.get_total() == 10000000
    
    def test_split_money_invalid_input_negative(self):
        """Test split_money dengan input negatif"""
        with pytest.raises(ValueError) as exc_info:
            self.splitter.split_money(-1000000)
        
        assert "lebih besar dari 0" in str(exc_info.value)
    
    def test_split_money_invalid_input_zero(self):
        """Test split_money dengan input nol"""
        with pytest.raises(ValueError) as exc_info:
            self.splitter.split_money(0)
        
        assert "lebih besar dari 0" in str(exc_info.value)
    
    def test_split_money_invalid_input_too_small(self):
        """Test split_money dengan input terlalu kecil"""
        with pytest.raises(ValueError) as exc_info:
            self.splitter.split_money(5000)
        
        assert "10.000" in str(exc_info.value)
    
    def test_split_money_conservation(self):
        """Test bahwa total pembagian sama dengan input"""
        amounts = [10000000, 5000000, 15000000, 100000000]
        
        for amount in amounts:
            result = self.splitter.split_money(amount)
            assert result.get_total() == amount
    
    def test_split_money_part_count(self):
        """Test bahwa jumlah bagian selalu 5 atau 6"""
        for _ in range(20):  # Test multiple times karena random
            result = self.splitter.split_money(10000000)
            assert result.num_parts in [5, 6]
            assert len(result.splits) == result.num_parts