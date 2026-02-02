# Dokumen Desain: Money Splitter

## Gambaran Umum

Money Splitter adalah aplikasi desktop Python dengan antarmuka grafis (GUI) yang memungkinkan pengguna untuk membagi sejumlah uang menjadi 5 atau 6 bagian secara acak dengan tampilan yang natural. Aplikasi ini menggunakan Tkinter untuk GUI dan dirancang dengan arsitektur yang bersih untuk memisahkan logika bisnis dari antarmuka pengguna.

## Arsitektur

Aplikasi menggunakan pola Model-View-Controller (MVC) dengan komponen-komponen berikut:

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   GUI Layer     │    │  Business Logic │    │   Data Models   │
│   (Tkinter)     │◄──►│   (Splitter)    │◄──►│  (SplitResult)  │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### Komponen Utama:
- **GUI Layer**: Antarmuka pengguna menggunakan Tkinter
- **Business Logic**: Algoritma pembagian uang dan validasi
- **Data Models**: Struktur data untuk menyimpan hasil pembagian
- **Utilities**: Helper functions untuk formatting dan validasi

## Komponen dan Interface

### 1. GUI Components (gui.py)

```python
class MoneySpitterGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.splitter = MoneySplitter()
        self.setup_ui()
    
    def setup_ui(self):
        # Setup main window, input fields, buttons, result display
        pass
    
    def on_split_button_click(self):
        # Handle split button click event
        pass
    
    def display_results(self, results: SplitResult):
        # Display split results in the GUI
        pass
    
    def show_error(self, message: str):
        # Display error messages
        pass
```

**UI Layout:**
- **Header**: Judul aplikasi "Money Splitter"
- **Input Section**: 
  - Label "Jumlah Uang (Rp)"
  - Entry field untuk input jumlah
  - Button "Bagi Uang"
- **Results Section**:
  - Area untuk menampilkan hasil pembagian
  - Tabel atau list dengan kolom: No, Jumlah, Persentase
  - Total verification di bagian bawah
- **Footer**: Status bar untuk pesan error/sukses

### 2. Business Logic (splitter.py)

```python
class MoneySplitter:
    def __init__(self):
        self.random = Random()
    
    def split_money(self, amount: int) -> SplitResult:
        # Main splitting algorithm
        pass
    
    def _generate_natural_splits(self, amount: int, num_parts: int) -> List[int]:
        # Generate natural-looking split amounts
        pass
    
    def _make_amount_natural(self, amount: int) -> int:
        # Adjust amount to look more natural
        pass
    
    def _validate_input(self, amount: int) -> bool:
        # Validate input amount
        pass
```

### 3. Data Models (models.py)

```python
@dataclass
class SplitResult:
    original_amount: int
    splits: List[int]
    num_parts: int
    timestamp: datetime
    
    def get_total(self) -> int:
        return sum(self.splits)
    
    def get_percentages(self) -> List[float]:
        return [split / self.original_amount * 100 for split in self.splits]

@dataclass
class SplitPart:
    amount: int
    percentage: float
    index: int
```

### 4. Utilities (utils.py)

```python
class CurrencyFormatter:
    @staticmethod
    def format_rupiah(amount: int) -> str:
        # Format amount as Indonesian Rupiah
        pass
    
    @staticmethod
    def parse_input(input_str: str) -> int:
        # Parse user input to integer
        pass

class ValidationUtils:
    @staticmethod
    def is_valid_amount(amount: int) -> bool:
        # Validate if amount is suitable for splitting
        pass
    
    @staticmethod
    def get_error_message(error_type: str) -> str:
        # Get localized error messages
        pass
```

## Data Models

### SplitResult
- `original_amount: int` - Jumlah asli yang dibagi
- `splits: List[int]` - Daftar hasil pembagian
- `num_parts: int` - Jumlah bagian (5 atau 6)
- `timestamp: datetime` - Waktu pembagian dilakukan

### SplitPart
- `amount: int` - Jumlah bagian individual
- `percentage: float` - Persentase dari total
- `index: int` - Urutan bagian

