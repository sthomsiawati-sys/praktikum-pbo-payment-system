# Sistem Pembayaran/Plugin dengan ABC dan Protocol

Praktikum Pemrograman Berorientasi Objek (PBO) — Program Studi Teknologi Informasi, Universitas Tangerang Raya.

## Deskripsi

Inti sistem pembayaran untuk toko kampus online. Inti hanya mengenal **kontrak**, sedangkan setiap metode pembayaran hadir sebagai **plugin** yang dapat ditambah tanpa mengubah kode inti.

- **Abstract Base Class (ABC)** dipakai untuk kontrak metode pembayaran (`PaymentMethod`).
- **Protocol** dipakai untuk kontrak kanal notifikasi (`Notifier`).
- **Registry + dekorator + autodiscovery** dipakai agar plugin baru cukup berupa satu berkas.

## Daftar Isi

1. [Persiapan Lingkungan](#1-persiapan-lingkungan)
2. [Percobaan 1: Kontrak Pembayaran dengan ABC](#2-percobaan-1-kontrak-pembayaran-dengan-abc)
3. [Percobaan 2: Kontrak Notifikasi dengan Protocol](#3-percobaan-2-kontrak-notifikasi-dengan-protocol)
4. [Percobaan 3: Merangkai PaymentProcessor](#4-percobaan-3-merangkai-paymentprocessor)
5. [Percobaan 4: Sistem Plugin dengan Registry](#5-percobaan-4-sistem-plugin-dengan-registry)
6. [Tugas Mandiri 1 sampai 4](#6-tugas-mandiri)
7. [Tugas Bonus](#7-tugas-bonus)
8. [Struktur Proyek Akhir](#8-struktur-proyek-akhir)
9. [Cara Menjalankan](#9-cara-menjalankan)
10. [Kesimpulan](#10-kesimpulan)

---

## 1. Persiapan Lingkungan

- Python 3.10 atau lebih baru (`python --version`), Git, dan VS Code.
- Folder proyek dibuat dan diinisialisasi dengan `git init`.
- Berkas `.gitignore` di folder utama berisi `__pycache__/`, `*.pyc`, `.venv/`, dan `.pytest_cache/`.
- Struktur awal: folder `core/` (dengan `__init__.py` kosong) dan `plugins/`.
- Program selalu dijalankan dari folder yang berisi `main.py`.

---

## 2. Percobaan 1: Kontrak Pembayaran dengan ABC

**Tujuan:** membuat kelas abstrak `PaymentMethod`, membuktikan ia tidak dapat diinstansiasi, lalu membuat subclass konkret pertama.

**Berkas:** `core/utils.py` (`rupiah`, `buat_id`), `core/base.py` (`PembayaranGagal`, `PaymentMethod`), `plugins/transfer_bank.py` (`TransferBank`).

`validasi()` dan `bayar()` bersifat abstrak. `proses()` bersifat konkret dan menjaga urutan langkah (_template method_):

```python
def proses(self, jumlah: float) -> str:
    if jumlah <= 0:
        raise PembayaranGagal("Jumlah pembayaran harus lebih dari 0")
    if not self.validasi(jumlah):
        raise PembayaranGagal(f"{self.nama} menolak pembayaran {rupiah(jumlah)}")
    return self.bayar(jumlah)
```

**Keluaran:**

```
Error yang diharapkan: Can't instantiate abstract class PaymentMethod without an implementation for abstract methods 'bayar', 'validasi'
Error yang diharapkan: Can't instantiate abstract class Setengah without an implementation for abstract method 'bayar'
ID transaksi: TRF-CE5F48E3
Saldo sisa  : 350000
```

**Analisis:**

1. `PaymentMethod("uji")` gagal karena kelas itu masih memiliki method abstrak. Python menolak membuat objek dari kelas abstrak, dan pengecekan ini terjadi sebelum `__init__` dijalankan.
2. `Setengah` hanya mengimplementasikan `validasi()`, sehingga `bayar()` masih abstrak dan `Setengah` sendiri tetap kelas abstrak. Pesan galat hanya menyebut `bayar` karena hanya itu yang belum diimplementasikan.
3. `proses()` ditulis di kelas induk agar urutan langkah konsisten untuk semua subclass, tidak ada duplikasi kode, dan perubahan aturan cukup dilakukan di satu tempat.

---

## 3. Percobaan 2: Kontrak Notifikasi dengan Protocol

**Tujuan:** mendefinisikan `Notifier` sebagai Protocol dan membuktikan bahwa kelas yang **tidak mewarisi** apa pun tetap diakui selama memiliki method `kirim()`.

**Berkas:** `core/protocols.py` (`Notifier` dengan `@runtime_checkable`), `core/notifiers.py` (`ConsoleNotifier`, `EmailNotifier`, `WhatsAppNotifier`).

```python
@runtime_checkable
class Notifier(Protocol):
    def kirim(self, penerima: str, pesan: str) -> None: ...
```

**Keluaran:**

```
ConsoleNotifier  memenuhi Notifier? True
EmailNotifier    memenuhi Notifier? True
WhatsAppNotifier memenuhi Notifier? True
TanpaKirim       memenuhi Notifier? False
```

**Eksperimen tambahan:** setelah `@runtime_checkable` dihapus, `isinstance()` memunculkan
`TypeError: Instance and class checks can only be used with @runtime_checkable protocols`.

**Analisis:**

1. `EmailNotifier` dianggap `Notifier` karena Protocol memakai _structural subtyping_: yang dinilai adalah bentuknya (memiliki method `kirim`), bukan pewarisannya.
2. Tanpa `@runtime_checkable`, `isinstance()` ditolak. Pemeriksaan runtime sengaja dibuat opt-in karena terbatas pada pengecekan nama method. Penegakan utama Protocol ada pada pemeriksa tipe statis (mypy/Pyright).
3. Jika `kirim(self)` tanpa parameter, `isinstance()` tetap `True`, karena pemeriksaan runtime hanya mengecek keberadaan nama method, bukan tanda tangan atau tipe argumen. Masalahnya baru muncul saat method dipanggil.

---

## 4. Percobaan 3: Merangkai PaymentProcessor

**Tujuan:** menyatukan kontrak ABC dan Protocol dalam satu kelas pemroses, serta membuktikan metode bayar dan kanal notifikasi dapat diganti tanpa mengubah pemroses.

**Berkas:** `plugins/ewallet.py` (`EWallet`, batas Rp2.000.000 per transaksi), `core/processor.py` (`PaymentProcessor`).

`PaymentProcessor` memakai tipe kontrak (`PaymentMethod`, `Notifier`), tidak pernah menyebut kelas konkret, dan menerima notifier dari luar (_dependency injection_). Pembayaran yang ditolak ditangkap sebagai `PembayaranGagal`, lalu pelanggan diberi tahu.

**Keluaran:**

```
[CONSOLE] ke andi@utr.ac.id: Pembayaran Rp250.000 via Transfer BCA berhasil. ID: TRF-4E1E4F3E
[CONSOLE] ke andi@utr.ac.id: Pembayaran gagal: E-Wallet GoPay menolak pembayaran Rp150.000
[EMAIL via smtp.kampus.ac.id] ke andi@utr.ac.id: Pembayaran Rp300.000 via E-Wallet DANA berhasil. ID: EWL-C59C322E
Error: notifier harus memiliki method kirim(penerima, pesan)
```

**Analisis:**

1. `checkout()` tidak bergantung pada metode tertentu: ia hanya memakai parameter bertipe `PaymentMethod` dan memanggil `metode.proses(...)` serta `metode.nama`.
2. GoPay Rp150.000 ditolak karena saldo hanya Rp100.000. Keputusan diambil di `EWallet.validasi()`, lalu `proses()` melempar `PembayaranGagal`.
3. `PaymentProcessor` cukup meminta Protocol `Notifier` karena hanya butuh satu kemampuan, `kirim()`. Kode pihak lain yang punya `kirim()` bisa langsung dipakai tanpa mewarisi kelas dasar kita.

---

## 5. Percobaan 4: Sistem Plugin dengan Registry

**Tujuan:** membuat pembuatan objek berbasis kode plugin, sehingga metode pembayaran baru cukup berupa berkas baru.

**Berkas:** `core/registry.py` (`register_plugin`, `daftar_plugin`, `buat_metode`), `plugins/__init__.py` (`muat_semua_plugin`), dekorator `@register_plugin("transfer")` pada `TransferBank` dan `@register_plugin("ewallet")` pada `EWallet`, serta `main.py` versi akhir.

```python
@register_plugin("transfer")
class TransferBank(PaymentMethod):
    ...
```

`main.py` tidak pernah mengimpor `TransferBank` atau `EWallet`; ia hanya memakai kode teks `"transfer"` dan `"ewallet"`.

**Keluaran:**

```
Plugin terdaftar: ['ewallet', 'transfer']
------------------------------------------------------------
[CONSOLE] ke mahasiswa@utr.ac.id: Pembayaran Rp250.000 via Transfer BCA berhasil. ID: TRF-A4678744
[CONSOLE] ke mahasiswa@utr.ac.id: Pembayaran gagal: E-Wallet GoPay menolak pembayaran Rp150.000
[CONSOLE] ke mahasiswa@utr.ac.id: Pembayaran gagal: E-Wallet GoPay menolak pembayaran Rp2.500.000
[PERINGATAN] "Plugin 'qris' tidak ditemukan. Tersedia: ['ewallet', 'transfer']"
------------------------------------------------------------
Riwayat transaksi berhasil:
  TRF-A4678744 │ Transfer BCA │ Rp250.000
```

**Analisis:**

1. Jika `@register_plugin("ewallet")` dihapus, kelas `EWallet` tidak pernah masuk registry (pendaftaran terjadi saat dekorator dijalankan ketika modul diimpor), sehingga plugin `ewallet` menjadi tidak ditemukan.
2. `muat_semua_plugin()` harus dipanggil sebelum `buat_metode()` karena registry awalnya kosong; dekorator baru aktif setelah modul plugin diimpor.
3. Prinsip **Open/Closed**: terbuka untuk penambahan (plugin baru = berkas baru) dan tertutup untuk perubahan (`main.py` dan `core/` tidak diubah).

---

## 6. Tugas Mandiri

### Tugas 1: Plugin QRIS

`plugins/qris.py` dengan kode `"qris"`, batas transaksi Rp5.000.000, dan ID berawalan `QRS`. Dijalankan **tanpa mengubah `main.py` dan `core/`**. Skenario QRIS Rp50.000 berubah dari peringatan menjadi pembayaran berhasil, dan `Plugin terdaftar` memuat tiga kode.

### Tugas 2: `TelegramNotifier` tanpa pewarisan

Ditambahkan di `core/notifiers.py` tanpa mewarisi apa pun. `isinstance(TelegramNotifier(), Notifier)` bernilai `True`, dan kelas ini dapat langsung dipakai `PaymentProcessor`:

```
[TELEGRAM] ke @mahasiswa: Pembayaran Rp50.000 via QRIS Kantin Kampus berhasil. ID: QRS-4CFB0295
```

### Tugas 3: Biaya admin sebagai method abstrak

- `biaya_admin(self, jumlah: float) -> float` ditambahkan sebagai method abstrak pada `PaymentMethod`.
- Dijalankan **sebelum** plugin diubah, hasilnya:
  `TypeError: Can't instantiate abstract class TransferBank without an implementation for abstract method 'biaya_admin'`. Seluruh plugin langsung gagal diinstansiasi karena belum mengimplementasikan kewajiban baru. Inilah harga kontrak yang ketat pada ABC: kewajiban baru langsung terdeteksi di semua turunan.
- Implementasi: transfer bank tetap Rp2.500, e-wallet 1% dari jumlah, QRIS 0,7% dari jumlah.
- `proses()` kini memvalidasi `total = jumlah + biaya_admin(jumlah)`, dan notifikasi sukses menyertakan biaya admin.

```
[CONSOLE] ... Pembayaran Rp250.000 + biaya admin Rp2.500 (total Rp252.500) via Transfer BCA berhasil. ID: TRF-7D09A668
[CONSOLE] ... Pembayaran gagal: E-Wallet GoPay menolak pembayaran Rp150.000 (total dengan biaya admin Rp151.500)
[CONSOLE] ... Pembayaran gagal: E-Wallet GoPay menolak pembayaran Rp2.500.000 (total dengan biaya admin Rp2.525.000)
[CONSOLE] ... Pembayaran Rp50.000 + biaya admin Rp350 (total Rp50.350) via QRIS Kantin Kampus berhasil. ID: QRS-71549972
```

### Tugas 4: Analisis tertulis

Ringkasan (analisis lengkap 200 sampai 300 kata ada di laporan):

- `PaymentMethod` lebih tepat sebagai **ABC** karena satu keluarga kelas yang kita kendalikan dan berbagi logika (`nama`, template method `proses()`); kontrak ditegakkan saat objek dibuat.
- `Notifier` lebih tepat sebagai **Protocol** karena kontraknya kecil (hanya `kirim()`) dan dapat dipenuhi kelas pihak ketiga tanpa pewarisan.
- `PaymentMethod` cocok menjadi Protocol bila metode pembayaran berasal dari banyak SDK eksternal yang tidak dapat diwarisi; `Notifier` cocok menjadi ABC bila semua kanal berbagi kode (log, retry, pembatasan laju).
- Risiko `@runtime_checkable`: `isinstance()` hanya mengecek nama method, bukan tanda tangannya. Dikurangi dengan mypy, anotasi tipe lengkap, dan uji otomatis.

---

## 7. Tugas Bonus

### Bonus 1: Plugin `VirtualAccount`

`plugins/virtual_account.py` dengan kode `"va"`. Tagihan dibuat dulu dengan status **`menunggu`**, dan dapat dibayar sebelum batas waktu (default 24 jam). Status menjadi **`lunas`** setelah dibayar atau **`kedaluwarsa`** setelah batas waktu lewat. Biaya admin tetap Rp4.000. Jam dapat diganti lewat parameter `sekarang` agar mudah diuji.

```
status awal : menunggu
[CONSOLE] ... Pembayaran Rp500.000 + biaya admin Rp4.000 (total Rp504.000) via Virtual Account BNI berhasil. ID: VAC-CB91F402
status akhir: lunas
[CONSOLE] ... Pembayaran gagal: Virtual Account BNI menolak pembayaran Rp500.000 (total dengan biaya admin Rp504.000)
```

### Bonus 2: Uji otomatis dengan pytest

Berkas: `conftest.py` (kosong, di folder utama), `tests/test_abc_dan_registry.py`, `tests/test_virtual_account.py`.

```bash
pytest -v
```

Yang diuji: ABC dan subclass tidak lengkap tidak dapat diinstansiasi, plugin tak dikenal memunculkan `KeyError`, seluruh plugin bawaan terdaftar, dan siklus status Virtual Account. Hasil: seluruh tes `PASSED`.

### Bonus 3: Anotasi tipe dan mypy

```bash
mypy main.py core plugins
```

Anotasi tipe dilengkapi, terutama pada `core/registry.py` (`TypeVar`, `Callable`, `**kwargs: Any`) dan daftar `skenario` di `main.py`.

Galat yang **hanya ditangkap mypy**: kelas `NotifierSalah` dengan `kirim(self)` (tanpa `penerima` dan `pesan`).

- `python uji_mypy.py`: `isinstance: True`, objek `PaymentProcessor` berhasil dibuat tanpa galat.
- `mypy uji_mypy.py`:
  `error: Argument 1 to "PaymentProcessor" has incompatible type "NotifierSalah"; expected "Notifier"`, dengan catatan _Expected `def kirim(self, penerima: str, pesan: str) -> None`_ dan _Got `def kirim(self) -> None`_.

`isinstance()` hanya memeriksa keberadaan nama method, sedangkan mypy membandingkan tanda tangannya.

---

## 8. Cara Menjalankan

```bash
git clone https://github.com/sthomsiawati-sys/praktikum-pbo-payment-system.git
cd praktikum-pbo-payment-system
python main.py
```

Pengujian dan pemeriksaan tipe:

```bash
pip install pytest mypy
pytest -v
mypy main.py core plugins
```

Menambah plugin baru: buat satu berkas di `plugins/` berisi kelas turunan `PaymentMethod` dengan dekorator `@register_plugin("kode")` dan implementasi `validasi`, `bayar`, serta `biaya_admin`. Tidak ada berkas lain yang perlu diubah.

Catatan: `main.py` pada repositori ini adalah versi akhir (Percobaan 4 yang telah dilengkapi Tugas 1 sampai 3). Pada praktikum, isi `main.py` diganti di setiap percobaan, sehingga keluaran Percobaan 1 sampai 3 di atas berasal dari versi `main.py` masing-masing tahap.

---

## 10. Kesimpulan

Praktikum ini menunjukkan bahwa sistem pembayaran dapat dirancang agar mudah berkembang dengan memisahkan inti dari ekstensinya. Inti hanya mengenal dua kontrak: `PaymentMethod` (ABC) untuk metode pembayaran dan `Notifier` (Protocol) untuk kanal notifikasi. Setiap metode pembayaran hadir sebagai plugin, sehingga QRIS dapat ditambahkan tanpa mengubah `main.py` dan `core/`, sesuai prinsip Open/Closed.

ABC bersifat nominal dan ditegakkan saat objek dibuat, sehingga cocok untuk `PaymentMethod` yang berbagi logika lewat _template method_. Protocol bersifat struktural dan cukup memiliki method yang diminta, sehingga cocok untuk `Notifier`, seperti `TelegramNotifier` yang tidak mewarisi apa pun. Pemeriksaan `isinstance()` dengan `@runtime_checkable` hanya mengecek nama method, sehingga `kirim(self)` tanpa parameter tetap lolos, sedangkan mypy menolaknya.
