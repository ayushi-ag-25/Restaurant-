from flask import *

app=Flask(__name__)

@app.route('/')
def homepage():
    return render_template('hote.html')

@app.route('/book')
def bookingload():
    return render_template('hotelloginpage.html',mes='')

details={}


@app.route('/check',methods=['POST','GET'])
def check():
    if request.method=="POST":
        user=request.form['username1']
        pasw=request.form['pass1']
        if user in details and details[user][0]==pasw:
            return render_template('dashboard.html',name=details[user][1])
        else:
            return render_template('hotelloginpage.html',mes='Invalid username and password')


@app.route('/add',methods=['POST','GET'])
def adding():
    if request.method=="POST":
        user=request.form['username2']
        pasw=request.form['pass2']
        n=request.form['nam']
        details[user]=[pasw,n]
        return render_template('hotelloginpage.html',mes='')

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Use PORT from environment, fallback to 5000 locally
    app.run(host="0.0.0.0", port=port)






















# from flask import *
# from datetime import timedelta
# app=Flask(__name__)

# app.secret_key = "secret123"
# app.permanent_session_lifetime = timedelta(minutes=1)

# @app.route('/login')
# def login():
#     session.permanent = True
#     session['user_id'] = 1
#     return "Logged in for 1 minutes"

# @app.errorhandler(406)
# def forbidden(e):
#     return "Username cannot start with number", 403


# @app.route('/l')
# def g():
#     abort(406,'bdbkwdw')

# @app.route('/')
# def h():
#     return render_template('sigup.html')
# @app.route('/set',methods=['POST','GET'])
# def k():
#     if request.method=='POST':
#         a=request.form
#         an=make_response(render_template('logi.html'))
#         an.set_cookie('username',a['user'])
#         an.set_cookie('password',a['pass'])
#         return an
# @app.route('/log',methods=["POST","GET"])
# def n():
#     if request.method=='POST':
#         a=request.form
#         if a['user']==request.cookies.get('username') and a['pass']==request.cookies.get('password'):
#             return redirect(url_for(login))
#         return "Failure"
    
# app.run(debug=True)


# ############################################3