## Algoritma Pembagian

### Algoritma Natural Split

1. **Tentukan Jumlah Bagian**: Pilih secara acak antara 5 atau 6 bagian
2. **Generate Base Splits**: Bagi jumlah secara acak dengan distribusi yang wajar
3. **Natural Adjustment**: Sesuaikan setiap bagian agar terlihat natural:
   - Hindari angka yang terlalu bulat (kelipatan 1 juta persis)
   - Preferensi untuk 3 digit terakhir berakhir dengan 000
   - Pastikan variasi yang wajar antar bagian
4. **Balance Adjustment**: Sesuaikan pembagian agar total tetap sama
5. **Final Validation**: Pastikan semua kriteria natural terpenuhi

### Pseudocode Algoritma:

```
function split_money(amount, num_parts):
    // Generate initial random splits
    base_splits = generate_random_splits(amount, num_parts)
    
    // Make each split look natural
    natural_splits = []
    for split in base_splits:
        natural_split = make_natural(split)
        natural_splits.append(natural_split)
    
    // Adjust to maintain exact total
    adjusted_splits = balance_splits(natural_splits, amount)
    
    // Final validation
    validate_splits(adjusted_splits, amount)
    
    return SplitResult(amount, adjusted_splits, num_parts)

function make_natural(amount):
    // Avoid too round numbers
    if amount % 1000000 == 0:
        adjustment = random(50000, 200000)
        amount += adjustment
    
    // Prefer thousands ending
    last_three = amount % 1000
    if last_three > 500:
        amount = amount - last_three + 1000
    else:
        amount = amount - last_three
    
    return amount
```

## Correctness Properties

*Property adalah karakteristik atau perilaku yang harus berlaku benar di semua eksekusi sistem yang valid - pada dasarnya, pernyataan formal tentang apa yang harus dilakukan sistem. Property berfungsi sebagai jembatan antara spesifikasi yang dapat dibaca manusia dan jaminan kebenaran yang dapat diverifikasi mesin.*

Berdasarkan analisis prework kriteria penerimaan, berikut adalah property yang dapat ditest:

### Property 1: Konservasi Total (Total Conservation)
*Untuk setiap* jumlah uang valid yang dibagi, total semua bagian hasil pembagian harus persis sama dengan jumlah input asli
**Validates: Requirements 1.2, 6.2, 6.4**

### Property 2: Jumlah Bagian yang Valid (Valid Part Count)
*Untuk setiap* pembagian yang dilakukan, jumlah bagian yang dihasilkan harus selalu 5 atau 6
**Validates: Requirements 1.1**

### Property 3: Penolakan Input Invalid (Invalid Input Rejection)
*Untuk setiap* input yang negatif, nol, atau terlalu kecil, sistem harus menolak input dan memberikan pesan error
**Validates: Requirements 1.4, 4.1, 4.2**

### Property 4: Angka Natural (Natural Numbers)
*Untuk setiap* hasil pembagian, tidak boleh ada bagian yang merupakan kelipatan persis 1.000.000
**Validates: Requirements 2.1, 2.2**

### Property 5: Preferensi Ribuan (Thousands Preference)
*Untuk setiap* hasil pembagian, mayoritas bagian (minimal 60%) harus berakhir dengan 000
**Validates: Requirements 2.3**

### Property 6: Variasi Ukuran (Size Variation)
*Untuk setiap* hasil pembagian, tidak boleh ada dua bagian yang identik dan perbedaan antara bagian terbesar dan terkecil harus minimal 10% dari rata-rata
**Validates: Requirements 2.4, 3.4**

### Property 7: Randomness Hasil (Result Randomness)
*Untuk setiap* input yang sama, memanggil fungsi pembagian 10 kali harus menghasilkan minimal 8 hasil yang berbeda
**Validates: Requirements 3.1**

### Property 8: Distribusi Wajar (Reasonable Distribution)
*Untuk setiap* hasil pembagian, tidak boleh ada bagian yang kurang dari 5% atau lebih dari 40% dari total
**Validates: Requirements 3.2**

