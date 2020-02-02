# import the Flask class from the flask module
from flask import Flask, render_template, redirect, url_for, request
import paramiko
import sqlite3 

# create the application object
app = Flask(__name__)
ssh_client = None

#landing page
@app.route('/')
def home():
    return render_template('index.html') 

#book grabbing page
@app.route('/control', methods=['GET', 'POST'])
def control():
    if(request.method == 'GET'):
        return render_template('control.html')

    if(request.method == 'POST'):
        #connect to turtlebot over ssh and run the grabbing script
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(hostname='pichu',username='pi',password='turtlebot')
        stdin,stdout,stderr=ssh_client.exec_command("cd catkin_ws; source devel/setup.bash; roscd sdp16_test/src; chmod +x *; rosrun sdp16_test pick_up_book.py")
        #return "stdin: " + str(stdin) + "\n" + "stdout: " + str(stdout) + "stderr" + str(stderr)
        return "Book Grabbing in progress."

# login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        #containers for username and password
        un  = request.form['username']
        pwd = request.form['password']

        #connect to database and get users
        conn = sqlite3.connect("webapp.db")
        cursor = conn.execute('select * from users')
        users = [user[0] for user in cursor.description]


        if un != 'admin' or pwd != 'admin':
            error = 'Invalid Credentials. Please try again.'
        else:
            return redirect(url_for('control'))
    return render_template('login.html', error=error)

#runs the code
if __name__ == '__main__':
    app.run(debug=True)
