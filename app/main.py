from flask import Blueprint, render_template, request, session, redirect, url_for, flash
from functools import wraps
from app.models.Users import Users


main = Blueprint('main', 
                 __name__,
                 static_folder='static',
                 template_folder='templates'
                 )

def require_user_session(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if 'user_username' not in session:
            return redirect(url_for('main.index'))
        return f(*args, **kwargs) 
    return wrapper

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        firstname = request.form['firstname']
        middlename = request.form['middlename']
        lastname = request.form['lastname']
        suffix = request.form['suffix']
        email = request.form['email']
        phone_number = request.form['phone_number']
        phone_number2 = request.form.get('phone_number2')
        role = request.form['role']

        try:
            Users.create_user(
                username=username,
                password=password,
                firstname=firstname,
                middlename=middlename,
                lastname=lastname,
                suffix=suffix,
                email=email,
                phone_number=phone_number,
                phone_number2=phone_number2,
                role=role
            )
            return redirect(url_for('main.index'))  # Redirect to a success page
        except Exception as e:
            return f"Error: {e}"

    return render_template('create-user.html')

@main.route('/login', methods=["POST", "GET"])
def login():
    if request.method == "POST":
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()

        if not username or not password:
            flash('Email and password are required.', 'error')
            return redirect(url_for('main.index'))
        user = Users.auth_user(username, password)
        if user is None:
            flash('Invalid username or password', 'error')
            return redirect(url_for('main.index'))

        session['user_username'] = username
        flash('Login successful!', 'success')
        return redirect(url_for('main.dashboard'))

    return render_template('index.html')

@main.route('/dashboard')
@require_user_session
def dashboard():

    return render_template('dashboard.html', username=session['user_username'])

@main.route('/calendar')
@require_user_session
def calendar():
    return render_template('calendar.html', email=session['user_username'])

@main.route('/gallery')
@require_user_session
def gallery():
    
    return render_template('gallery.html', email=session['user_username'])

@main.route('/about')
@require_user_session
def about():
    return render_template('about.html', email=session['user_username'])

@main.route('/thankyou')
@require_user_session
def thankyou():

    return render_template('thankyou.html', email=session['user_username'])

@main.route('/package')
@require_user_session
def package():
    return render_template('package.html', email=session['user_username'])

@main.route('/eventDetails')
@require_user_session
def eventDetails():
    
    return render_template('event-details.html', email=session['user_username'])

@main.route('/manual')
@require_user_session
def manual():
    
    return render_template('manual.html', email=session['user_username'])
    
@main.route('/payment')
@require_user_session
def payment():
    
    return render_template('payment.html', email=session['user_username'])

@main.route('/qrcode')
@require_user_session
def qrcode():
    
    return render_template('qrcode.html', email=session['user_username'])

@main.route('/booking')
@require_user_session
def booking():
    
    return render_template('booking.html', email=session['user_username'])

@main.route('/existingBooking')
@require_user_session
def existingBooking():
    
    return render_template('existingBooking.html', email=session['user_username'])

@main.route('/adminLogin')
@require_user_session
def adminLogin():
    
    return render_template('adminLogin.html', email=session['user_username'])
    
@main.route('/logout')
@require_user_session
def logout():
    session.clear()
    flash('You have been logged out', 'success')
    return redirect(url_for('main.index'))
