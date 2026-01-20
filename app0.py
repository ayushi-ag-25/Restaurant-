from flask import *
import os
from datetime import timedelta
import mysql.connector as ms

# ---------------- DATABASE CONNECTION ----------------
def my_db():
    return ms.connect(
        host=os.environ.get("MYSQLHOST"),
        user=os.environ.get("MYSQLUSER"),
        passwd=os.environ.get("MYSQLPASSWORD"),
        database=os.environ.get("MYSQLDATABASE"),
        port=int(os.environ.get("MYSQLPORT"))
    )

# ---------------- CREATE TABLES (RUN ONCE) ----------------
def init_db():
    mycon = my_db()
    cursor = mycon.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS LOGIN(
        ID INT PRIMARY KEY AUTO_INCREMENT,
        GENDER VARCHAR(10),
        MOBILE BIGINT UNIQUE,
        PASSWORD VARCHAR(20),
        NAME VARCHAR(20),
        MAIL VARCHAR(50)
    ) AUTO_INCREMENT=1000
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS BOOKINGS(
        ID INT,
        NAME VARCHAR(20),
        BID INT PRIMARY KEY AUTO_INCREMENT,
        MOBILE BIGINT,
        DOC DATE,
        TOC TIME,
        TABLETYPE VARCHAR(30),
        REQUEST VARCHAR(500)
    ) AUTO_INCREMENT=1000
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS FEEDBACKS(
        FID INT PRIMARY KEY AUTO_INCREMENT,
        ID INT,
        NAME VARCHAR(20),
        MOBILE BIGINT,
        RATE INT,
        FEEDBACK VARCHAR(500)
    ) AUTO_INCREMENT=1000
    """)

    mycon.commit()
    mycon.close()

# ---------------- FLASK APP ----------------
app = Flask(__name__)
app.secret_key = '123'
app.permanent_session_lifetime = timedelta(days=1)

# ---------------- LOGIN CHECK DECORATOR ----------------
def checklogin(f):
    def wrapper(*args, **kwargs):
        if 'userid' in session:
            return f(*args, **kwargs)
        return redirect(url_for('bookingload'))
    wrapper.__name__ = f.__name__
    return wrapper

# ---------------- ROUTES ----------------
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
        if int(entry[3]) == int(data['pass']):
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
    if cursor.fetchone():
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
    data = request.form
    mycon = my_db()
    cursor = mycon.cursor()
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
    data = request.form
    mycon = my_db()
    cursor = mycon.cursor()

    prompt = 'UPDATE LOGIN SET '
    values = []
    for i, key in enumerate(data):
        if i != 0:
            prompt += ','
        prompt += f'{key.upper()}=%s'
        values.append(int(data[key]) if key == 'mobile' else data[key])

    cursor.execute(prompt + ' WHERE ID=%s', tuple(values) + (session['userid'],))
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

# ---------------- RUN APP ----------------
if __name__ == "__main__":
    init_db()
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port)
