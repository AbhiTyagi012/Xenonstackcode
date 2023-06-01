from flask import Flask, request,render_template,redirect,session
import mysql.connector
import os

app = Flask(__name__)
app.secret_key=os.urandom(24)

conn = mysql.connector.connect(host="localhost",user="root",password = "",database="login")
cursor = conn.cursor()

@app.route('/')
def login():
    if 'id' in session:
        return render_template('index.html')
    else:
        return render_template('login.html')
    #return render_template('login.html')

@app.route('/register')
def about():
    return render_template('register.html')

@app.route('/home')
def home():
    if 'id' in session:
        return render_template('index.html')
    else:
        return redirect('/')

@app.route('/login_validation', methods = ['POST'])
def login_validation():
    email = request.form.get('email')
    password = request.form.get('password')

    cursor.execute(""" SELECT * FROM `accounts` WHERE `email` LIKE '{}' AND `password` LIKE '{}'""".format(email,password))
    users = cursor.fetchall()
    if len(users)>0:
        session['id']=users[0][0]
        return redirect('/home')
    else:
        return redirect('/')

@app.route('/add_user', methods=['POST'])
def add_user():
    name = request.form.get('uname')
    email = request.form.get('uemail')
    password=request.form.get('upassword')

    cursor.execute("""INSERT INTO `accounts` (`id`, `name`, `email`, `password`) VALUES
    (NULL, '{}','{}','{}')""".format(name,email,password))
    conn.commit()

    cursor.execute("""SELECT * FROM `accounts` WHERE `email` LIKE '{}'""".format(email))
    myuser = cursor.fetchall()
    session['id'] = myuser[0][0]
    return redirect('/home')

@app.route('/logout')
def logout():
    session.pop('id')
    return redirect('/')

@app.route('/contact', methods = ['POST'] )
def contact():
    name = request.form.get('cname')
    email = request.form.get('cemail')
    message = request.form.get('cmessage')

    cursor.execute("""INSERT INTO `query` (`number`, `name`, `email`, `message`) VALUES
        (NULL, '{}','{}','{}')""".format(name, email, message))
    conn.commit()
    return redirect('/')


if __name__ == "__main__":
    app.run(debug=True)