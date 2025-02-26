from flask import Blueprint, render_template, request, session, redirect, url_for, flash, jsonify, current_app
from functools import wraps
from decimal import Decimal
import os
from sqlalchemy.sql import func
from flask_cors import cross_origin
from app.functions import remove_booking_parent_rows
from werkzeug.utils import secure_filename
from app.models import db
from app.models.Users import Users
from datetime import datetime
from app.models.Menu import Menu
from app.models.EventDetails import EventDetails
from app.models.EventMenuChoices import EventMenuChoices
from app.models.Bookings import Bookings
from app.models.Payments import Payments
from app.models.Packages import Packages
from app.models.BlockDates import BlockedDates
from app.models.MenuItems import MenuItems
main = Blueprint('main', 
                 __name__,
                 static_folder='static',
                 template_folder='templates'
                 )


from functools import wraps

    
def require_user_session(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if 'user_username' not in session:
            return redirect(url_for('main.index'))
        return f(*args, **kwargs) 
    return wrapper

def require_admin_login(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        user = get_current_user()
        if not user or user.role != 'admin':  # Ensure user exists and has 'admin' role
            return redirect(url_for('main.dashboard')), 400
        return f(*args, **kwargs)  # Proceed with the decorated function
    return wrapper

@require_user_session
def get_current_user():
    return Users.get_user_by_username(session['user_username'])

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password'].strip()
        password2 = request.form['password2'].strip()
        firstname = request.form['firstname'].strip()
        middlename = request.form['middlename'].strip()
        lastname = request.form['lastname'].strip()
        suffix = request.form['suffix'].strip()
        email = request.form['email'].strip()
        phone_number = request.form['phone_number'].strip()
        phone_number2 = request.form.get('phone_number2').strip()

        if password != password2:
            return render_template('register.html')

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
                role='customer'
            )
            return redirect(url_for('main.index'))  # Redirect to a success page
        except Exception as e:
            return f"Error: {e}"

    return render_template('register.html')

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
    current_user = get_current_user()
    
    total_bookings = Bookings.query.filter_by(user_id=current_user.user_id).count()
    completed_count = Bookings.query.filter_by(user_id=current_user.user_id, status='completed').count()
    to_pay_count = Bookings.query.filter_by(user_id=current_user.user_id, status='to-pay').count()
    processing_count = Bookings.query.filter_by(user_id=current_user.user_id, status='processing').count()
    customer_count = Users.query.filter_by(role='customer').count()
    threshold = 0.6 * total_bookings if total_bookings > 0 else 0
    
    return render_template(
        'dashboard.html', 
        username=session['user_username'],
        current_user=current_user,
        completed_count=completed_count,
        to_pay_count=to_pay_count,
        processing_count=processing_count,
        threshold=threshold,
        customer_count=customer_count
    )

@main.route('/get_dashboard_data')
@require_user_session
@cross_origin()
def get_dashboard_data():
    current_user = get_current_user()

    completed_count = Bookings.query.filter_by(user_id=current_user.user_id, status='completed').count()
    to_pay_count = Bookings.query.filter_by(user_id=current_user.user_id, status='to-pay').count()
    processing_count = Bookings.query.filter_by(user_id=current_user.user_id, status='processing').count()
    customer_count = Users.query.filter_by(role='customer').count()

    return jsonify({
        "completed_count": completed_count,
        "to_pay_count": to_pay_count,
        "processing_count": processing_count,
        "customer_count": customer_count
    })

@main.route('/get_booking_data', methods=['GET'])
@require_user_session
@cross_origin()  # Allows AJAX calls from the frontend
def get_booking_data():
    current_user = get_current_user()
    filter_type = request.args.get('filter', 'weekly')  # Get filter type (default: weekly)

    # Grouping by week, month, or year
    if filter_type == "weekly":
        results = db.session.query(
            func.week(Bookings.created_at).label("week"),
            func.count(Bookings.booking_id).label("count")
        ).filter(Bookings.user_id == current_user.user_id
        ).group_by("week").all()

        labels = [f"Week {row.week}" for row in results]
        values = [row.count for row in results]

    elif filter_type == "monthly":
        results = db.session.query(
            func.month(Bookings.created_at).label("month"),
            func.count(Bookings.booking_id).label("count")
        ).filter(Bookings.user_id == current_user.user_id
        ).group_by("month").all()

        labels = [f"Month {row.month}" for row in results]
        values = [row.count for row in results]

    elif filter_type == "yearly":
        results = db.session.query(
            func.year(Bookings.created_at).label("year"),
            func.count(Bookings.booking_id).label("count")
        ).filter(Bookings.user_id == current_user.user_id
        ).group_by("year").all()

        labels = [str(row.year) for row in results]
        values = [row.count for row in results]

    else:
        return jsonify({"error": "Invalid filter type"}), 400

    return jsonify({"labels": labels, "values": values})

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
    user = get_current_user();

    if user:
        return render_template('package.html', email=session['user_username'], role=user.role)

@main.route('/add_package', methods=['POST'])
@require_admin_login
def add_package():
    if 'package_image' not in request.files:
        return jsonify({'error': 'Image is required'}), 400

    package_name = request.form.get('package_name')
    package_description = request.form.get('package_description')
    package_price = request.form.get('package_price')
    menu_quantity = request.form.get('menu_quantity')
    color_motif = request.form.get('color_motif')
    event_theme = request.form.get('event_theme')
    package_image = request.files['package_image']

    if not package_name or not package_description or not package_price or not menu_quantity or not color_motif or not event_theme:
        return jsonify({'error': 'All fields are required'}), 400

    try:
        filename = secure_filename(package_image.filename)
        upload_folder = current_app.config['UPLOAD_FOLDER']
        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder)

        image_path = os.path.join(upload_folder, filename)
        package_image.save(image_path)

        relative_image_path = f"uploads/{filename}"
        full_image_url = url_for('static', filename=relative_image_path)

        new_package = Packages(
            package_name=package_name,
            description=package_description,
            price=float(package_price),
            color_motif=color_motif,
            event_theme=event_theme,
            menu_quantity=menu_quantity,
            image_path=full_image_url
        )

        db.session.add(new_package)
        db.session.commit()

        return jsonify({
            'success': 'Package added successfully',
            'package_id': new_package.package_id,
            'package_name': package_name,
            'description': package_description,
            'price': package_price,
            'color_motif': color_motif,
            'event_theme': event_theme,
            'menu_quantity': menu_quantity,
            'image_path': full_image_url
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@main.route('/get_packages', methods=['GET'])
def get_packages():
    try:
        packages = Packages.query.all()
        package_counts = (
            db.session.query(Bookings.package_id, func.count(Bookings.package_id))
            .filter(Bookings.package_id.isnot(None))
            .group_by(Bookings.package_id)
            .order_by(func.count(Bookings.package_id).desc())
            .all()
        )

        most_common_package_id = package_counts[0][0] if package_counts else None
        package_list = [
            {
                "package_id": p.package_id,
                "package_name": p.package_name,
                "description": p.description,
                "event_theme": p.event_theme,
                "price": p.price,
                "menu_quantity": p.menu_quantity,
                "image_path": p.image_path or "../static/img/background-main.jpg",
                "is_most_common": p.package_id == most_common_package_id
            }
            for p in packages
        ]

        return jsonify(package_list), 200

    except Exception as e:
        print(e)
        return jsonify({"error": str(e)}), 500

@main.route('/update_package/<int:package_id>', methods=['POST'])
def update_package(package_id):
    data = request.json
    package = Packages.query.get(package_id)

    if not package:
        return jsonify({"error": "Package not found"}), 404

    for key, value in data.items():
        if hasattr(package, key):
            setattr(package, key, value)

    db.session.commit()
    return jsonify({"message": "Package updated successfully!"}), 200

@main.route('/delete_package', methods=['POST'])
@require_admin_login
def delete_package():
    package_id = request.json.get('package_id')
    if not package_id:
        return jsonify({'error': 'Package ID is required'}), 400
    
    response, status = Packages.delete_package(package_id)
    return jsonify(response), status


@main.route('/eventDetails')
@require_user_session
def eventDetails():
    return render_template('event-details.html', email=session['user_username'])

@main.route('/add-menu-choice/<int:event_id>', methods=['POST'])
@require_user_session
def add_menu_choice(event_id):
    try:
        args = request.form
        menu_id = int(args['menus'])
        quantity = int(args['quantity'])

        # Insert the new menu choice into EventMenuChoices
        EventMenuChoices.insert(menu_id=menu_id, event_id=event_id, quantity=quantity)

        # Recalculate the total price for the booking
        total_price = 0
        event_menu_choices = EventMenuChoices.get_all_choices_by_event_id(event_id)
        for choice in event_menu_choices:
            menu = Menu.query.get(choice.menu_id)
            if menu:
                total_price += menu.price * choice.quantity

        # Update the total price in the booking
        booking = Bookings.query.filter_by(event_id=event_id).first()
        if booking:
            booking.total_price = total_price
            db.session.commit()

        flash('Menu item added successfully!')
    except Exception as e:
        db.session.rollback()
        flash(f"Error adding menu item: {str(e)}")

    return redirect(url_for('main.booking_confirmation', event_id=event_id))


@main.route('/update-menu-choice/<int:choice_id>', methods=['POST'])
@require_user_session
def update_menu_choice(choice_id):
    try:
        args = request.form
        new_quantity = int(args['quantity'])

        # Update the quantity in the EventMenuChoices table
        choice = EventMenuChoices.update_choice_quantity(choice_id, new_quantity)
        
        # Recalculate the total price for the booking
        event_id = choice.event_id
        Bookings.update_booking_total_price(event_id)  # Class method to update total price
        
        flash('Menu quantity updated successfully!')
    except Exception as e:
        db.session.rollback()
        flash(f"Error updating menu quantity: {str(e)}")

    return redirect(request.referrer or url_for('main.booking_confirmation', event_id=choice.event_id))


@main.route('/delete-menu-choice/<int:choice_id>', methods=['POST'])
@require_user_session
def delete_menu_choice(choice_id):
    try:
        # Get the choice by ID
        choice = EventMenuChoices.query.get_or_404(choice_id)
        event_id = choice.event_id
        
        # Delete the menu choice using the class method
        EventMenuChoices.delete_choice(choice_id)
        
        # Recalculate and update the total price for the booking after the deletion
        Bookings.update_booking_total_price(event_id)
        
        flash('Menu item removed successfully!')
    except Exception as e:
        db.session.rollback()
        flash(f"Error deleting menu item: {str(e)}")

    return redirect(request.referrer or url_for('main.booking_confirmation', event_id=event_id))

@main.route('/delete-booking/<int:booking_id>', methods=['POST'])
@require_user_session
def delete_booking(booking_id):
    try:
        current_user = get_current_user()
        booking = Bookings.get_booking_by_booking_id(booking_id)
        payment_id = booking.payment_id
        event_id = booking.event_id
        package_id = booking.package_id

        # Prevent unauthorized booking deletion
        if current_user.role != "admin" and booking.user_id != current_user.user_id:
            return jsonify({'success': False, 'message': 'You can only delete your own bookings.'})

        # Remove the booking and associated menu choices
        if not Bookings.delete_booking_with_choices(booking.booking_id):
            return jsonify({'success': False, 'message': 'Failed to delete booking.'})

        # Now call the function to remove parent rows (payment, package, event details)
        if not remove_booking_parent_rows(event_id, package_id, payment_id):
            return jsonify({'success': False, 'message': 'Failed to remove parent rows.'})

        return jsonify({'success': True, 'message': 'Booking deleted successfully!'})
        
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error deleting booking: {str(e)}'})


    except Exception as e:
        flash(f"Error deleting booking: {str(e)}")

    return redirect(url_for('main.booking'))


# New endpoint for admin to delete bookings
@main.route('/delete-booking-by-admin/<int:booking_id>', methods=['POST'])
@require_admin_login
def delete_booking_by_admin(booking_id):
    try:
        booking = Bookings.get_booking_by_booking_id(booking_id)
        payment_id = booking.payment_id
        event_id = booking.event_id
        package_id = booking.package_id

        # Remove the booking and associated menu choices
        if not Bookings.delete_booking_with_choices(booking.booking_id):
            return jsonify({'success': False, 'message': 'Failed to delete booking.'})

        # Call the function to remove parent rows (payment, package, event details)
        if not remove_booking_parent_rows(event_id, package_id, payment_id):
            return jsonify({'success': False, 'message': 'Failed to remove parent rows.'})

        return jsonify({'success': True, 'message': 'Booking deleted successfully!'})
        
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error deleting booking: {str(e)}'})


@main.route("/booking-confirmation/<int:event_id>")
def booking_confirmation(event_id):
    # Retrieve the event by ID to show a confirmation page or summary
    event = EventDetails.query.get(event_id)
    booking = Bookings.get_booking_by_event_id(event_id)
    # Retrieve the menu choices for this event
    event_menu_choices = EventMenuChoices.get_all_choices_by_event_id(event_id)
    # Retrieve all menus and their prices based on the selected items for this event
    selected_menus = []
    total_price = 0
    for choice in event_menu_choices:
        menu = Menu.query.get(choice.menu_id)
        selected_menus.append({
            'choice_id': choice.choice_id,
            'menu_name': menu.menu_name,
            'price': menu.price,
            'quantity': choice.quantity
        })
        total_price += menu.price * choice.quantity
    current_user = get_current_user()
    current_user_active_booking = Bookings.get_active_booking_by_event_and_user(event_id, current_user.user_id)
    all_menus = Menu.get_available_menus_for_event(event_id)
    return render_template("booking-confirmation.html", 
                            current_user_active_booking=current_user_active_booking,
                            all_menus=all_menus,
                            event=event,
                            selected_menus=selected_menus, 
                            total_price=total_price,
                            booking=booking)

@main.route('/eventDetailsManual', methods=['POST', 'GET'])
@require_user_session
def eventDetailsManual():
    current_user = get_current_user()
    if request.method == "POST":
        try:
            args = request.form
            user_id = current_user.user_id

            # Calculate total price
            # Calculate total price
            total_price = sum(
                Menu.query.get(menu_id).price * int(args.get(f'menu_quantities[{menu_id}]', 1))
                for menu_id in args.getlist('menus')
                if Menu.query.get(menu_id)
            )
            
            date_obj = datetime.strptime(args['event_date'], '%Y-%m-%d').date()
            if BlockedDates.get_blocked_date_by_date(date_obj):
                print(f"cannot insert booking in blocked dates")
                return redirect(url_for('main.eventDetailsManual'))

            # Create event
            new_event = EventDetails.insert(
                event_name=args['event_name'],
                number_of_guests=args['event_guest'],
                event_date_obj=date_obj,
                food_time=args['food_delivered'],
                event_location=args['event_location'],
                event_theme=args['theme'],
                event_color=args['color']
            )

            if not new_event or not new_event.event_id:
                print("Failed to create EventDetails")
                return redirect(url_for('main.eventDetailsManual'))

            # Create booking
            new_booking = Bookings.insert(
                user_id=user_id,
                total_price=total_price, 
                status='to-pay',
                event_id=new_event.event_id
            )

            # Add menu choices
            for menu_id in args.getlist('menus'):
                EventMenuChoices.insert(
                    menu_id=menu_id, event_id=new_event.event_id,
                    quantity = int(args.get(f'menu_quantities[{menu_id}]', 1))
                )

            db.session.commit()
            print('Booking created successfully!')
            return redirect(url_for('main.booking_confirmation', 
                                    event_id=new_event.event_id,
                                    booking_id=new_booking.booking_id)
                                    )

        except Exception as e:
            db.session.rollback()
            print(f"Error: {str(e)}")
            return redirect(url_for('main.eventDetailsManual'))

    return render_template('event-details-manual.html', menus=Menu.query.all(), email=session['user_username'])

    
@main.route('/payment', methods=['POST', 'GET'])
@require_user_session
def payment():
    if request.method != 'POST':
        flash("Invalid request method.", "error")
        return redirect(url_for('main.booking_confirmation'))

    # Fetch form data
    booking_id = request.form.get('booking_id')
    payment_method = request.form.get('payment_method')
    reference_no = request.form.get('reference_no')
    current_user = get_current_user()
    try:
        amount = Decimal(request.form.get('amount'))  # Convert amount to Decimal
    except (ValueError, TypeError):
        flash("Invalid payment amount.", "error")
        return redirect(url_for('main.booking_confirmation'))

    # Validate booking
    booking = Bookings.get_booking_by_booking_id(booking_id)
    if not booking:
        flash("Booking not found.", "error")
        return redirect(url_for('main.booking_confirmation'))

    # Validate payment amount
    min_required_payment = booking.total_price / 2

    if amount < min_required_payment:
        flash(f"Amount should be at least 50% ({min_required_payment}).", "warning")
        return redirect(url_for('main.booking_confirmation', event_id=booking.event_id))
    
    if amount > booking.total_price:
        flash(f"Amount should not be above the booking price value ({booking.total_price}).", "warning")
        return redirect(url_for('main.booking_confirmation', event_id=booking.event_id))

    try:
        # Create payment entry
        payment = Payments.create_payment(
            amount=amount,
            payment_method=payment_method,
            reference_no=reference_no
        )

        # Associate payment with the booking
        booking_payment = Bookings.add_payment_to_booking_current_user(
            booking_id=booking_id,
            payment_id=payment.payment_id,
            current_user=current_user.user_id
        )

        flash("Payment received successfully!", "success")
        return redirect(url_for('main.booking_confirmation', event_id=booking_payment.event_id))

    except ValueError as e:
        db.session.rollback()
        flash(str(e), "error")

    return redirect(url_for('main.booking_confirmation', event_id=booking.event_id))


@main.route('/qrcode')
@require_user_session
def qrcode():
    return render_template('qrcode.html', email=session['user_username'])

@main.route('/booking')
@require_user_session
def booking():
    current_user = get_current_user()
    bookings_data = EventDetails.get_user_bookings_with_events(current_user.user_id)

    formatted_bookings = [
        {
            "booking_id": booking_id,
            "status": status,
            "paid_amount": paid_amount,
            "total_price": total_price,
            "payment_id": payment_id,
            "is_paid": payment_status == "completed",  # Check if the payment status is 'paid'
            "event_id": event_id,
            "event_name": event_name,
            "event_date": event_date,
            "food_time": food_time,
            "event_location": event_location,
        }
        for booking_id, status, paid_amount, total_price, payment_id, payment_status, event_id, event_name, event_date, food_time, event_location in bookings_data
    ]

    return render_template('booking.html', 
                           current_user_bookings=formatted_bookings,
                           current_user=current_user
                           )



@main.route('/fetch_bookings')
def fetch_bookings():
    try:
        bookings = (
            db.session.query(Bookings)
            .join(Payments, Payments.payment_id == Bookings.payment_id)
            .filter(Bookings.status == "processing", Payments.payment_status == "completed")
            .all()
        )

        events = []

        for booking in bookings:
            if booking.event_details:  # Ensure event details exist
                event = {
                    "id": booking.booking_id,
                    'event_id': booking.event_details.event_id,
                    "title": f"{booking.event_details.event_name} - {booking.status}",
                    "start": booking.event_details.event_date.strftime("%Y-%m-%dT%H:%M:%S"),
                    "status": booking.status,
                    "total_price": float(booking.total_price),
                }
                events.append(event)

        return jsonify(events)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@main.route('/fetch_blocked_dates', methods=['GET'])
def fetch_blocked_dates():
    try:
        blocked_dates = BlockedDates.get_blocked_dates()
        return jsonify(blocked_dates), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@main.route('/toggle_block_date', methods=['POST'])
@require_admin_login
def toggle_block_date():
    try:
        data = request.get_json()
        date_str = data.get('date')

        if not date_str:
            return jsonify({'error': 'Date is required'}), 400

        date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()

        existing_date = BlockedDates.query.filter_by(date=date_obj).first()

        if existing_date:
            db.session.delete(existing_date)
            db.session.commit()
            return jsonify({'success': 'Date unblocked successfully.', 'date': date_str, 'status': 'unblocked'}), 200
        else:
            blocked_date = BlockedDates(date=date_obj)
            db.session.add(blocked_date)
            db.session.commit()
            return jsonify({'success': 'Date blocked successfully.', 'date': date_str, 'status': 'blocked'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Edit payment details (Amount or Status)
@main.route('/edit_payment/<int:payment_id>', methods=['POST'])
@require_admin_login
def edit_payment(payment_id):
    payment = Payments.query.get(payment_id)
    if not payment:
        return jsonify({'success': False, 'message': 'Payment not found.'}), 404

    data = request.get_json()
    new_amount = data.get('amount')
    new_payment_method = data.get('payment_method')
    new_payment_status = data.get('payment_status')

    if new_amount:
        payment.amount = new_amount
    if new_payment_method:
        payment.payment_method = new_payment_method
    if new_payment_status:
        payment.payment_status = new_payment_status
        # Update booking status based on payment status
        update_booking_status = Bookings.update_booking_status_based_on_payment(payment_id, new_payment_status, payment.amount)
        if not update_booking_status:
            return jsonify({'success': False, 'message': 'booking status not updated.'}), 400


    db.session.commit()

    return jsonify({'success': True, 'message': 'Payment and booking status updated.'})

# Delete payment
@main.route('/delete_payment/<int:payment_id>', methods=['DELETE'])
@require_admin_login
def delete_payment(payment_id):
    payment = Payments.query.get(payment_id)
    if not payment:
        return jsonify({'success': False, 'message': 'Payment not found.'}), 404
    if not Bookings.remove_payment(payment_id):
        return jsonify({'success': False, 'message': 'Booking not yet paid.'}), 404
    db.session.delete(payment)
    db.session.commit()
    
    return jsonify({'success': True})

@main.route('/get_payment_details/<int:payment_id>', methods=['GET'])
@require_admin_login
def get_payment_details(payment_id):
    payment = Payments.query.get(payment_id)
    
    if payment:
        payment_data = {
            'reference_no': payment.reference_no,
            'payment_date': payment.payment_date,
            'payment_method': payment.payment_method,
            'amount': str(payment.amount),
            'payment_status': payment.payment_status
        }
        return jsonify(payment_data)
    
    return jsonify({'error': 'Payment not found'}), 404


@main.route('/manage_bookings')
@require_admin_login
def manage_bookings():
    # Fetch all bookings from the database
    all_bookings = Bookings.query.all()
    for i in all_bookings:
        print(i.events)
    return render_template(
        'manage-bookings.html', 
        username=session['user_username'],
        all_bookings=all_bookings
    )


@main.route('/delete_user/<string:username>', methods=['POST'])  # Use string instead of int
@require_admin_login
def delete_user(username):
    if not username:
        return jsonify({'error': 'Username is required'}), 400
    
    user_deleted = Users.delete_user(username)
    if not user_deleted:
        return jsonify({'error': 'User not found or could not be deleted'}), 400

    return jsonify({"message": "User deleted successfully"}), 200


@main.route('/manage_users')
@require_admin_login
def manage_users():
    all_users = Users.query.all()
    return render_template('manage-users.html', 

                           all_users=all_users)

@main.route('/delete_menu_item/<int:item_id>', methods=['POST'])
@require_admin_login
def delete_menu_item(item_id):
    item = MenuItems.query.get(item_id)
    
    if not item:
        return jsonify({
            'status': 404,
            'message': 'Item not found'
        }), 404  # Return 404 status code if item is not found
    
    # Delete the item
    db.session.delete(item)
    db.session.commit()
    
    return jsonify({
        'status': 200,
        'message': 'Item deleted successfully'
    }), 200  # Return 200 status code when deletion is successful


@main.route('/get_menu/<int:menu_id>', methods=['GET'])
def get_menu(menu_id):
    menu = Menu.query.get(menu_id)
    if not menu:
        return jsonify({"error": "Menu not found"}), 404

    items = MenuItems.query.filter_by(menu_id=menu_id).all()
    item_list = [
        {"item_id": i.item_id, "item_name": i.item_name, "category": i.category}
        for i in items
    ]

    return jsonify({
        "menu_id": menu.menu_id,
        "menu_name": menu.menu_name,
        "description": menu.description,
        "price": menu.price,
        "items": item_list
    })


@main.route('/edit_menu', methods=['POST'])
@require_admin_login
def edit_menu():
    args = request.form
    menu_id = args.get("menu_id")

    # Fetch the menu by ID
    menu = Menu.query.get(menu_id)
    if not menu:
        return jsonify({"message": "Menu not found"}), 404

    # Update the menu details
    menu.menu_name = args["menu_name"]
    menu.description = args["menu_description"]
    menu.price = args["menu_price"]
    db.session.commit()
    print(f"Updated Menu: {menu_id} -> Name: {menu.menu_name}, Description: {menu.description}, Price: {menu.price}")

    # Handle new items being added
    new_index = 0
    while f"new_items[{new_index}][name]" in args:
        new_item_name = args[f"new_items[{new_index}][name]"]
        new_item_category = args[f"new_items[{new_index}][category]"]

        print(f"Adding New Item: Name={new_item_name}, Category={new_item_category}")

        # Add the new item to the menu
        new_item = MenuItems(
            menu_id=menu_id,
            item_name=new_item_name,
            category=new_item_category
        )
        db.session.add(new_item)
        new_index += 1

    # Separate logic for adding new items and updating existing items
    index = 0
    # Handle updating existing items
    while f"existing_items[{index}][id]" in args:
        item_id = args[f"existing_items[{index}][id]"]
        item_name = args[f"existing_items[{index}][name]"]
        item_category = args[f"existing_items[{index}][category]"]

        print(f"Processing Existing Item: ID={item_id}, Name={item_name}, Category={item_category}")

        # Check if item exists
        item = MenuItems.query.get(item_id)
        
        # If the item exists, update it
        if item:
            print(f"Updating existing item with ID={item_id}")
            item.item_name = item_name
            item.category = item_category
        # If the item doesn't exist, add a new one (though this part should not usually be needed)
        else:
            print(f"Item with ID={item_id} not found, creating new item.")
            new_item = MenuItems(
                menu_id=menu_id,
                item_name=item_name,
                category=item_category
            )
            db.session.add(new_item)

        index += 1

    # Commit the changes to the database
    db.session.commit()
    print("Database commit completed.")


    return jsonify({"message": "menu update success"}), 200



@main.route('/delete_menu', methods=['POST'])
@require_admin_login
def delete_menu():
    menu_id = request.json.get('menu_id')
    if not menu_id:
        return jsonify({'error': 'Menu ID is required'}), 400
    
    if not Menu.delete_menu(menu_id):
        return jsonify({'error': 'cannot delete menu'}), 400

    return jsonify({"message": "menu deleteion success"}), 200

@main.route('/add_menu', methods=['POST'])
@require_admin_login
def add_menu():
    args = request.form

    # Insert menu
    menu = Menu.insert(
        menu_name=args['menu_name'],
        description=args['menu_description'],
        price=args['menu_price']
    )

    if not menu:
        return jsonify({"message": "menu insertion failed"}), 400

    # Insert menu items
    menu_items = []
    index = 0
    while f"menu_items[{index}][name]" in args:
        item_name = args[f"menu_items[{index}][name]"]
        category = args[f"menu_items[{index}][category]"]
        
        MenuItems.insert(menu_id=menu.menu_id, item_name=item_name, category=category)
        index += 1

    return jsonify({"message": "menu insertion success"}), 200

    
@main.route('/get_menu_items', methods=['POST'])
@require_admin_login
def get_menu_items():
    menu_id = request.json.get('menu_id')
    if not menu_id:
        return jsonify({'error': 'Menu ID is required'}), 400

    menu_items = MenuItems.query.filter_by(menu_id=menu_id).all()
    if not menu_items:
        return jsonify({'error': 'No items found for this menu.'}), 404

    items = [{'item_id': item.item_id, 'item_name': item.item_name, 'category': item.category} for item in menu_items]
    return jsonify({'menu_items': items}), 200


@main.route('/manage_menus')
@require_admin_login
def manage_menus():
    all_menus = Menu.query.all()
    return render_template('manage-menus.html', 
                           all_menus=all_menus)

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

@main.route('/get_user_details', methods=['GET'])
@require_user_session
def get_user_details():
    user = get_current_user()
    if user:
        return jsonify({
            'username': user.username,
            'user_role': user.role
            })
    return jsonify({'error': 'User not found'}), 404


