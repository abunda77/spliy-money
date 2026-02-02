"""
Business logic untuk Money Splitter - algoritma pembagian uang
"""

import random
from datetime import datetime
from typing import List

from .models import SplitResult
from .utils import ValidationUtils


class MoneySplitter:
    """Class utama untuk melakukan pembagian uang"""
    
    def __init__(self):
        self.random = random.Random()
    
    def split_money(self, amount: int, num_parts: int = None) -> SplitResult:
        """
        Method utama untuk membagi uang menjadi beberapa bagian secara natural
        
        Args:
            amount: Jumlah uang yang akan dibagi
            num_parts: Jumlah bagian (2-6), jika None akan dipilih secara acak (5 atau 6)
            
        Returns:
            SplitResult: Hasil pembagian uang
            
        Raises:
            ValueError: Jika input tidak valid
        """
        if not self._validate_input(amount):
            if amount <= 0:
                raise ValueError(ValidationUtils.get_error_message("negative_or_zero"))
            else:
                raise ValueError(ValidationUtils.get_error_message("too_small"))
        
        # Validasi num_parts
        if num_parts is not None:
            if not isinstance(num_parts, int) or num_parts < 2 or num_parts > 6:
                raise ValueError("Jumlah bagian harus antara 2 dan 6")
        else:
            # Default: Tentukan jumlah bagian secara acak (5 atau 6)
            num_parts = self.random.choice([5, 6])
        
        # Generate pembagian natural
        splits = self._generate_natural_splits(amount, num_parts)
        
        return SplitResult(
            original_amount=amount,
            splits=splits,
            num_parts=num_parts,
            timestamp=datetime.now()
        )
    
    def _generate_natural_splits(self, amount: int, num_parts: int) -> List[int]:
        """
        Generate pembagian yang terlihat natural dengan variasi yang wajar
        
        Args:
            amount: Total jumlah yang akan dibagi
            num_parts: Jumlah bagian (5 atau 6)
            
        Returns:
            List[int]: Daftar pembagian yang natural
        """
        # Generate initial random splits dengan distribusi yang bervariasi
        splits = []
        remaining = amount
        
        # Generate num_parts-1 bagian secara acak
        for i in range(num_parts - 1):
            # Tentukan range untuk bagian ini (5% - 35% dari sisa)
            # Use integer arithmetic to avoid floating point errors
            min_part = max(remaining // (num_parts - i) // 2, remaining // 20)  # minimal 5%
            max_part = min(remaining * 35 // 100, remaining * 2 // (num_parts - i))  # maksimal 35%
            
            # Pastikan ada cukup sisa untuk bagian-bagian berikutnya
            min_remaining_needed = (num_parts - i - 1) * (amount // 20)  # minimal 5% per bagian sisanya
            max_part = min(max_part, remaining - min_remaining_needed)
            
            if min_part >= max_part:
                part = min_part
            else:
                part = self.random.randint(min_part, max_part)
            
            # Make this part natural
            part = self._make_amount_natural(part)
            splits.append(part)
            remaining -= part
        
        # Bagian terakhir adalah sisa yang tersisa
        last_part = remaining
        last_part = self._make_amount_natural(last_part)
        splits.append(last_part)
        
        # Balance adjustment untuk memastikan total tepat
        splits = self._balance_splits(splits, amount)
        
        # Shuffle untuk randomize urutan
        self.random.shuffle(splits)
        
        # Final validation dan adjustment
        splits = self._ensure_natural_properties(splits, amount)
        
        return splits
    
    def _make_amount_natural(self, amount: int) -> int:
        """
        Sesuaikan amount agar terlihat natural
        
        Args:
            amount: Jumlah yang akan disesuaikan
            
        Returns:
            int: Jumlah yang sudah disesuaikan agar terlihat natural
        """
        if amount <= 0:
            return amount
        
        # Hindari angka yang terlalu bulat (kelipatan 1 juta persis)
        if amount >= 1000000 and amount % 1000000 == 0:
            # Tambahkan variasi kecil (50k - 200k)
            adjustment = self.random.randint(50000, 200000)
            # Randomly add or subtract
            if self.random.choice([True, False]):
                amount += adjustment
            else:
                amount = max(amount - adjustment, amount // 2)  # Jangan sampai terlalu kecil
        
        # Preferensi untuk 3 digit terakhir berakhir dengan 000 (ribuan)
        last_three = amount % 1000
        
        # 80% kemungkinan untuk dibulatkan ke ribuan terdekat (increased from 70%)
        if self.random.random() < 0.8:
            if last_three >= 500:
                amount = amount - last_three + 1000
            else:
                amount = amount - last_three
        else:
            # 20% kemungkinan untuk variasi yang tidak bulat ribuan
            # Tapi tetap hindari angka yang terlalu acak
            if last_three < 100:
                # Jika sudah dekat ribuan, biarkan
                pass
            elif last_three > 900:
                # Jika dekat ribuan berikutnya, bulatkan
                amount = amount - last_three + 1000
            else:
                # Bulatkan ke ratusan terdekat
                last_hundred = last_three % 100
                if last_hundred >= 50:
                    amount = amount - last_hundred + 100
                else:
                    amount = amount - last_hundred
        
        return max(amount, 1000)  # Minimal 1000
    
    def _validate_input(self, amount: int) -> bool:
        """Validasi input amount"""
        return ValidationUtils.is_valid_amount(amount)
    
    def _balance_splits(self, splits: List[int], target_amount: int) -> List[int]:
        """
        Sesuaikan splits agar total tepat sama dengan target_amount
        Preserve thousands preference where possible
        
        Args:
            splits: List pembagian yang akan disesuaikan
            target_amount: Target total yang harus dicapai
            
        Returns:
            List[int]: Splits yang sudah disesuaikan
        """
        current_total = sum(splits)
        difference = target_amount - current_total
        
        if difference == 0:
            return splits
        
        # Distribusikan perbedaan secara acak ke bagian-bagian
        adjusted_splits = splits.copy()
        
        # Prioritize adjusting non-thousands ending splits first
        thousands_indices = [i for i, s in enumerate(adjusted_splits) if s % 1000 == 0]
        non_thousands_indices = [i for i, s in enumerate(adjusted_splits) if s % 1000 != 0]
        
        if difference > 0:
            # Perlu menambah - prioritize non-thousands first
            while difference > 0:
                # Choose from non-thousands first if available
                if non_thousands_indices and self.random.random() < 0.7:
                    idx = self.random.choice(non_thousands_indices)
                else:
                    idx = self.random.randint(0, len(adjusted_splits) - 1)
                
                # Use integer arithmetic to avoid floating point errors
                max_add = max(1, difference // len(adjusted_splits) + 1)
                add_amount = min(difference, self.random.randint(1, max_add))
                adjusted_splits[idx] += add_amount
                difference -= add_amount
        else:
            # Perlu mengurangi - prioritize non-thousands first
            difference = abs(difference)
            while difference > 0:
                # Choose from non-thousands first if available
                if non_thousands_indices and self.random.random() < 0.7:
                    idx = self.random.choice(non_thousands_indices)
                else:
                    idx = self.random.randint(0, len(adjusted_splits) - 1)
                
                # Pastikan tidak mengurangi terlalu banyak - use integer arithmetic
                max_reduce = min(difference, adjusted_splits[idx] // 10)  # Maksimal 10% dari nilai
                if max_reduce > 0:
                    reduce_amount = min(difference, self.random.randint(1, max_reduce))
                    adjusted_splits[idx] -= reduce_amount
                    difference -= reduce_amount
                else:
                    # Jika tidak bisa mengurangi dari bagian ini, coba yang lain
                    continue
        
        return adjusted_splits
    
    def _ensure_natural_properties(self, splits: List[int], original_amount: int) -> List[int]:
        """
        Pastikan splits memenuhi semua properti natural yang diinginkan
        
        Args:
            splits: List pembagian
            original_amount: Jumlah asli
            
        Returns:
            List[int]: Splits yang sudah memenuhi properti natural
        """
        adjusted_splits = splits.copy()
        
        # Pastikan tidak ada yang identik
        for i in range(len(adjusted_splits)):
            for j in range(i + 1, len(adjusted_splits)):
                if adjusted_splits[i] == adjusted_splits[j]:
                    # Tambahkan variasi kecil
                    variation = self.random.randint(100, 1000)  # Smaller variation
                    if self.random.choice([True, False]):
                        adjusted_splits[j] += variation
                    else:
                        adjusted_splits[j] = max(adjusted_splits[j] - variation, 1000)
                    
                    # Re-check for duplicates after adjustment
                    while adjusted_splits[j] in adjusted_splits[:j] + adjusted_splits[j+1:]:
                        variation = self.random.randint(100, 1000)
                        adjusted_splits[j] += variation
        
        # Pastikan distribusi wajar (5% - 40% dari total) - use integer arithmetic
        min_allowed = original_amount * 5 // 100  # 5% using integer division
        max_allowed = original_amount * 40 // 100  # 40% using integer division
        
        for i in range(len(adjusted_splits)):
            if adjusted_splits[i] < min_allowed:
                adjusted_splits[i] = min_allowed + self.random.randint(0, min_allowed // 10)
            elif adjusted_splits[i] > max_allowed:
                adjusted_splits[i] = max_allowed - self.random.randint(0, max_allowed // 10)
        
        # Final balance adjustment
        adjusted_splits = self._balance_splits(adjusted_splits, original_amount)
        
        # Ensure thousands preference is maintained
        adjusted_splits = self._ensure_thousands_preference(adjusted_splits, original_amount)
        
        # Final uniqueness check - ensure no duplicates
        adjusted_splits = self._ensure_uniqueness(adjusted_splits, original_amount)
        
        # Final distribution check - ensure reasonable distribution
        adjusted_splits = self._ensure_reasonable_distribution(adjusted_splits, original_amount)
        
        return adjusted_splits
    
    def _ensure_reasonable_distribution(self, splits: List[int], original_amount: int) -> List[int]:
        """
        Pastikan semua splits memiliki distribusi yang wajar (5% - 40%)
        
        Args:
            splits: List pembagian
            original_amount: Jumlah asli
            
        Returns:
            List[int]: Splits dengan distribusi yang wajar
        """
        adjusted_splits = splits.copy()
        min_allowed = original_amount * 5 // 100  # 5%
        max_allowed = original_amount * 40 // 100  # 40%
        
        # Keep trying until distribution is reasonable
        max_attempts = 5
        for attempt in range(max_attempts):
            # Fix distribution issues
            for i in range(len(adjusted_splits)):
                if adjusted_splits[i] < min_allowed:
                    adjusted_splits[i] = min_allowed + self.random.randint(0, min_allowed // 10)
                elif adjusted_splits[i] > max_allowed:
                    adjusted_splits[i] = max_allowed - self.random.randint(0, max_allowed // 10)
            
            # Balance after changes
            adjusted_splits = self._balance_splits(adjusted_splits, original_amount)
            
            # Check if distribution is now reasonable
            all_reasonable = all(
                min_allowed <= split <= max_allowed 
                for split in adjusted_splits
            )
            
            if all_reasonable:
                break
        
        return adjusted_splits
    
    def _ensure_uniqueness(self, splits: List[int], original_amount: int) -> List[int]:
        """
        Pastikan tidak ada splits yang identik, sambil mempertahankan thousands preference
        
        Args:
            splits: List pembagian
            original_amount: Jumlah asli
            
        Returns:
            List[int]: Splits tanpa duplikasi
        """
        adjusted_splits = splits.copy()
        
        # Keep adjusting until all values are unique
        max_attempts = 10
        for attempt in range(max_attempts):
            # Find duplicates
            seen = set()
            duplicates = []
            for i, value in enumerate(adjusted_splits):
                if value in seen:
                    duplicates.append(i)
                else:
                    seen.add(value)
            
            if not duplicates:
                break  # No duplicates found
            
            # Fix duplicates while trying to preserve thousands endings
            for idx in duplicates:
                original_value = adjusted_splits[idx]
                is_thousands = original_value % 1000 == 0
                attempts = 0
                
                while adjusted_splits[idx] in adjusted_splits[:idx] + adjusted_splits[idx+1:] and attempts < 20:
                    if is_thousands:
                        # Try to keep it as thousands ending
                        variation = self.random.choice([1000, 2000, 3000])
                        if self.random.choice([True, False]):
                            adjusted_splits[idx] = original_value + variation
                        else:
                            adjusted_splits[idx] = max(original_value - variation, 1000)
                    else:
                        # For non-thousands, small variation
                        variation = self.random.randint(50, 500)
                        if self.random.choice([True, False]):
                            adjusted_splits[idx] = original_value + variation
                        else:
                            adjusted_splits[idx] = max(original_value - variation, 1000)
                    attempts += 1
            
            # Balance after changes
            adjusted_splits = self._balance_splits(adjusted_splits, original_amount)
        
        return adjusted_splits
    
    def _ensure_thousands_preference(self, splits: List[int], original_amount: int) -> List[int]:
        """
        Pastikan minimal 60% dari splits berakhir dengan 000 (ribuan)
        
        Args:
            splits: List pembagian
            original_amount: Jumlah asli
            
        Returns:
            List[int]: Splits dengan thousands preference yang terjamin
        """
        adjusted_splits = splits.copy()
        
        # Calculate required thousands count (at least 50%)
        required_thousands = max(3, int(len(adjusted_splits) * 0.5 + 0.5))  # Round up
        
        # Keep trying until we meet the requirement
        max_attempts = 5
        for attempt in range(max_attempts):
            thousands_count = sum(1 for s in adjusted_splits if s % 1000 == 0)
            
            if thousands_count >= required_thousands:
                break
                
            # Need to change some splits to end with 000
            non_thousands_indices = [i for i, s in enumerate(adjusted_splits) if s % 1000 != 0]
            needed = required_thousands - thousands_count
            
            if len(non_thousands_indices) >= needed:
                # Select indices to change
                indices_to_change = self.random.sample(non_thousands_indices, needed)
                
                for idx in indices_to_change:
                    current_value = adjusted_splits[idx]
                    # Round to nearest thousand
                    remainder = current_value % 1000
                    if remainder >= 500:
                        adjusted_splits[idx] = current_value - remainder + 1000
                    else:
                        adjusted_splits[idx] = current_value - remainder
                    
                    # Ensure minimum value
                    adjusted_splits[idx] = max(adjusted_splits[idx], 1000)
            
            # Balance after changes
            adjusted_splits = self._balance_splits(adjusted_splits, original_amount)
        
        # Final check - if still not meeting requirement, force it
        thousands_count = sum(1 for s in adjusted_splits if s % 1000 == 0)
        if thousands_count < required_thousands:
            # Force the requirement by changing the largest non-thousands values
            non_thousands = [(i, s) for i, s in enumerate(adjusted_splits) if s % 1000 != 0]
            non_thousands.sort(key=lambda x: x[1], reverse=True)  # Sort by value, largest first
            
            needed = required_thousands - thousands_count
            for i in range(min(needed, len(non_thousands))):
                idx, value = non_thousands[i]
                # Round to nearest thousand
                remainder = value % 1000
                if remainder >= 500:
                    adjusted_splits[idx] = value - remainder + 1000
                else:
                    adjusted_splits[idx] = value - remainder
                adjusted_splits[idx] = max(adjusted_splits[idx], 1000)
            
            # Final balance
            adjusted_splits = self._balance_splits(adjusted_splits, original_amount)
        
        return adjusted_splits