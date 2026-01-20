from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from datetime import timedelta
import mysql.connector as ms
import os

# Database connection using environment variables
def my_db():
    mycon = ms.connect(
        user=os.environ.get("DB_USER", "root"),
        host=os.environ.get("DB_HOST", "localhost"),
        passwd=os.environ.get("DB_PASS", ""),
        database=os.environ.get("DB_NAME", "hotel")
    )
    return mycon

# Initialize database tables
def init_db():
    mycon = my_db()
    cursor = mycon.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS LOGIN(
            ID INT PRIMARY KEY AUTO_INCREMENT,
            GENDER VARCHAR(10),
            MOBILE BIGINT UNIQUE,
            PASSWORD VARCHAR(20),
            NAME VARCHAR(20),
            MAIL VARCHAR(50)
        ) AUTO_INCREMENT = 1000
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS BOOKINGS(
            ID INT,
            NAME VARCHAR(20),
            BID INT PRIMARY KEY AUTO_INCREMENT,
            MOBILE BIGINT,
            DOC DATE,
            TOC TIME,
            TABLETYPE VARCHAR(30),
            REQUEST VARCHAR(500)
        ) AUTO_INCREMENT = 1000
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS FEEDBACKS(
            FID INT PRIMARY KEY AUTO_INCREMENT,
            ID INT,
            NAME VARCHAR(20),
            MOBILE BIGINT,
            RATE INT,
            FEEDBACK VARCHAR(500)
        ) AUTO_INCREMENT = 1000
    ''')
    mycon.commit()

# Flask app setup
app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "123")
app.permanent_session_lifetime = timedelta(days=1)

# Login check decorator
def checklogin(f):
    def wrapper(*args, **kwargs):
        if 'userid' in session:
            return f(*args, **kwargs)
        return redirect(url_for('bookingload'))
    wrapper.__name__ = f.__name__
    return wrapper

# Routes
@app.route('/')
def homepage():
    return render_template('hote.html')

@app.route('/book')
def bookingload():
    return render_template('hotelloginpage.html')

@app.route('/register', methods=['GET', 'POST'])
def reg():
    return render_template('register.html')

@app.route('/dashboard')
@checklogin
def dash():
    return render_template('dashboard.html', n=session['name'])

@app.route('/check', methods=['POST'])
def check():
    data = request.get_json()
    mycon = my_db()
    cursor = mycon.cursor()
    cursor.execute('SELECT * FROM LOGIN WHERE MOBILE=%s', (data['mob'],))
    entry = cursor.fetchone()
    response = {'mobexist': 0, 'passmatch': 0}
    if entry:
        response['mobexist'] = 1
        if str(entry[3]) == str(data['pass']):
            session['userid'] = entry[0]
            session['name'] = entry[4]
            response['passmatch'] = 1
    return jsonify(response)

@app.route('/add', methods=['POST'])
def adding():
    data = request.get_json()
    mycon = my_db()
    cursor = mycon.cursor()
    cursor.execute('SELECT * FROM LOGIN WHERE MOBILE=%s', (data['mob'],))
    entry = cursor.fetchone()
    if entry:
        return jsonify({'success': False})
    cursor.execute(
        'INSERT INTO LOGIN(GENDER,MOBILE,PASSWORD,NAME,MAIL) VALUES(%s,%s,%s,%s,%s)',
        (data['gender'], data['mob'], data['pass'], data['name'], data['mail'])
    )
    mycon.commit()
    return jsonify({'success': True})

@app.route('/bookpage')
@checklogin
def bookpage():
    return render_template('booking.html')

@app.route('/booking', methods=['POST'])
@checklogin
def booking():
    data = request.form
    mycon = my_db()
    cursor = mycon.cursor()
    cursor.execute(
        'INSERT INTO BOOKINGS(ID,NAME,MOBILE,DOC,TOC,TABLETYPE,REQUEST) VALUES(%s,%s,%s,%s,%s,%s,%s)',
        (session['userid'], data['name'], data['mob'], data['doc'], data['time'], data['type'], data['req'])
    )
    mycon.commit()
    return redirect(url_for('dash'))

@app.route('/history')
@checklogin
def history():
    mycon = my_db()
    cursor = mycon.cursor()
    cursor.execute('SELECT * FROM BOOKINGS WHERE ID=%s', (session['userid'],))
    data = cursor.fetchall()
    d = [list(i[1:]) for i in data]
    return render_template('historybook.html', d=d)

@app.route('/feedback')
@checklogin
def fedd():
    return render_template('feedback.html')

@app.route('/feedsave', methods=['POST'])
@checklogin
def fed():
    mycon = my_db()
    cursor = mycon.cursor()
    data = request.form
    cursor.execute(
        'INSERT INTO FEEDBACKS(ID,NAME,MOBILE,RATE,FEEDBACK) VALUES(%s,%s,%s,%s,%s)',
        (session['userid'], data['name'], data['mob'], data['rating'], data['message'])
    )
    mycon.commit()
    return redirect(url_for('dash'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('bookingload'))

@app.after_request
def add_no_cache_headers(response):
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, private'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

@app.route('/profile')
@checklogin
def profile():
    mycon = my_db()
    cursor = mycon.cursor()
    cursor.execute('SELECT * FROM LOGIN WHERE ID=%s', (session['userid'],))
    t = list(cursor.fetchone())
    cursor.execute('SELECT * FROM FEEDBACKS WHERE ID=%s', (session['userid'],))
    f = len(cursor.fetchall())
    cursor.execute('SELECT * FROM BOOKINGS WHERE ID=%s', (session['userid'],))
    b = len(cursor.fetchall())
    t.extend([f, b])
    return render_template('profile.html', t=t)

@app.route('/changeprofile', methods=['POST'])
@checklogin
def edit():
    mycon = my_db()
    cursor = mycon.cursor()
    data = request.form
    prompt = 'UPDATE LOGIN SET '
    c = 0
    k = []
    for i in data:
        if c != 0:
            prompt += ','
        prompt += f'{i.upper()}=%s'
        k.append(int(data[i]) if i == 'mobile' else data[i])
        c += 1
    cursor.execute(prompt + ' WHERE ID=%s', tuple(k) + (session['userid'],))
    mycon.commit()
    session['name'] = data['name']
    return redirect(url_for('profile'))

@app.route('/editprofile')
@checklogin
def cedit():
    mycon = my_db()
    cursor = mycon.cursor()
    cursor.execute('SELECT * FROM LOGIN WHERE ID=%s', (session['userid'],))
    data = cursor.fetchone()
    return render_template('editprofile.html', d=data)

# Run the app
if __name__ == "__main__":
    init_db()
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
