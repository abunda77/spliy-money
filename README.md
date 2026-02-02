# Money Splitter

Aplikasi desktop untuk membagi sejumlah uang menjadi 5 atau 6 bagian secara acak dengan tampilan yang natural untuk keperluan transaksi tunai.

## Fitur

- Membagi uang menjadi 5-6 bagian secara acak
- Hasil pembagian terlihat natural (tidak terlalu bulat)
- Antarmuka grafis yang mudah digunakan
- Validasi input yang komprehensif
- Format mata uang Indonesia (Rupiah)

## Persyaratan Sistem

- Python 3.8 atau lebih baru
- Tkinter (sudah built-in dengan Python)

## Instalasi

1. Clone repository ini:
```bash
git clone <repository-url>
cd money-splitter
```

2. Buat virtual environment (opsional tapi direkomendasikan):
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# atau
venv\Scripts\activate  # Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Cara Penggunaan

Jalankan aplikasi dengan:
```bash
python main.py
```

Atau jika sudah diinstall:
```bash
money-splitter
```

### Menggunakan Aplikasi

1. Masukkan jumlah uang yang ingin dibagi (minimal Rp 10.000)
2. Klik tombol "Bagi Uang"
3. Lihat hasil pembagian di tabel
4. Total akan ditampilkan untuk verifikasi

## Development

### Menjalankan Tests

```bash
# Jalankan semua tests
pytest

# Jalankan dengan coverage
pytest --cov=money_splitter

# Jalankan hanya unit tests
pytest tests/test_*.py -k "not property"

# Jalankan hanya property-based tests
pytest tests/test_properties.py
```

### Struktur Proyek

```
money-splitter/
├── money_splitter/          # Package utama
│   ├── __init__.py
│   ├── models.py           # Data models
│   ├── splitter.py         # Business logic
│   ├── utils.py            # Utility functions
│   └── gui.py              # GUI components
├── tests/                  # Test files
│   ├── __init__.py
│   ├── test_models.py      # Unit tests untuk models
│   ├── test_utils.py       # Unit tests untuk utils
│   ├── test_splitter.py    # Unit tests untuk splitter
│   └── test_properties.py  # Property-based tests
├── main.py                 # Entry point
├── requirements.txt        # Dependencies
├── pytest.ini            # Pytest configuration
├── setup.py               # Package setup
└── README.md              # Dokumentasi
```

## Algoritma

Aplikasi menggunakan algoritma pembagian yang:

1. Memilih secara acak antara 5 atau 6 bagian
2. Membagi jumlah dengan distribusi yang wajar
3. Menyesuaikan hasil agar terlihat natural:
   - Menghindari angka yang terlalu bulat
   - Preferensi untuk angka yang berakhir dengan ribuan (000)
   - Memastikan variasi yang wajar antar bagian
4. Mempertahankan total yang persis sama dengan input

## Testing

Aplikasi menggunakan dual testing approach:

- **Unit Tests**: Test contoh spesifik dan edge cases
- **Property-Based Tests**: Test universal properties dengan input acak

Property yang ditest:
- Konservasi total (total hasil = input)
- Jumlah bagian valid (5 atau 6)
- Penolakan input invalid
- Presisi integer (tidak ada floating point errors)

## Lisensi

MIT License - lihat file LICENSE untuk detail.