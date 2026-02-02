"""
Data models untuk Money Splitter application
"""

from dataclasses import dataclass
from datetime import datetime
from typing import List


@dataclass
class SplitResult:
    """Model untuk menyimpan hasil pembagian uang"""
    original_amount: int
    splits: List[int]
    num_parts: int
    timestamp: datetime
    
    def __post_init__(self):
        """Validasi data setelah inisialisasi"""
        if self.original_amount <= 0:
            raise ValueError("Original amount must be positive")
        if not self.splits:
            raise ValueError("Splits list cannot be empty")
        if len(self.splits) != self.num_parts:
            raise ValueError("Number of splits must match num_parts")
        if any(split <= 0 for split in self.splits):
            raise ValueError("All splits must be positive")
    
    def get_total(self) -> int:
        """Mengembalikan total dari semua bagian"""
        return sum(self.splits)
    
    def get_percentages(self) -> List[float]:
        """Mengembalikan persentase setiap bagian dari total"""
        if self.original_amount == 0:
            return [0.0] * len(self.splits)
        # Use integer arithmetic to avoid floating point precision errors
        # Calculate percentage as (split * 10000) // original_amount / 100.0
        # This gives us 2 decimal places precision using integer operations
        return [(split * 10000 // self.original_amount) / 100.0 for split in self.splits]
    
    def is_balanced(self) -> bool:
        """Mengecek apakah total splits sama dengan original amount"""
        return self.get_total() == self.original_amount
    
    def get_split_parts(self) -> List['SplitPart']:
        """Mengembalikan list SplitPart objects"""
        percentages = self.get_percentages()
        return [
            SplitPart(amount=split, percentage=percentage, index=i)
            for i, (split, percentage) in enumerate(zip(self.splits, percentages))
        ]


@dataclass
class SplitPart:
    """Model untuk bagian individual dari pembagian"""
    amount: int
    percentage: float
    index: int
    
    def __post_init__(self):
        """Validasi data setelah inisialisasi"""
        if self.amount <= 0:
            raise ValueError("Amount must be positive")
        if self.percentage < 0:
            raise ValueError("Percentage cannot be negative")
        if self.index < 0:
            raise ValueError("Index must be non-negative")