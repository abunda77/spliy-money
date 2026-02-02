# Dokumen Persyaratan

## Pengantar

Aplikasi Money Splitter adalah sistem yang memecah sejumlah uang menjadi 5 atau 6 bagian secara acak dengan tampilan yang natural untuk keperluan transaksi tunai. Aplikasi ini dirancang untuk membantu perencanaan transaksi tunai dengan pembagian yang tidak terlihat terlalu bulat atau mencurigakan.

## Glosarium

- **Money_Splitter**: Sistem utama yang melakukan pembagian uang
- **Split_Amount**: Jumlah hasil pembagian individual
- **Natural_Amount**: Jumlah yang terlihat wajar dan tidak terlalu bulat
- **Cash_Transaction**: Transaksi menggunakan uang tunai
- **Random_Generator**: Komponen yang menghasilkan nilai acak

## Persyaratan

### Persyaratan 1: Pembagian Uang Dasar

**User Story:** Sebagai pengguna, saya ingin membagi sejumlah uang menjadi beberapa bagian, sehingga saya dapat merencanakan transaksi tunai dengan lebih baik.

#### Kriteria Penerimaan

1. KETIKA pengguna memasukkan jumlah uang yang valid, MAKA Money_Splitter HARUS membagi jumlah tersebut menjadi 5 atau 6 bagian
2. KETIKA pembagian dilakukan, MAKA Money_Splitter HARUS memastikan total semua Split_Amount sama dengan jumlah input asli
3. KETIKA pembagian selesai, MAKA Money_Splitter HARUS menampilkan semua Split_Amount kepada pengguna
4. KETIKA jumlah input tidak valid atau negatif, MAKA Money_Splitter HARUS menolak input dan memberikan pesan error yang jelas

### Persyaratan 2: Pembagian yang Terlihat Natural

**User Story:** Sebagai pengguna, saya ingin hasil pembagian terlihat natural dan tidak mencurigakan, sehingga cocok untuk transaksi tunai.

#### Kriteria Penerimaan

1. KETIKA Money_Splitter membagi uang, MAKA setiap Split_Amount HARUS terlihat natural dan tidak terlalu bulat
2. KETIKA menghasilkan Split_Amount, MAKA Money_Splitter HARUS menghindari angka yang terlalu bulat seperti 1.000.000, 2.000.000, atau 3.000.000 persis
3. KETIKA menentukan 3 digit terakhir, MAKA Money_Splitter HARUS lebih memilih angka yang berakhir dengan ribuan (000) daripada digit acak
4. KETIKA pembagian dilakukan, MAKA setiap Split_Amount HARUS memiliki variasi yang wajar dalam ukuran

### Persyaratan 3: Randomisasi dan Variasi

**User Story:** Sebagai pengguna, saya ingin setiap pembagian menghasilkan hasil yang berbeda, sehingga pola pembagian tidak dapat diprediksi.

#### Kriteria Penerimaan

1. KETIKA Money_Splitter dipanggil dengan input yang sama berulang kali, MAKA hasil pembagian HARUS berbeda setiap kali
2. KETIKA Random_Generator menghasilkan pembagian, MAKA distribusi ukuran Split_Amount HARUS bervariasi secara wajar
3. KETIKA menentukan jumlah bagian, MAKA Money_Splitter HARUS secara acak memilih antara 5 atau 6 bagian
4. KETIKA menghasilkan Split_Amount, MAKA tidak boleh ada dua Split_Amount yang identik dalam satu pembagian

### Persyaratan 4: Validasi Input dan Error Handling

**User Story:** Sebagai pengguna, saya ingin sistem menangani input yang tidak valid dengan baik, sehingga saya mendapat feedback yang jelas.

#### Kriteria Penerimaan

1. KETIKA pengguna memasukkan jumlah negatif atau nol, MAKA Money_Splitter HARUS menolak input dan memberikan pesan error
2. KETIKA pengguna memasukkan jumlah yang terlalu kecil untuk dibagi, MAKA Money_Splitter HARUS memberikan pesan error yang informatif
3. KETIKA terjadi error dalam proses pembagian, MAKA Money_Splitter HARUS memberikan pesan error yang jelas dan tidak crash
4. KETIKA input berupa format yang tidak valid, MAKA Money_Splitter HARUS memberikan panduan format yang benar

### Persyaratan 5: Format Output yang Mudah Dibaca

**User Story:** Sebagai pengguna, saya ingin hasil pembagian ditampilkan dalam format yang mudah dibaca, sehingga saya dapat dengan mudah memahami dan menggunakan hasilnya.

#### Kriteria Penerimaan

1. KETIKA menampilkan Split_Amount, MAKA Money_Splitter HARUS memformat angka dengan pemisah ribuan yang sesuai
2. KETIKA menampilkan hasil, MAKA Money_Splitter HARUS menunjukkan total keseluruhan untuk verifikasi
3. KETIKA pembagian selesai, MAKA Money_Splitter HARUS menampilkan jumlah bagian yang dihasilkan
4. KETIKA menampilkan hasil, MAKA Money_Splitter HARUS menggunakan mata uang atau format yang konsisten

### Persyaratan 6: Algoritma Pembagian yang Efisien

**User Story:** Sebagai sistem, saya ingin melakukan pembagian dengan algoritma yang efisien, sehingga proses berjalan cepat dan akurat.

#### Kriteria Penerimaan

1. KETIKA melakukan pembagian, MAKA Money_Splitter HARUS menyelesaikan proses dalam waktu yang wajar (kurang dari 1 detik)
2. KETIKA menghasilkan Split_Amount, MAKA algoritma HARUS memastikan tidak ada pembulatan yang menyebabkan kehilangan atau kelebihan uang
3. KETIKA menghitung pembagian, MAKA Money_Splitter HARUS menggunakan aritmatika yang presisi untuk menghindari error floating point
4. KETIKA proses selesai, MAKA total semua Split_Amount HARUS persis sama dengan input asli