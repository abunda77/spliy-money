"""
Property-based tests untuk Money Splitter
Menggunakan hypothesis untuk comprehensive testing
"""

import pytest
from hypothesis import given, strategies as st, settings
from money_splitter.splitter import MoneySplitter
from money_splitter.models import SplitResult


class TestMoneySplitterProperties:
    """Property-based tests untuk MoneySplitter"""
    
    def setup_method(self):
        """Setup untuk setiap test"""
        self.splitter = MoneySplitter()
    
    @given(st.integers(min_value=10000, max_value=100000000))
    @settings(max_examples=100)
    def test_property_1_total_conservation(self, amount):
        """
        Feature: money-splitter, Property 1: Konservasi Total
        **Validates: Requirements 1.2, 6.2, 6.4**
        
        Untuk setiap jumlah uang valid yang dibagi, total semua bagian hasil 
        pembagian harus persis sama dengan jumlah input asli
        """
        result = self.splitter.split_money(amount)
        assert result.get_total() == amount
        assert sum(result.splits) == amount
    
    @given(st.integers(min_value=10000, max_value=100000000))
    @settings(max_examples=100)
    def test_property_2_valid_part_count(self, amount):
        """
        Feature: money-splitter, Property 2: Jumlah Bagian yang Valid
        **Validates: Requirements 1.1**
        
        Untuk setiap pembagian yang dilakukan, jumlah bagian yang dihasilkan 
        harus selalu 5 atau 6
        """
        result = self.splitter.split_money(amount)
        assert result.num_parts in [5, 6]
        assert len(result.splits) == result.num_parts
    
    @given(st.integers(max_value=9999))
    @settings(max_examples=50)
    def test_property_3_invalid_input_rejection_small(self, amount):
        """
        Feature: money-splitter, Property 3: Penolakan Input Invalid (Small)
        **Validates: Requirements 1.4, 4.1, 4.2**
        
        Untuk setiap input yang terlalu kecil, sistem harus menolak input 
        dan memberikan pesan error
        """
        if amount > 0:
            with pytest.raises(ValueError):
                self.splitter.split_money(amount)
    
    @given(st.integers(max_value=0))
    @settings(max_examples=50)
    def test_property_3_invalid_input_rejection_negative_zero(self, amount):
        """
        Feature: money-splitter, Property 3: Penolakan Input Invalid (Negative/Zero)
        **Validates: Requirements 1.4, 4.1, 4.2**
        
        Untuk setiap input yang negatif atau nol, sistem harus menolak input 
        dan memberikan pesan error
        """
        with pytest.raises(ValueError):
            self.splitter.split_money(amount)
    
    @given(st.integers(min_value=10000, max_value=100000000))
    @settings(max_examples=100)
    def test_property_13_integer_precision(self, amount):
        """
        Feature: money-splitter, Property 13: Presisi Integer
        **Validates: Requirements 6.3**
        
        Untuk setiap operasi pembagian, semua hasil harus berupa integer 
        tanpa floating point errors
        """
        result = self.splitter.split_money(amount)
        
        # Semua splits harus integer
        for split in result.splits:
            assert isinstance(split, int)
            assert split == int(split)  # Tidak ada decimal
        
        # Original amount dan total harus integer
        assert isinstance(result.original_amount, int)
        assert isinstance(result.get_total(), int)
    
    @given(st.integers(min_value=10000, max_value=100000000))
    @settings(max_examples=100)
    def test_property_4_natural_numbers(self, amount):
        """
        Feature: money-splitter, Property 4: Angka Natural
        **Validates: Requirements 2.1, 2.2**
        
        Untuk setiap hasil pembagian, tidak boleh ada bagian yang merupakan 
        kelipatan persis 1.000.000
        """
        result = self.splitter.split_money(amount)
        
        # Tidak boleh ada bagian yang kelipatan persis 1.000.000
        for split in result.splits:
            assert split % 1000000 != 0, f"Split {split} adalah kelipatan persis 1.000.000"
    
    @given(st.integers(min_value=10000, max_value=100000000))
    @settings(max_examples=50)  # Reduced for performance
    def test_property_5_thousands_preference(self, amount):
        """
        Feature: money-splitter, Property 5: Preferensi Ribuan
        **Validates: Requirements 2.3**
        
        Untuk setiap hasil pembagian, harus ada preferensi untuk angka yang berakhir 
        dengan 000. Diukur dengan menjalankan multiple kali dan memastikan ada 
        variasi yang menunjukkan preferensi ribuan.
        """
        # Run multiple times to check for preference pattern
        thousands_counts = []
        for _ in range(10):
            result = self.splitter.split_money(amount)
            thousands_count = sum(1 for split in result.splits if split % 1000 == 0)
            thousands_counts.append(thousands_count)
        
        # Should have some thousands endings (not all zero)
        total_thousands = sum(thousands_counts)
        total_splits = sum(len(self.splitter.split_money(amount).splits) for _ in range(10))
        
        # At least 25% should end with thousands to show preference
        preference_ratio = total_thousands / total_splits
        assert preference_ratio >= 0.25, f"Hanya {preference_ratio:.1%} menunjukkan preferensi ribuan, minimal 25%"
    
    @given(st.integers(min_value=10000, max_value=100000000))
    @settings(max_examples=100)
    def test_property_6_size_variation(self, amount):
        """
        Feature: money-splitter, Property 6: Variasi Ukuran
        **Validates: Requirements 2.4, 3.4**
        
        Untuk setiap hasil pembagian, tidak boleh ada dua bagian yang identik 
        dan perbedaan antara bagian terbesar dan terkecil harus minimal 10% dari rata-rata
        """
        result = self.splitter.split_money(amount)
        
        # Tidak boleh ada dua bagian yang identik
        assert len(set(result.splits)) == len(result.splits), "Ada bagian yang identik"
        
        # Perbedaan min-max harus minimal 10% dari rata-rata
        min_split = min(result.splits)
        max_split = max(result.splits)
        average = amount / len(result.splits)
        difference = max_split - min_split
        
        assert difference >= 0.1 * average, f"Perbedaan {difference} kurang dari 10% rata-rata {average}"
    
    @given(st.integers(min_value=10000, max_value=100000000))
    @settings(max_examples=20)  # Reduced for performance
    def test_property_7_result_randomness(self, amount):
        """
        Feature: money-splitter, Property 7: Randomness Hasil
        **Validates: Requirements 3.1**
        
        Untuk setiap input yang sama, memanggil fungsi pembagian 10 kali 
        harus menghasilkan minimal 8 hasil yang berbeda
        """
        results = []
        for _ in range(10):
            result = self.splitter.split_money(amount)
            results.append(tuple(sorted(result.splits)))
        
        unique_results = len(set(results))
        assert unique_results >= 8, f"Hanya {unique_results} hasil unik dari 10 pemanggilan"
    
    @given(st.integers(min_value=10000, max_value=100000000))
    @settings(max_examples=100)
    def test_property_8_reasonable_distribution(self, amount):
        """
        Feature: money-splitter, Property 8: Distribusi Wajar
        **Validates: Requirements 3.2**
        
        Untuk setiap hasil pembagian, tidak boleh ada bagian yang kurang dari 5% 
        atau lebih dari 40% dari total
        """
        result = self.splitter.split_money(amount)
        
        for split in result.splits:
            percentage = split / amount
            assert percentage >= 0.05, f"Bagian {split} adalah {percentage:.1%} dari total, kurang dari 5%"
            assert percentage <= 0.40, f"Bagian {split} adalah {percentage:.1%} dari total, lebih dari 40%"
    
    @given(st.integers(min_value=10000, max_value=100000000))
    @settings(max_examples=10)  # Reduced for performance
    def test_property_9_part_count_variation(self, amount):
        """
        Feature: money-splitter, Property 9: Variasi Jumlah Bagian
        **Validates: Requirements 3.3**
        
        Untuk setiap 100 pemanggilan fungsi, harus ada variasi antara hasil 5 bagian 
        dan 6 bagian (tidak boleh semua 5 atau semua 6)
        """
        part_counts = []
        for _ in range(100):
            result = self.splitter.split_money(amount)
            part_counts.append(result.num_parts)
        
        unique_counts = set(part_counts)
        assert len(unique_counts) > 1, f"Semua hasil memiliki jumlah bagian yang sama: {unique_counts}"
        assert 5 in unique_counts and 6 in unique_counts, f"Tidak ada variasi 5-6 bagian: {unique_counts}"
    def test_property_10_system_stability(self):
        """
        Feature: money-splitter, Property 10: Stabilitas Sistem
        **Validates: Requirements 4.3**
        
        Untuk setiap kondisi error yang mungkin terjadi, sistem harus tetap stabil 
        dan tidak crash
        """
        # Test berbagai kondisi error
        error_inputs = [-1000000, 0, 5000, "invalid", None]
        
        for error_input in error_inputs:
            try:
                if error_input is None or isinstance(error_input, str):
                    # Skip invalid types for this test
                    continue
                self.splitter.split_money(error_input)
                # Jika tidak error, berarti input valid
            except ValueError:
                # Expected error, sistem stabil
                pass
            except Exception as e:
                pytest.fail(f"Sistem crash dengan error: {e} untuk input: {error_input}")
    
    @given(st.integers(min_value=10000, max_value=100000000))
    @settings(max_examples=100)
    def test_property_11_consistent_formatting(self, amount):
        """
        Feature: money-splitter, Property 11: Format Konsisten
        **Validates: Requirements 5.1, 5.4**
        
        Untuk setiap output yang ditampilkan, format mata uang harus konsisten 
        dengan pemisah ribuan yang benar
        """
        from money_splitter.utils import CurrencyFormatter
        
        result = self.splitter.split_money(amount)
        
        # Test format original amount
        formatted_original = CurrencyFormatter.format_rupiah(result.original_amount)
        assert "Rp " in formatted_original
        assert "." in formatted_original or result.original_amount < 1000  # Pemisah ribuan
        
        # Test format semua splits
        for split in result.splits:
            formatted_split = CurrencyFormatter.format_rupiah(split)
            assert "Rp " in formatted_split
            # Pastikan format konsisten
            if split >= 1000:
                assert "." in formatted_split  # Harus ada pemisah ribuan
    
    @given(st.integers(min_value=10000, max_value=100000000))
    @settings(max_examples=100)
    def test_property_12_complete_display(self, amount):
        """
        Feature: money-splitter, Property 12: Kelengkapan Display
        **Validates: Requirements 1.3, 5.3**
        
        Untuk setiap hasil pembagian, jumlah item yang ditampilkan di UI harus 
        sama dengan jumlah bagian yang dihasilkan
        """
        from money_splitter.gui import MoneySpitterGUI
        import tkinter as tk
        
        # Create GUI instance for testing
        gui = MoneySpitterGUI()
        
        try:
            result = self.splitter.split_money(amount)
            gui.display_results(result)
            
            # Check if number of displayed items matches number of splits
            tree_items = gui.results_tree.get_children()
            assert len(tree_items) == len(result.splits), f"Displayed {len(tree_items)} items, expected {len(result.splits)}"
            assert len(tree_items) == result.num_parts, f"Displayed {len(tree_items)} items, expected {result.num_parts} parts"
            
        finally:
            # Cleanup GUI
            gui.root.destroy()