from flask import Flask, render_template, request
from flask_mysqldb import MySQL

app = Flask(__name__)

# ---------- MySQL Config ----------
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '6363890714'   # change if needed
app.config['MYSQL_DB'] = 'test'

mysql = MySQL(app)

# ---------- LOGIN PAGE ----------
@app.route('/')
def login():
    return render_template('login.html')

# ---------- REGISTER PAGE ----------
@app.route('/register')
def register():
    return render_template('register.html')

# ---------- SAVE USER ----------
@app.route('/save', methods=['POST'])
def save():
    name = request.form['name']
    password = request.form['password']

    cur = mysql.connection.cursor()
    cur.execute(
        "INSERT INTO users (name, password) VALUES (%s, %s)",
        (name, password)
    )
    mysql.connection.commit()
    cur.close()

    return "Registered Successfully"

# ---------- CHECK LOGIN ----------
@app.route('/check', methods=['POST'])
def check():
    name = request.form['name']
    password = request.form['password']

    cur = mysql.connection.cursor()
    cur.execute(
        "SELECT * FROM users WHERE name=%s AND password=%s",
        (name, password)
    )
    user = cur.fetchone()
    cur.close()

    if user:
        return "Login Success"
    else:
        return "Login Failed"

# ---------- RUN ----------
if __name__ == "__main__":
    app.run(debug=True)
