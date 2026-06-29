from flask import Flask, render_template, request, redirect, session, send_from_directory
import sqlite3
import os

app = Flask(__name__)
app.secret_key = "GramSevaSecret2026"
# Create database if it doesn't exist
conn = sqlite3.connect('complaints.db')

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS complaints (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    name TEXT,

    mobile TEXT,

    village TEXT,

    address TEXT,

    complaint_type TEXT,

    description TEXT,

    image TEXT,

    video TEXT,

    status TEXT DEFAULT 'Pending'

)
""")

conn.commit()

conn.close()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/complaint')
def complaint():
    return render_template('complaint.html')
@app.route('/admin-login')
def admin_login():
    return render_template('admin_login.html')
@app.route('/admin-auth', methods=['POST'])
def admin_auth():

    password = request.form['password']

    if password == "Muzammil123":
        session['admin'] = True
        return redirect('/admin')

    return "<h2>Wrong Password!</h2>"
@app.route('/submit', methods=['POST'])
def submit():

    name = request.form['name']
    mobile = request.form['mobile']
    village = request.form['village']
    address = request.form['address']
    complaint_type = request.form['complaint_type']
    description = request.form['description']

    image = request.files.get('image')
    video = request.files.get('video')

    image_filename = ""

    if image and image.filename:
        image_filename = image.filename
        os.makedirs("uploads", exist_ok=True)
        image.save(
            os.path.join("uploads", image_filename)
        )
    video_filename = ""

    if video and video.filename:

        video_filename = video.filename
        os.makedirs("uploads/videos", exist_ok=True)
        video.save(
            os.path.join("uploads", "videos", video_filename)
        )

    conn = sqlite3.connect('complaints.db')

    cursor = conn.cursor()

    cursor.execute('''
INSERT INTO complaints
(name, mobile, village, address, complaint_type, description, image, video)
VALUES (?, ?, ?, ?, ?, ?, ?, ?)
''', (
    name,
    mobile,
    village,
    address,
    complaint_type,
    description,
    image_filename,
    video_filename
))

    conn.commit()

    complaint_id = "GSA-2026-" + str(cursor.lastrowid).zfill(4)

    conn.close()

    return render_template(
        'success.html',
        complaint_id=complaint_id
    )
@app.route('/admin')
def admin():

    if not session.get('admin'):
        return redirect('/admin-login')

    conn = sqlite3.connect('complaints.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM complaints")

    complaints = cursor.fetchall()

    print("========== DATABASE ==========")
    print(complaints)
    print("==============================")

    conn.close()

    return render_template(
        'admin.html',
        complaints=complaints
    )
@app.route('/uploads/<filename>')
def uploaded_file(filename):

    return send_from_directory(
        'uploads',
        filename
    )
@app.route('/videos/<filename>')
def uploaded_video(filename):

    return send_from_directory(
        'uploads/videos',
        filename
    )
@app.route('/logout')
def logout():

    session.pop('admin', None)

    return redirect('/admin-login')
if __name__ == "__main__":
    app.run(debug=True)
