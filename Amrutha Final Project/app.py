from flask import Flask, render_template, request, redirect, flash, url_for, session
from models.user import create_user, login as user_login, get_user_by_id
from models.contact import user_contact
# from models.cart import get_cart_items, add_to_cart, remove_from_cart  # Assuming you will create models for cart
import os
from werkzeug.utils import secure_filename
from flask_login import LoginManager, login_required, UserMixin, login_user, logout_user, current_user
from config.config import get_db_connect

app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'development-only-change-me')

#  Setup Flask-Login
login_manager = LoginManager()
login_manager.login_view = 'login_route'
login_manager.init_app(app)

#  Dummy user class wrapper for Flask-Login
class User(UserMixin):
    def __init__(self, id, email_id):
        self.id = id
        self.email_id = email_id

    def get_id(self):
        return str(self.id)

#  Load user for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    user_data = get_user_by_id(user_id)
    if user_data:
        return User(user_data['userID'], user_data['email_id'])
    return None



#  Get current user (custom function for use outside Flask-Login)
def get_current_user():
    user_id = session.get('user_id')
    if user_id:
        return get_user_by_id(user_id)
    return None


#  Utility function to check file extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

#  Home route
@app.route('/')
def index():
    return render_template('home.html', user_logged_in=current_user.is_authenticated)

@app.context_processor
def inject_user():
    return dict(current_user=current_user)


#  Logout route
@app.route('/logout')
def logout():
    logout_user()
    session.clear()
    flash("Logged out successfully", "info")
    return redirect(url_for('index'))

#  User dashboard
@app.route('/user/userdashboard')
@login_required
def user_dashboard():
    return render_template("home.html")

#  About
@app.route('/about')
def about():
    return render_template('user/about.html')

@app.route('/products')
def products():
    return render_template('user/products.html')

#  Services
@app.route('/services')
def services():
    return render_template('user/services.html')

#  Contact
@app.route('/contact')
def contact():
    return render_template('user/contact.html')
# blog
@app.route('/blog')
def blog():
    return render_template('user/blog.html') 

#  Login
@app.route('/user/login', methods=['GET', 'POST'])
def login_route():
    if request.method == 'POST':
        email_id = request.form['email_id']
        password = request.form['password']
        user = user_login(email_id, password)

        if user and user.get('userID'):
            session['user_id'] = user['userID']
            session['email_id'] = user['email_id']
            login_user(User(user['userID'], user['email_id']))
            flash("Login successful", "success")
            return redirect(url_for('user_dashboard'))
        else:
            flash("Invalid email ID or password", "danger")
            return redirect(url_for('login_route'))

    return render_template('user/login.html')

#  Register
@app.route('/user/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email_id = request.form['email_id']
        mobile_no = request.form['mobile_no']
        password = request.form['password']
        confirm = request.form['confirm']
        address = request.form['address']
        usertype = request.form['usertype']

        if password != confirm:
            flash("Passwords do not match", "danger")
            return redirect(url_for('register'))

        result = create_user(first_name, last_name, email_id, mobile_no, password, address, usertype)

        if result == "exists":
            flash("Email or mobile number already exists", "warning")
            return redirect(url_for('register'))
        else:
            flash("User registered successfully. Please login.", "success")
            return redirect(url_for('login_route'))

    return render_template('user/register.html')

#  Profile Route - View and Edit
@app.route('/user/profile', methods=['GET'])
@login_required
def profile():
    user_id = current_user.get_id()
    user = get_user_by_id(user_id)

    return render_template('user/profile.html', user=user)

#  Cart Route
@app.route('/user/cart')
@login_required
def cart():
    user_id = current_user.get_id()
    items = get_cart_items(user_id)
    return render_template('user/cart.html', cart_items=items)

#  Order History Route
@app.route('/user/order-history')
@login_required
def order_history():
    user_id = current_user.get_id()
    orders = get_order_history(user_id)
    return render_template('user/order_history.html', orders=orders)

#  Change Password Route
@app.route('/user/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    if request.method == 'POST':
        old_password = request.form['old_password']
        new_password = request.form['new_password']
        confirm_password = request.form['confirm_password']

        if new_password != confirm_password:
            flash("Passwords do not match", "danger")
            return redirect(url_for('change_password'))

        if update_password(current_user.id, old_password, new_password):
            flash("Password changed successfully", "success")
            return redirect(url_for('user_dashboard'))
        else:
            flash("Incorrect old password", "danger")
            return redirect(url_for('change_password'))

    return render_template('user/change_password.html')

@app.route('/user/update-profile', methods=['GET', 'POST'])
@login_required
def update_profile():
    if request.method == 'POST':
        # Get the form data
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email_id = request.form['email_id']
        mobile_no = request.form['mobile_no']
        address = request.form['address']
        
        # Call the update function in models/user.py
        result = update_user(current_user.id, first_name, last_name, email_id, mobile_no, address)
        
        if result == "updated":
            flash("Profile updated successfully.", "success")
            return redirect(url_for('profile'))  # Redirect to the profile page
        
        flash("Error updating profile. Please try again.", "danger")
    
    # If it's a GET request, display the current user's profile data
    user_data = get_user_by_id(current_user.id)
    return render_template('user/profile.html', user=user_data)


#contact module 
@app.route('/message', methods=['POST'])
def contact_user():
    if request.method == 'POST':
        name=request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')
        user = user_contact(name,email, message)
        flash("message sent  successful", "success")
    return render_template('user/contact.html')

#  Run the app
if __name__ == '__main__':
    app.run(debug=True)
