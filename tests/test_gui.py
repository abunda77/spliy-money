"""
Unit tests untuk GUI components
"""

import unittest
import tkinter as tk
from money_splitter.gui import MoneySpitterGUI
from money_splitter.models import SplitResult
from money_splitter.utils import CurrencyFormatter
from datetime import datetime


class TestMoneySpitterGUI(unittest.TestCase):
    """Test cases untuk MoneySpitterGUI class"""
    
    def setUp(self):
        """Setup test fixtures"""
        self.gui = MoneySpitterGUI()
    
    def tearDown(self):
        """Cleanup after tests"""
        self.gui.root.destroy()
    
    def test_gui_initialization(self):
        """Test GUI initialization - Requirements 1.3, 5.3"""
        # Test main window setup
        self.assertEqual(self.gui.root.title(), "Money Splitter")
        self.assertIsNotNone(self.gui.amount_entry)
        self.assertIsNotNone(self.gui.split_button)
        self.assertIsNotNone(self.gui.results_tree)
        self.assertIsNotNone(self.gui.total_label)
        self.assertIsNotNone(self.gui.summary_label)
    
    def test_input_field_functionality(self):
        """Test input field for money amount - Requirements 1.3"""
        # Test input entry
        test_amount = "1000000"
        self.gui.amount_entry.insert(0, test_amount)
        self.assertEqual(self.gui.amount_entry.get(), test_amount)
        
        # Test parsing
        parsed = CurrencyFormatter.parse_input(test_amount)
        self.assertEqual(parsed, 1000000)
    
    def test_split_button_exists(self):
        """Test 'Bagi Uang' button exists - Requirements 1.3"""
        self.assertEqual(self.gui.split_button.cget("text"), "Bagi Uang")
        self.assertIsNotNone(self.gui.split_button.cget("command"))
    
    def test_display_results_functionality(self):
        """Test display results shows all split amounts - Requirements 1.3, 5.3"""
        # Create test result
        test_splits = [200000, 180000, 220000, 150000, 250000]
        test_result = SplitResult(
            original_amount=1000000,
            splits=test_splits,
            num_parts=5,
            timestamp=datetime.now()
        )
        
        # Display results
        self.gui.display_results(test_result)
        
        # Check if all splits are displayed
        tree_items = self.gui.results_tree.get_children()
        self.assertEqual(len(tree_items), 5)
        
        # Check if summary shows number of parts (Requirement 5.3)
        summary_text = self.gui.summary_label.cget("text")
        self.assertEqual(summary_text, "Dibagi menjadi 5 bagian")
        
        # Check if total is displayed
        total_text = self.gui.total_label.cget("text")
        self.assertIn("Total:", total_text)
        self.assertIn("Rp 1.000.000", total_text)
    
    def test_display_all_split_amounts(self):
        """Test that all Split_Amount are displayed to user - Requirements 1.3"""
        # Test with 6 parts
        test_splits = [150000, 180000, 200000, 170000, 160000, 140000]
        test_result = SplitResult(
            original_amount=1000000,
            splits=test_splits,
            num_parts=6,
            timestamp=datetime.now()
        )
        
        self.gui.display_results(test_result)
        
        # Verify all splits are shown
        tree_items = self.gui.results_tree.get_children()
        self.assertEqual(len(tree_items), 6)
        
        # Verify each split amount is displayed correctly
        for i, item in enumerate(tree_items):
            values = self.gui.results_tree.item(item)['values']
            expected_amount = CurrencyFormatter.format_rupiah(test_splits[i])
            self.assertEqual(values[1], expected_amount)  # Column 1 is amount
    
    def test_display_number_of_parts(self):
        """Test that number of parts generated is displayed - Requirements 5.3"""
        # Test with 5 parts
        test_result_5 = SplitResult(
            original_amount=1000000,
            splits=[200000, 200000, 200000, 200000, 200000],
            num_parts=5,
            timestamp=datetime.now()
        )
        
        self.gui.display_results(test_result_5)
        summary_text = self.gui.summary_label.cget("text")
        self.assertEqual(summary_text, "Dibagi menjadi 5 bagian")
        
        # Test with 6 parts
        test_result_6 = SplitResult(
            original_amount=1200000,
            splits=[200000, 200000, 200000, 200000, 200000, 200000],
            num_parts=6,
            timestamp=datetime.now()
        )
        
        self.gui.display_results(test_result_6)
        summary_text = self.gui.summary_label.cget("text")
        self.assertEqual(summary_text, "Dibagi menjadi 6 bagian")
    
    def test_clear_results_functionality(self):
        """Test clear results functionality"""
        # First add some results
        test_result = SplitResult(
            original_amount=1000000,
            splits=[200000, 200000, 200000, 200000, 200000],
            num_parts=5,
            timestamp=datetime.now()
        )
        self.gui.display_results(test_result)
        
        # Verify results are displayed
        self.assertTrue(len(self.gui.results_tree.get_children()) > 0)
        self.assertNotEqual(self.gui.summary_label.cget("text"), "")
        self.assertNotEqual(self.gui.total_label.cget("text"), "")
        
        # Clear results
        self.gui.clear_results()
        
        # Verify results are cleared
        self.assertEqual(len(self.gui.results_tree.get_children()), 0)
        self.assertEqual(self.gui.summary_label.cget("text"), "")
        self.assertEqual(self.gui.total_label.cget("text"), "")
    
    def test_error_handling_gui(self):
        """Test error handling in GUI"""
        # Test with invalid input
        self.gui.amount_entry.insert(0, "invalid")
        
        # This should not crash the application
        try:
            self.gui.on_split_button_click()
            # Should handle error gracefully
        except Exception as e:
            self.fail(f"GUI should handle errors gracefully, but got: {e}")
    
    def test_status_updates(self):
        """Test status bar updates"""
        # Initial status
        self.assertEqual(self.gui.status_var.get(), "Siap")
        
        # Test with valid input
        self.gui.amount_entry.insert(0, "1000000")
        self.gui.on_split_button_click()
        
        # Should show success status
        self.assertEqual(self.gui.status_var.get(), "Pembagian berhasil")


if __name__ == '__main__':
    unittest.main()