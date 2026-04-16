from flask import Flask, render_template, request, redirect, url_for, session, flash
import json
import os
from datetime import datetime
import threading
import requests
import time

app = Flask(__name__)
app.secret_key = 'super-secret-2024'

STUDENTS_FILE = 'data/students.json'

def init_data():
    os.makedirs('data', exist_ok=True)
    if not os.path.exists(STUDENTS_FILE):
        with open(STUDENTS_FILE, 'w') as f:
            json.dump({}, f)

init_data()

COURSES = {
    'Mathematics': 1500, 'Science': 1600, 'English': 1200,
    'Python': 2000, 'SQL': 1800, 'HTML/CSS': 1700, 'JavaScript': 1900
}

@app.route('/')
def index():
    return render_template('index.html', courses=COURSES)

@app.route('/courses')
def courses():
    return render_template('courses.html', courses=COURSES)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        session['reg_data'] = request.form.to_dict()
        session['otp'] = '123456'  # Demo OTP
        flash('Demo OTP: 123456')
        return redirect(url_for('verify_otp'))
    return render_template('register.html', courses=COURSES)

@app.route('/verify_otp', methods=['GET', 'POST'])
def verify_otp():
    if request.method == 'POST':
        if request.form['otp'] == session.get('otp'):
            data = session['reg_data']
            students = json.load(open(STUDENTS_FILE))
            sid = f"STU{len(students)+1:04d}"
            students[sid] = {**data, 'date': datetime.now().isoformat()}
            json.dump(students, open(STUDENTS_FILE, 'w'))
            session.clear()
            flash('Registered!')
            return redirect(url_for('login'))
        flash('Wrong OTP!')
    return render_template('verify_otp.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['user_email'] = request.form['email']
        return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html', email=session.get('user_email'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)


    

def keep_alive():
    # Replace with your actual Render URL
    URL = "https://apexhive-academy.onrender.com"
    while True:
        try:
            requests.get(URL)
            print("✅ Keep-alive ping sent")
        except Exception as e:
            print(f"❌ Ping failed: {e}")
        time.sleep(840) # 14 minutes

# Start the pinging in a separate thread
threading.Thread(target=keep_alive, daemon=True).start()