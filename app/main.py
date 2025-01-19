from flask import Blueprint, render_template, request, session, redirect, url_for, flash

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
    if request.method == "POST":
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '').strip()

        if not email or not password:
            flash('Email and password are required.', 'error')
            return redirect(url_for('main.index'))

        if email not in users or users.get(email) != password:
            flash('Invalid email or password', 'error')
            return redirect(url_for('main.index'))

        session['user_email'] = email
        flash('Login successful!', 'success')
        return redirect(url_for('main.dashboard'))

    return render_template('index.html')

@main.route('/dashboard')
def dashboard():
    if 'user_email' not in session:
        flash('You must log in to access the dashboard', 'error')
        return redirect(url_for('main.index'))

    return render_template('dashboard.html', email=session['user_email'])

@main.route('/calendar')
def calendar():
    if 'user_email' not in session:
        flash('You must log in to access the dashboard', 'error')
        return redirect(url_for('main.index'))

    return render_template('calendar.html', email=session['user_email'])

@main.route('/gallery')
def gallery():
    if 'user_email' not in session:
        flash('You must log in to access the dashboard', 'error')
        return redirect(url_for('main.index'))

    return render_template('gallery.html', email=session['user_email'])

@main.route('/about')
def about():
    if 'user_email' not in session:
        flash('You must log in to access the dashboard', 'error')
        return redirect(url_for('main.index'))

    return render_template('about.html', email=session['user_email'])

@main.route('/thankyou')
def thankyou():
    if 'user_email' not in session:
        flash('You must log in to access the dashboard', 'error')
        return redirect(url_for('main.index'))

    return render_template('thankyou.html', email=session['user_email'])

@main.route('/package')
def package():
    if 'user_email' not in session:
        flash('You must log in to access the dashboard', 'error')
        return redirect(url_for('main.index'))

    return render_template('package.html', email=session['user_email'])

@main.route('/eventDetails')
def eventDetails():
    if 'user_email' not in session:
        flash('You must log in to access the dashboard', 'error')
        return redirect(url_for('main.index'))

    return render_template('event-details.html', email=session['user_email'])

@main.route('/manual')
def manual():
    if 'user_email' not in session:
        flash('You must log in to access the dashboard', 'error')
        return redirect(url_for('main.index'))

    return render_template('manual.html', email=session['user_email'])
    
@main.route('/payment')
def payment():
    if 'user_email' not in session:
        flash('You must log in to access the dashboard', 'error')
        return redirect(url_for('main.index'))

    return render_template('payment.html', email=session['user_email'])

@main.route('/qrcode')
def qrcode():
    if 'user_email' not in session:
        flash('You must log in to access the dashboard', 'error')
        return redirect(url_for('main.index'))

    return render_template('qrcode.html', email=session['user_email'])

@main.route('/booking')
def booking():
    if 'user_email' not in session:
        flash('You must log in to access the dashboard', 'error')
        return redirect(url_for('main.index'))

    return render_template('booking.html', email=session['user_email'])

@main.route('/existingBooking')
def existingBooking():
    if 'user_email' not in session:
        flash('You must log in to access the dashboard', 'error')
        return redirect(url_for('main.index'))

    return render_template('existingBooking.html', email=session['user_email'])

@main.route('/adminLogin')
def adminLogin():
    if 'user_email' not in session:
        flash('You must log in to access the dashboard', 'error')
        return redirect(url_for('main.index'))

    return render_template('adminLogin.html', email=session['user_email'])
    
@main.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out', 'success')
    return redirect(url_for('main.index'))
