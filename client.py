from ftplib import FTP
import ftplib
from flask import Flask, request, render_template, redirect, url_for,session
from functools import wraps
from io import BytesIO
from flask import render_template


app = Flask(__name__)
app.secret_key = "123test"

# Konfigurasi FTP
ftp_host = '127.0.0.1'
ftp_user = 'test'
ftp_password = '123'
ftp_port = 2121

# session["ftp"] = None

def login_ftp(host,port,user,password):
    ftp = FTP()
    try:
        # password = int(password)
        ftp.connect(host=host, port=port)
        ftp.login(user, passwd=password)
        
        ftp.getwelcome()
        
        # ftp.connect(host=ftp_host,port=ftp_port)
        # ftp.login(ftp_user, ftp_password)

        # Check if FTP is logged in\
        
        if ftp.getwelcome():
            return ftp
        else:
            ftp.quit()  # Disconnect from FTP server
            return None
        
    except Exception as e:
        print(f"FTP connection error: {e}")
        return None

def login_required_custom(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        
        if session.get("host") is None:
            # If the user is not logged in, redirect to the login page
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Fungsi untuk mengupload file ke server FTP
def upload_file(file):
    ftp = login_ftp(session["host"],session["port"],session["user"],session["password"])
    
    if ftp :
        # Membaca file dari objek BytesIO
        file_data = file.stream.read()

        # Mengirim file sebagai BytesIO ke server FTP
        ftp.storbinary('STOR {}'.format(file.filename), BytesIO(file_data))

        ftp.quit()
    else :
        return render_template('index.html', error_message='Terjadi kesalahan pada saat login')

# Fungsi untuk mengunduh file dari server FTP
def download_file(file_name):
    ftp = login_ftp(session["host"],session["port"],session["user"],session["password"])
    
    if ftp:
        # Membuka file sebagai BytesIO
        file_data = BytesIO()

        # Mengunduh file dari server FTP ke BytesIO
        ftp.retrbinary('RETR {}'.format(file_name), file_data.write)

        # Mengembalikan data file yang diunduh
        file_data.seek(0)
        return file_data
    else:
        return render_template('index.html', error_message='Terjadi kesalahan pada saat login')
    
# Fungsi untuk mendapatkan daftar file di server FTP
@login_required_custom
def get_file_list():
    ftp = login_ftp(session["host"],session["port"],session["user"],session["password"])
    
    

    files = ftp.nlst()
    ftp.quit()

    return files

def get_current_path():
    ftp = login_ftp(session["host"],session["port"],session["user"],session["password"])
    
    current_path = ftp.pwd()
    return current_path

# Route utama
@app.route('/', methods=['GET', 'POST'])
@login_required_custom
def index():
    # session.clear()
    if request.method == 'POST':
        if 'upload_file' in request.files:
            file = request.files['upload_file']
            if file.filename == '':
                return render_template('index.html', error_message='Mohon pilih file yang ingin diunggah')
            upload_file(file)
            return render_template('uploaded.html')
        elif 'download_file' in request.form:
            file_name = request.form['download_file']
            if file_name == '':
                return render_template('index.html', error_message='Mohon masukkan nama file yang ingin diunduh')
            file_data = download_file(file_name)
            return redirect('/download/{}'.format(file_name))

    file_list = get_file_list()
    return render_template('index.html', file_list=file_list)

# Route unduhan file
@app.route('/download/<path:file_name>')
def download(file_name):
    file_data = download_file(file_name)
    return app.response_class(file_data, mimetype='application/octet-stream', direct_passthrough=True)

# Route setelah mengunggah file
@app.route('/uploaded')
def uploaded():
    return render_template('uploaded.html')

# Route setelah mengunggah file
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session["host"] = str(request.form["host"])
        session["user"] = str(request.form["user"])
        session["password"] = str(request.form["password"])
        session["port"] = int(request.form["port"])
        
        for i in session:
            print(session[i])
        
        ftp = login_ftp(session["host"],session["port"],session["user"],session["password"])
        
        if ftp is None :
            error_message = "Failed to establish FTP connection. Please check your credentials."
            return render_template('login.html', error_message=error_message)
        else: 
            return redirect(url_for("index"))
        
    return render_template('login.html')

# Route ingin melihat file list
@app.route('/ftp')
@login_required_custom
def ftp_file_list():
    file_list = get_file_list()
    current_path = get_current_path()
    return render_template('ftp_file_list.html',path = current_path,file_list=file_list)

# Route for deleting a file
@app.route('/delete/<path:file_name>')
@login_required_custom
def delete_file(file_name):
    ftp = login_ftp(session["host"], session["port"], session["user"], session["password"])

    if ftp:
        try:
            ftp.delete(file_name)
            ftp.quit()
            return redirect(url_for("ftp_file_list"))
        except ftplib.error_perm as e:
            return render_template('ftp_file_list.html', error_message=str(e))
    else:
        return render_template('ftp_file_list.html', error_message='Terjadi kesalahan pada saat login')

# Route for renaming a file
@app.route('/rename/<path:file_name>', methods=['GET', 'POST'])
@login_required_custom
def rename_file(file_name):
    ftp = login_ftp(session["host"], session["port"], session["user"], session["password"])
    part = file_name.split('.')[1]
    print(part)

    if ftp:
        if request.method == 'POST':
            new_name = request.form.get('new_name') + "." + part
            try:
                ftp.rename(file_name, new_name)
                ftp.quit()
                return redirect(url_for("ftp_file_list"))
            except ftplib.error_perm as e:
                return render_template('rename_file.html', error_message=str(e), file_name=file_name)
        else:
            return render_template('rename_file.html', file_name=file_name)
    else:
        return render_template('ftp_file_list.html', error_message='Terjadi kesalahan pada saat login')

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))


if __name__ == '__main__':
    app.run(debug=True)