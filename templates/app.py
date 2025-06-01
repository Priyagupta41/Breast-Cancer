from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_cors import CORS

app = Flask(__name__)
app.secret_key = 'your_secret_key'
CORS(app)  # Only needed during development

# Dummy org-only user credentials
users = {
    "orguser1": "password123",
    "admin": "adminpass"
}

@app.route('/')
def login_page():
    return render_template('login.html')  # Your HTML page

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    if username in users and users[username] == password:
        session['user'] = username
        return redirect(url_for('home'))
    else:
        flash('Access denied. Only authorized personnel allowed.')
        return redirect(url_for('login_page'))

@app.route('/home')
def home():
    if 'user' in session:
        return render_template('homenewfinalpage.html')  # This must exist in templates folder
    else:
        return redirect(url_for('login_page'))

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login_page'))

if __name__ == '__main__':
    app.run(debug=True)
