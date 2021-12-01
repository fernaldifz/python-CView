# IF3152-2021-G12-CView
## Penjelasan Singkat
CView adalah aplikasi yang digunakan untuk menjadi sebuah alat bantu review Curriculum Vitae (CV) yang dipunyai oleh seorang customer yang nantinya akan di-review oleh seseorang HR yang berada pada bidang tersebut. CView terdiri dari tiga pengguna utama sebagai berikut.
- Tuteers : berfungsi untuk menjadi pemegang CV yang nantinya ingin CV-nya untuk di-review.
- Reviewer : berfungsi untuk melakukan review terhadap CV yang tuteers upload dan nantinya akan mengembalikan feedback dari CV tersebut kepada tuteers.
- Admin : berfungsi untuk melakukan sebuah modifikasi data paket review cv yang disediakan sebelumnya

Aplikasi CView memiliki beberapa fitur penting, yaitu fitur registrasi akun untuk menerima informasi data diri dari pengguna, fitur upload CV yang nantinya akan diteruskan kepada reviewer / HR dan begitu sebaliknya dari reviewer ke tuteers sehingga tuteers juga dapat melihat hasil CV yang telah di-review, fitur email untuk pemberitahuan hasil review melalui email masing - masing tuteers, dan fitur pembayaran digital.

## Cara Menjalankan Aplikasi
Aplikasi CView dapat dijalankan dengan membuka directory IF3152-2021-G12-CView, kemudian menjalankan perintah
```
cd src
python main.py
```
## Daftar Modul yang Diimplementasi
Berikut merupakan daftar modul yang diimplementasi:
- Paket (18219035 - Muhammad Raflie Dwi Putra)
- (((Masukkan Capture Screen)))
- CV Uploader (18219067 - Muhammad Fahrel Naufal A.)
![Modul CV Uploader](https://gitlab.informatika.org/wpo9nine/if3152-2021-g12-cview/-/raw/main/doc/CVUploaderInterface.PNG)
![Modul CV Uploader - Download Review](https://gitlab.informatika.org/wpo9nine/if3152-2021-g12-cview/-/raw/main/doc/CVUploaderReviewDownloadInterface.PNG)
- Pembayaran (18219099 - Fernaldi Fauzie)
![Modul Metode Pembayaran](https://gitlab.informatika.org/wpo9nine/if3152-2021-g12-cview/-/raw/main/doc/metodePembayaranInterface.png)
![Modul Konfirmasi Pembayaran](https://gitlab.informatika.org/wpo9nine/if3152-2021-g12-cview/-/raw/main/doc/konfirmasiPembayaranInterface.png)
- Laporan Pemesanan (18219085 - Muhammad Ilyas Irfan Syiraaj)
- (((Masukkan Capture Screen)))

## Daftar Tabel Basis Data yang Diimplementasi
Berikut merupakan daftar tabel basis data yang diimplementasi:
- Paket
  - ID
  - ID_User
  - ID_Paket
  - Jumlah_CV
  - Durasi
  - Harga
- Pembayaran
  - ID_Pembayaran
  - ID_User
  - Metode_Pembayaran
  - Jumlah_Pembayaran
  - Status_Pembayaran
- Pemesanan
  - ID
  - ID_Tuteers
  - ID_Paket
  - ID_CV
  - ID_Pembayaran
  - Tanggal Pemesanan
- Tuteers
  - id
  - nama
  - username
  - email
  - password
  - phonenumber
  - instansi
  - usia
  - jenis_kelamin
  - id_paket
  - referal_code
  - bukti_pembayaran
  - CV
  - sumber_informasi
  - penawaran_informasi
  - isActive
- cvupload
  - cvid
  - ID_user
  - cvname
  - cvfile
- paketTersedia
  - id_paket
  - jumlah_CV
  - durasi
  - harga
