from flask import Flask
from flask import render_template
from datetime import datetime
import pymysql
from flaskext.mysql import MySQL
from flask import request   
import traceback  
import werkzeug
import json

app = Flask(__name__)
mysql = MySQL()
 
# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'adminadmin'
app.config['MYSQL_DATABASE_DB'] = 'airline'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)


@app.route('/')
@app.route('/home')
def index():
    return render_template('index.html')

@app.route('/user/<name>')

def user(name):
    return render_template('user.html', name=name)

@app.route('/comments')
def comments():
    comments = ["it", "Hello", "the", "world"]
    return render_template('comments.html', comments=comments)
    
@app.route('/about')

def about():
    return render_template('about.html')

@app.route('/showsignup')
def showsignup():
    """Renders the about page."""
    return render_template(
        'signup.html',
        title='signup',
        year=datetime.now().year,
        message='Your application DB Test  page.'
    )
    
@app.route('/signup')
def signup():
    db = pymysql.connect("localhost","root","adminadmin","airline" )
    cursor = db.cursor()
    sql = "INSERT INTO tbl_user(user_username, user_password, user_email) VALUES ('" +request.args.get('inputName')+ "', '" +request.args.get('inputPassword')+"', '"+ request.args.get('inputEmail') + "')"
    try:
        cursor.execute(sql)
        db.commit()
        return render_template('login.html') 
    except:
        traceback.print_exc()
        db.rollback()
        return "error" , sql
		
    db.close()

    
@app.route('/showlogin' ,methods=['POST','GET'])
def showlogin():
    """Renders the about page."""
    return render_template(
        'login.html',
        title='login',
        year=datetime.now().year,
        message='Your application DB Test  page.'
    )

@app.route('/login')
def getLoginRequest():
    db = pymysql.connect("localhost","root","adminadmin","airline" )
    cursor = db.cursor()
    sql = "select * from tbl_user where user_username='"+request.args.get('inputusername')+"' and user_password='"+request.args.get('inputpw')+"'"
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
        print(len(results))
        if len(results)==1:
            return 'login success'
        else:
            return 'wrong password or user name'
        db.commit()
    except:
        traceback.print_exc()
        db.rollback()
    db.close()

if __name__ == '__main__':
    app.run(debug=True)
    
    