# import the Flask class from the flask module
from flask import Flask, render_template, redirect, url_for, request
import paramiko

# create the application object
app = Flask(__name__)
ssh_client = None

# use decorators to link the function to a url
@app.route('/')
def home():
    return render_template('index.html')  # return a string

@app.route('/welcome')
def welcome():
    return render_template('welcome.html')  # render a template

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

# Route for handling the login page logic
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Invalid Credentials. Please try again.'
        else:
            return redirect(url_for('home'))
    return render_template('login.html', error=error)

# start the server with the 'run()' method
if __name__ == '__main__':
    app.run(debug=True)
