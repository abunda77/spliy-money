# Rencana Implementasi: Money Splitter

## Gambaran Umum

Implementasi aplikasi Money Splitter menggunakan Python dengan GUI Tkinter. Pendekatan implementasi akan membangun komponen secara incremental, dimulai dari logika bisnis inti, kemudian GUI, dan diakhiri dengan integrasi dan testing.

## Tasks

- [x] 1. Setup struktur proyek dan dependencies
  - Buat struktur direktori proyek
  - Setup virtual environment Python
  - Install dependencies (tkinter sudah built-in)
  - Buat file requirements.txt
  - Setup testing framework (pytest, hypothesis)
  - _Requirements: Semua requirements memerlukan struktur proyek yang baik_

- [ ] 2. Implementasi data models dan utilities
  - [x] 2.1 Buat data models (SplitResult, SplitPart)
    - Implementasi dataclass untuk SplitResult dengan method get_total() dan get_percentages()
    - Implementasi dataclass untuk SplitPart
    - _Requirements: 1.2, 5.2_

  - [ ]* 2.2 Write property test untuk data models
    - **Property 1: Konservasi Total**
    - **Validates: Requirements 1.2**

  - [x] 2.3 Implementasi CurrencyFormatter utility
    - Method format_rupiah() untuk formatting mata uang Indonesia
    - Method parse_input() untuk parsing input pengguna
    - _Requirements: 5.1, 5.4_

  - [ ]* 2.4 Write unit tests untuk CurrencyFormatter
    - Test formatting dengan berbagai input
    - Test parsing dengan format yang berbeda
    - _Requirements: 5.1, 5.4_

  - [x] 2.5 Implementasi ValidationUtils
    - Method is_valid_amount() untuk validasi jumlah
    - Method get_error_message() untuk pesan error dalam bahasa Indonesia
    - _Requirements: 1.4, 4.1, 4.2, 4.4_

  - [ ]* 2.6 Write property test untuk ValidationUtils
    - **Property 3: Penolakan Input Invalid**
    - **Validates: Requirements 1.4, 4.1, 4.2**

- [ ] 3. Implementasi algoritma pembagian uang
  - [x] 3.1 Buat class MoneySplitter dengan method split_money()
    - Implementasi algoritma utama untuk membagi uang
    - Method _validate_input() untuk validasi
    - _Requirements: 1.1, 1.2_

  - [ ]* 3.2 Write property test untuk jumlah bagian
    - **Property 2: Jumlah Bagian yang Valid**
    - **Validates: Requirements 1.1**

  - [x] 3.3 Implementasi method _generate_natural_splits()
    - Algoritma untuk generate pembagian yang terlihat natural
    - Hindari angka terlalu bulat
    - _Requirements: 2.1, 2.2, 2.4_

  - [ ]* 3.4 Write property test untuk angka natural
    - **Property 4: Angka Natural**
    - **Validates: Requirements 2.1, 2.2**

  - [ ]* 3.5 Write property test untuk variasi ukuran
    - **Property 6: Variasi Ukuran**
    - **Validates: Requirements 2.4, 3.4**

  - [x] 3.6 Implementasi method _make_amount_natural()
    - Sesuaikan angka agar berakhir dengan ribuan (000)
    - Pastikan tidak terlalu bulat
    - _Requirements: 2.3_

  - [ ]* 3.7 Write property test untuk preferensi ribuan
    - **Property 5: Preferensi Ribuan**
    - **Validates: Requirements 2.3**

- [x] 4. Checkpoint - Test algoritma pembagian
  - Pastikan semua tests untuk algoritma pembagian pass
  - Tanyakan user jika ada pertanyaan

- [ ] 5. Implementasi randomization dan distribusi
  - [x] 5.1 Tambahkan randomization ke MoneySplitter
    - Random choice antara 5 atau 6 bagian
    - Ensure hasil berbeda setiap kali dipanggil
    - _Requirements: 3.1, 3.3_

  - [ ]* 5.2 Write property test untuk randomness
    - **Property 7: Randomness Hasil**
    - **Validates: Requirements 3.1**

  - [ ]* 5.3 Write property test untuk variasi jumlah bagian
    - **Property 9: Variasi Jumlah Bagian**
    - **Validates: Requirements 3.3**

  - [x] 5.4 Implementasi distribusi yang wajar
    - Pastikan tidak ada bagian yang terlalu kecil atau besar
    - _Requirements: 3.2_

  - [ ]* 5.5 Write property test untuk distribusi wajar
    - **Property 8: Distribusi Wajar**
    - **Validates: Requirements 3.2**

