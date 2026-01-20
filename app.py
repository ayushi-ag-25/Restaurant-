from flask import *
import os
from datetime import timedelta
import mysql.connector as ms

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "123")  # CHANGED
app.permanent_session_lifetime = timedelta(days=1)

# ---------------- DATABASE ----------------
def my_db():
    return ms.connect(
        host=os.environ.get("DB_HOST"),
        user=os.environ.get("DB_USER"),
        password=os.environ.get("DB_PASSWORD"),
        database=os.environ.get("DB_NAME"),
        port=int(os.environ.get("DB_PORT", 3306))
    )

# ---------------- INIT DB ----------------
def init_db():
    con = my_db()
    cur = con.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS LOGIN(
        ID INT PRIMARY KEY AUTO_INCREMENT,
        GENDER VARCHAR(10),
        MOBILE BIGINT UNIQUE,
        PASSWORD VARCHAR(50),   -- CHANGED (safer)
        NAME VARCHAR(20),
        MAIL VARCHAR(50)
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS BOOKINGS(
        BID INT PRIMARY KEY AUTO_INCREMENT,
        ID INT,
        NAME VARCHAR(20),
        MOBILE BIGINT,
        DOC DATE,
        TOC TIME,
        TABLETYPE VARCHAR(30),
        REQUEST VARCHAR(500)
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS FEEDBACKS(
        FID INT PRIMARY KEY AUTO_INCREMENT,
        ID INT,
        NAME VARCHAR(20),
        MOBILE BIGINT,
        RATE INT,
        FEEDBACK VARCHAR(500)
    )
    """)

    con.commit()
    con.close()

# ---------------- LOGIN CHECK ----------------
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

@app.route('/register')
def reg():
    return render_template('register.html')

@app.route('/dashboard')
@checklogin
def dash():
    return render_template('dashboard.html', n=session['name'])

# ---------------- LOGIN ----------------
@app.route('/check', methods=['POST','GET'])
def check():
    data = request.get_json()
    con = my_db()
    cur = con.cursor()

    cur.execute("SELECT * FROM LOGIN WHERE MOBILE=%s", (data['mob'],))
    entry = cur.fetchone()
    con.close()

    res = {'mobexist': 0, 'passmatch': 0}

    if entry:
        res['mobexist'] = 1
        if entry[3] == data['pass']:   # CHANGED (string compare)
            session['userid'] = entry[0]
            session['name'] = entry[4]
            res['passmatch'] = 1

    return jsonify(res)

# ---------------- REGISTER ----------------
@app.route('/add', methods=['POST','GET'])
def adding():
    try:  # CHANGED
        data = request.get_json()
        con = my_db()
        cur = con.cursor()

        cur.execute("SELECT ID FROM LOGIN WHERE MOBILE=%s", (data['mob'],))
        if cur.fetchone():
            return jsonify({'success': False})

        cur.execute("""
            INSERT INTO LOGIN(GENDER,MOBILE,PASSWORD,NAME,MAIL)
            VALUES(%s,%s,%s,%s,%s)
        """, (
            data['gender'],
            data['mob'],
            data['pass'],
            data['name'],
            data['mail']
        ))

        con.commit()
        con.close()
        return jsonify({'success': True})

    except Exception as e:   # CHANGED
        print("ERROR:", e)
        return jsonify({'success': False}), 500

# ---------------- BOOKING ----------------
@app.route('/bookpage')
@checklogin
def bookpage():
    return render_template('booking.html')

@app.route('/booking', methods=['POST'])
@checklogin
def booking():
    d = request.form
    con = my_db()
    cur = con.cursor()

    cur.execute("""
        INSERT INTO BOOKINGS(ID,NAME,MOBILE,DOC,TOC,TABLETYPE,REQUEST)
        VALUES(%s,%s,%s,%s,%s,%s,%s)
    """, (
        session['userid'],
        d['name'],
        d['mob'],
        d['doc'],
        d['time'],
        d['type'],
        d['req']
    ))

    con.commit()
    con.close()
    return redirect(url_for('dash'))

# ---------------- HISTORY ----------------
@app.route('/history')
@checklogin
def history():
    con = my_db()
    cur = con.cursor()
    cur.execute("SELECT * FROM BOOKINGS WHERE ID=%s", (session['userid'],))
    data = [list(i[1:]) for i in cur.fetchall()]
    con.close()
    return render_template('historybook.html', d=data)

# ---------------- FEEDBACK ----------------
@app.route('/feedback')
@checklogin
def fedd():
    return render_template('feedback.html')

@app.route('/feedsave', methods=['POST','GET'])
@checklogin
def fed():
    d = request.form
    con = my_db()
    cur = con.cursor()

    cur.execute("""
        INSERT INTO FEEDBACKS(ID,NAME,MOBILE,RATE,FEEDBACK)
        VALUES(%s,%s,%s,%s,%s)
    """, (
        session['userid'],
        d['name'],
        d['mob'],
        d['rating'],
        d['message']
    ))

    con.commit()
    con.close()
    return redirect(url_for('dash'))

# ---------------- LOGOUT ----------------
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('bookingload'))

# ---------------- PROFILE ----------------
@app.route('/profile')
@checklogin
def profile():
    con = my_db()
    cur = con.cursor()

    cur.execute("SELECT * FROM LOGIN WHERE ID=%s", (session['userid'],))
    t = list(cur.fetchone())

    cur.execute("SELECT COUNT(*) FROM FEEDBACKS WHERE ID=%s", (session['userid'],))
    f = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM BOOKINGS WHERE ID=%s", (session['userid'],))
    b = cur.fetchone()[0]

    con.close()
    t.extend([f, b])
    return render_template('profile.html', t=t)

# ---------------- START ----------------
if __name__ == "__main__":
    init_db()   # runs once on deploy
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
