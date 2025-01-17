from flask import Blueprint, render_template, request, session

main = Blueprint('main', 
                 __name__,
                 static_folder='static',
                 template_folder='templates'
                 )

users = {
    'admin@gmail.com': 'password',
    'admin1': 'password'
}

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/login', methods=["POST", "GET"])
def login():
    email = request.form['email'].strip()
    password = request.form['password'].strip()

    if not email in users:
        if not users.get('email') == password:
            return render_template('index.html')

        return render_template('index.html')

    session['user_email'] = email

    return render_template('dashboard.html')