- [ ] 6. Implementasi GUI dengan Tkinter
  - [x] 6.1 Buat class MoneySpitterGUI dengan setup dasar
    - Setup main window dan basic layout
    - Buat input field untuk jumlah uang
    - Buat button "Bagi Uang"
    - _Requirements: 1.3, 5.3_

  - [x] 6.2 Implementasi input handling dan validasi
    - Method on_split_button_click() untuk handle button click
    - Validasi input dan tampilkan error jika perlu
    - _Requirements: 1.4, 4.3, 4.4_

  - [x] 6.3 Implementasi display hasil pembagian
    - Method display_results() untuk menampilkan hasil
    - Format hasil dengan pemisah ribuan
    - Tampilkan total untuk verifikasi
    - _Requirements: 1.3, 5.1, 5.2, 5.4_

  - [ ]* 6.4 Write property test untuk kelengkapan display
    - **Property 12: Kelengkapan Display**
    - **Validates: Requirements 1.3, 5.3**

  - [x] 6.5 Implementasi error handling di GUI
    - Method show_error() untuk menampilkan pesan error
    - Pastikan aplikasi tidak crash pada error
    - _Requirements: 4.3_

  - [ ]* 6.6 Write property test untuk stabilitas sistem
    - **Property 10: Stabilitas Sistem**
    - **Validates: Requirements 4.3**

- [ ] 7. Implementasi format dan presisi
  - [x] 7.1 Pastikan semua operasi menggunakan integer arithmetic
    - Hindari floating point errors
    - Validasi bahwa semua hasil adalah integer
    - _Requirements: 6.3_

  - [ ]* 7.2 Write property test untuk presisi integer
    - **Property 13: Presisi Integer**
    - **Validates: Requirements 6.3**

  - [x] 7.3 Implementasi format konsisten untuk semua output
    - Pastikan format mata uang konsisten di seluruh aplikasi
    - _Requirements: 5.1, 5.4_

  - [ ]* 7.4 Write property test untuk format konsisten
    - **Property 11: Format Konsisten**
    - **Validates: Requirements 5.1, 5.4**

- [ ] 8. Integrasi dan wiring komponen
  - [x] 8.1 Integrasikan MoneySplitter dengan GUI
    - Wire business logic dengan UI components
    - Pastikan semua komponen bekerja bersama
    - _Requirements: Semua requirements_

  - [x] 8.2 Implementasi main application entry point
    - Buat main.py untuk menjalankan aplikasi
    - Setup proper application lifecycle
    - _Requirements: Semua requirements_

  - [ ]* 8.3 Write integration tests
    - Test end-to-end flow dari input hingga output
    - Test error scenarios
    - _Requirements: Semua requirements_

- [ ] 9. Final checkpoint dan testing
  - [ ] 9.1 Jalankan semua property-based tests
    - Pastikan semua 13 properties pass dengan 100+ iterations
    - _Requirements: Semua requirements_

  - [~] 9.2 Jalankan semua unit tests
    - Pastikan coverage yang baik untuk edge cases
    - _Requirements: Semua requirements_

  - [~] 9.3 Manual testing aplikasi GUI
    - Test berbagai skenario input
    - Verify UI behavior dan error handling
    - _Requirements: Semua requirements_

- [~] 10. Final checkpoint - Pastikan semua tests pass
  - Pastikan semua tests pass, tanyakan user jika ada pertanyaan

## Notes

- Tasks yang ditandai dengan `*` adalah optional dan bisa dilewati untuk MVP yang lebih cepat
- Setiap task mereferensikan requirements spesifik untuk traceability
- Checkpoints memastikan validasi incremental
- Property tests memvalidasi universal correctness properties
- Unit tests memvalidasi contoh spesifik dan edge cases
- Aplikasi menggunakan integer arithmetic untuk menghindari floating point errors
- GUI menggunakan Tkinter yang sudah built-in di Python