### Property 9: Variasi Jumlah Bagian (Part Count Variation)
*Untuk setiap* 100 pemanggilan fungsi, harus ada variasi antara hasil 5 bagian dan 6 bagian (tidak boleh semua 5 atau semua 6)
**Validates: Requirements 3.3**

### Property 10: Stabilitas Sistem (System Stability)
*Untuk setiap* kondisi error yang mungkin terjadi, sistem harus tetap stabil dan tidak crash
**Validates: Requirements 4.3**

### Property 11: Format Konsisten (Consistent Formatting)
*Untuk setiap* output yang ditampilkan, format mata uang harus konsisten dengan pemisah ribuan yang benar
**Validates: Requirements 5.1, 5.4**

### Property 12: Kelengkapan Display (Complete Display)
*Untuk setiap* hasil pembagian, jumlah item yang ditampilkan di UI harus sama dengan jumlah bagian yang dihasilkan
**Validates: Requirements 1.3, 5.3**

### Property 13: Presisi Integer (Integer Precision)
*Untuk setiap* operasi pembagian, semua hasil harus berupa integer tanpa floating point errors
**Validates: Requirements 6.3**

## Error Handling

### Strategi Error Handling

1. **Input Validation Errors**:
   - Jumlah negatif atau nol: "Jumlah harus lebih besar dari 0"
   - Jumlah terlalu kecil: "Jumlah minimal untuk dibagi adalah Rp 10.000"
   - Format tidak valid: "Masukkan angka yang valid (contoh: 1000000)"

2. **Processing Errors**:
   - Algoritma gagal: "Terjadi kesalahan dalam pembagian, silakan coba lagi"
   - Memory errors: "Jumlah terlalu besar untuk diproses"

3. **UI Errors**:
   - Display errors: Fallback ke format sederhana
   - Event handling errors: Log error dan tampilkan pesan umum

### Error Recovery

- Semua error ditangkap dan tidak menyebabkan crash aplikasi
- User selalu mendapat feedback yang jelas
- State aplikasi direset setelah error
- Log error untuk debugging (optional)

## Testing Strategy

### Dual Testing Approach

Aplikasi ini akan menggunakan kombinasi unit testing dan property-based testing untuk memastikan kebenaran dan keandalan:

**Unit Tests**:
- Test specific examples dan edge cases
- Test integrasi antar komponen
- Test error conditions dengan input spesifik
- Test UI behavior dengan skenario tertentu

**Property-Based Tests**:
- Test universal properties dengan input acak
- Minimum 100 iterasi per property test
- Comprehensive input coverage melalui randomization
- Setiap property test harus reference design document property

**Property Test Configuration**:
- Library: `hypothesis` untuk Python
- Minimum 100 iterations per test
- Tag format: **Feature: money-splitter, Property {number}: {property_text}**
- Setiap correctness property diimplementasikan oleh SATU property-based test

**Unit Testing Focus**:
- Specific examples yang mendemonstrasikan correct behavior
- Integration points antara GUI dan business logic
- Edge cases seperti input boundary values
- Error conditions dengan input spesifik

**Property Testing Focus**:
- Universal properties yang berlaku untuk semua input
- Comprehensive input coverage melalui randomization
- Validasi invariants dan mathematical properties
- Stress testing dengan berbagai kombinasi input

### Test Structure

```python
# Property-based test example
@given(st.integers(min_value=10000, max_value=100000000))
def test_total_conservation(amount):
    """Feature: money-splitter, Property 1: Total conservation"""
    splitter = MoneySplitter()
    result = splitter.split_money(amount)
    assert sum(result.splits) == amount

# Unit test example  
def test_split_10_million_example():
    """Test specific example: 10 million split"""
    splitter = MoneySplitter()
    result = splitter.split_money(10000000)
    assert len(result.splits) in [5, 6]
    assert sum(result.splits) == 10000000
```

Strategi testing ini memastikan bahwa:
- Unit tests menangkap bug konkret dan memvalidasi behavior spesifik
- Property tests memverifikasi correctness umum di semua input
- Kombinasi keduanya memberikan coverage komprehensif