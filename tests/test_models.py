"""
Unit tests untuk data models
"""

import pytest
from datetime import datetime
from money_splitter.models import SplitResult, SplitPart


class TestSplitResult:
    """Test cases untuk SplitResult model"""
    
    def test_get_total(self):
        """Test get_total method"""
        splits = [2000000, 1500000, 1800000, 2200000, 2500000]
        result = SplitResult(
            original_amount=10000000,
            splits=splits,
            num_parts=5,
            timestamp=datetime.now()
        )
        
        assert result.get_total() == 10000000
        assert result.get_total() == sum(splits)
    
    def test_get_percentages(self):
        """Test get_percentages method"""
        splits = [2000000, 3000000, 5000000]  # Total: 10M
        result = SplitResult(
            original_amount=10000000,
            splits=splits,
            num_parts=3,
            timestamp=datetime.now()
        )
        
        percentages = result.get_percentages()
        assert len(percentages) == 3
        assert percentages[0] == 20.0  # 2M/10M * 100
        assert percentages[1] == 30.0  # 3M/10M * 100
        assert percentages[2] == 50.0  # 5M/10M * 100
    
    def test_get_percentages_zero_amount(self):
        """Test get_percentages with zero original amount"""
        splits = [0, 0, 0]
        with pytest.raises(ValueError, match="Original amount must be positive"):
            SplitResult(
                original_amount=0,
                splits=splits,
                num_parts=3,
                timestamp=datetime.now()
            )
    
    def test_is_balanced(self):
        """Test is_balanced method"""
        # Balanced case
        splits = [2000000, 3000000, 5000000]
        result = SplitResult(
            original_amount=10000000,
            splits=splits,
            num_parts=3,
            timestamp=datetime.now()
        )
        assert result.is_balanced() is True
        
        # Unbalanced case
        splits = [2000000, 3000000, 4000000]  # Total: 9M, not 10M
        result = SplitResult(
            original_amount=10000000,
            splits=splits,
            num_parts=3,
            timestamp=datetime.now()
        )
        assert result.is_balanced() is False
    
    def test_get_split_parts(self):
        """Test get_split_parts method"""
        splits = [2000000, 3000000, 5000000]
        result = SplitResult(
            original_amount=10000000,
            splits=splits,
            num_parts=3,
            timestamp=datetime.now()
        )
        
        parts = result.get_split_parts()
        assert len(parts) == 3
        assert parts[0].amount == 2000000
        assert parts[0].percentage == 20.0
        assert parts[0].index == 0
        assert parts[1].amount == 3000000
        assert parts[1].percentage == 30.0
        assert parts[1].index == 1
        assert parts[2].amount == 5000000
        assert parts[2].percentage == 50.0
        assert parts[2].index == 2
    
    def test_validation_negative_amount(self):
        """Test validation for negative original amount"""
        with pytest.raises(ValueError, match="Original amount must be positive"):
            SplitResult(
                original_amount=-1000000,
                splits=[500000, 500000],
                num_parts=2,
                timestamp=datetime.now()
            )
    
    def test_validation_empty_splits(self):
        """Test validation for empty splits list"""
        with pytest.raises(ValueError, match="Splits list cannot be empty"):
            SplitResult(
                original_amount=1000000,
                splits=[],
                num_parts=0,
                timestamp=datetime.now()
            )
    
    def test_validation_mismatched_num_parts(self):
        """Test validation for mismatched num_parts"""
        with pytest.raises(ValueError, match="Number of splits must match num_parts"):
            SplitResult(
                original_amount=1000000,
                splits=[500000, 500000],
                num_parts=3,  # Should be 2
                timestamp=datetime.now()
            )
    
    def test_validation_negative_splits(self):
        """Test validation for negative splits"""
        with pytest.raises(ValueError, match="All splits must be positive"):
            SplitResult(
                original_amount=1000000,
                splits=[600000, -100000, 500000],
                num_parts=3,
                timestamp=datetime.now()
            )


class TestSplitPart:
    """Test cases untuk SplitPart model"""
    
    def test_split_part_creation(self):
        """Test SplitPart creation"""
        part = SplitPart(amount=1500000, percentage=15.0, index=0)
        
        assert part.amount == 1500000
        assert part.percentage == 15.0
        assert part.index == 0
    
    def test_validation_negative_amount(self):
        """Test validation for negative amount"""
        with pytest.raises(ValueError, match="Amount must be positive"):
            SplitPart(amount=-1500000, percentage=15.0, index=0)
    
    def test_validation_negative_percentage(self):
        """Test validation for negative percentage"""
        with pytest.raises(ValueError, match="Percentage cannot be negative"):
            SplitPart(amount=1500000, percentage=-15.0, index=0)
    
    def test_validation_negative_index(self):
        """Test validation for negative index"""
        with pytest.raises(ValueError, match="Index must be non-negative"):
            SplitPart(amount=1500000, percentage=15.0, index=-1)