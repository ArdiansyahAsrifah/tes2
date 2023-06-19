"# FileBridge" 

Import Modul dan Pustaka:

from ftplib import FTP: Mengimpor kelas FTP dari modul ftplib untuk berinteraksi dengan server FTP.
from flask import Flask, request, render_template, redirect, url_for, session: Mengimpor kelas Flask dan beberapa objek terkait untuk membuat aplikasi web.
from functools import wraps: Mengimpor fungsi wraps untuk mempertahankan metadata fungsi yang didekorasi.
from io import BytesIO: Mengimpor kelas BytesIO untuk membaca dan menulis data file sebagai objek BytesIO.
Membuat Aplikasi Flask:

app = Flask(__name__): Membuat objek aplikasi Flask dengan nama modul saat ini.
app.secret_key = "123test": Mengatur kunci rahasia untuk melindungi data sesi pengguna.
Konfigurasi FTP:

ftp_host, ftp_user, ftp_password, ftp_port: Variabel yang menyimpan informasi konfigurasi server FTP seperti alamat host, username, password, dan port.
Fungsi login_ftp(host, port, user, password):

Membuat objek FTP dan mencoba untuk terhubung ke server FTP menggunakan informasi yang diberikan.
Jika koneksi berhasil, fungsi akan mengembalikan objek FTP yang berhasil terhubung, jika tidak, akan mengembalikan None.
Fungsi login_required_custom(f):

Fungsi dekorator yang memeriksa apakah pengguna sudah masuk atau belum.
Jika pengguna belum masuk, maka akan diarahkan ke halaman login, jika sudah masuk, fungsi yang didekorasi akan dieksekusi.
Fungsi upload_file(file):

Menggunakan objek FTP untuk mengunggah file yang diberikan ke server FTP.
File yang diunggah dibaca sebagai objek BytesIO dan dikirim ke server FTP menggunakan metode storbinary.
Fungsi download_file(file_name):

Menggunakan objek FTP untuk mengunduh file dengan nama yang diberikan dari server FTP.
File yang diunduh disimpan sebagai objek BytesIO dengan menggunakan metode retrbinary.
Fungsi get_file_list():

Menggunakan objek FTP untuk mendapatkan daftar file di server FTP menggunakan metode nlst.
Fungsi get_current_path():

Menggunakan objek FTP untuk mendapatkan jalur saat ini di server FTP menggunakan metode pwd.
Route Utama /:

Digunakan sebagai halaman utama aplikasi.
Jika metode permintaan adalah POST, maka dilakukan pengecekan apakah pengguna ingin mengunggah atau mengunduh file.
Jika pengguna mengunggah file, fungsi upload_file() dipanggil untuk mengunggah file yang dipilih.
Jika pengguna mengunduh file, fungsi download_file() dipanggil untuk mengunduh file yang dipilih.
Jika metode permintaan adalah GET, maka dilakukan pemanggilan fungsi get_file_list() untuk mendapatkan daftar file di server FTP.
Daftar file kemudian ditampilkan di halaman utama menggunakan template HTML.
Route Unduhan File /download/<path:file_name>:

Digunakan untuk mengunduh file dari server FTP.
Fungsi download_file() dipanggil untuk mengunduh file yang diberikan.
Data file yang diunduh kemudian dikirimkan sebagai respons dengan menggunakan app.response_class.
Route Setelah Mengunggah File /uploaded:

Digunakan sebagai halaman setelah pengguna berhasil mengunggah file.
Menampilkan pesan bahwa file telah diunggah menggunakan template HTML.
Route Login /login:

Digunakan sebagai halaman login.
Jika metode permintaan adalah POST, maka dilakukan pengecekan kredensial FTP yang diberikan oleh pengguna menggunakan fungsi login_ftp().
Jika kredensial valid, pengguna akan diarahkan ke halaman utama.
Jika kredensial tidak valid, pesan kesalahan ditampilkan di halaman login.
Jika metode permintaan adalah GET, maka halaman login akan ditampilkan.
Route Logout /logout:

Digunakan untuk keluar dari sesi pengguna.
Data sesi pengguna akan dibersihkan dan pengguna akan diarahkan ke halaman utama.
Route Daftar File FTP /ftp:

Digunakan untuk menampilkan daftar file di server FTP.
Fungsi get_file_list() dipanggil untuk mendapatkan daftar file di server FTP.
Jalur saat ini di server FTP juga ditampilkan.
Daftar file dan jalur saat ini ditampilkan menggunakan template HTML.
Menjalankan Aplikasi:

if __name__ == '__main__': app.run(debug=True): Memastikan bahwa aplikasi hanya dijalankan ketika dijalankan secara langsung (bukan diimpor sebagai modul).
Mengaktifkan mode debug sehingga perubahan dalam kode akan segera terlihat.