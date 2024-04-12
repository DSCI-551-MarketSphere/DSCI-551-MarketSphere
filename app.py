from flask import Flask, render_template, request, redirect, session, url_for
from backend.user import *
from backend.product import *
from backend.order import *
import os

app = Flask(__name__, template_folder='frontend')
app.secret_key = os.urandom(24)

@app.route('/')
def home():
    user = get_current_user()
    if user:
        user_role = get_current_user_role()
        if user_role == "admin":
            return redirect('/admin')
        elif user_role == "buyer":
            return redirect('/buyer')
        elif user_role == "seller":
            return redirect('/seller')
    return render_template('home.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup_route():
    if request.method == 'POST':
        email = request.form['email']
        user_name = request.form['user_name']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        password = request.form['password']
        user_role = request.form['user_role']
        success, message = signup(email, user_name, first_name, last_name, password, user_role)
        if success:
            return redirect('/')
        else:
            return render_template('signup.html', error=message)
    return render_template('signup.html')

@app.route('/signin', methods=['GET', 'POST'])
def signin_route():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        success, message = signin(email, password)
        if success:
            user = get_current_user()
            if user:
                user_role = get_current_user_role()
                if user_role == "admin":
                    return redirect('/admin')
                elif user_role == "buyer":
                    return redirect('/buyer')
                elif user_role == "seller":
                    return redirect('/seller')
            else:
                return render_template('signin.html', error="User not found.")
        else:
            return render_template('signin.html', error=message)
    return render_template('signin.html')

@app.route('/logout')
def logout_route():
    logout()
    return render_template('logout.html')


@app.route('/admin', methods=['GET', 'POST'])
def admin_panel():
    if get_current_user_role() == "admin":
        current_admin = get_current_user()
        
        if request.method == 'POST':
            if 'delete_user' in request.form:
                email = request.form['email']
                # user_email = request.form['user_email']
                current_admin.delete_user(email)
        
        users = current_admin.get_all_users()
        products = current_admin.get_all_products()
        orders = current_admin.get_all_orders()
        
        return render_template('admin_panel.html', users=users, products=products, orders=orders)
    else:
        return redirect('/')
    

@app.route('/modify_user', methods=['GET', 'POST'])
def modify_user():
    if get_current_user_role() == "admin":
        if request.method == 'POST':
            email = request.form.get('email')
            user_data = {
                "user_name": request.form.get('user_name'),
                "first_name": request.form.get('first_name'),
                "last_name": request.form.get('last_name'),
                "user_role": request.form.get('user_role')
            }
            current_admin = get_current_user()
            current_admin.modify_user(email, user_data)
            return redirect(url_for('admin_panel'))
        else:
            email = request.args.get('email')
            current_admin = get_current_user()
            success, user_data = current_admin.get_user(email)
            if success:
                return render_template('modify_user.html', user_data=user_data)
            else:
                return redirect(url_for('admin_panel'))
    else:
        return redirect('/')

# @app.route('/modify_user', methods=['GET', 'POST'])
# def modify_user():
#     if get_current_user_role() == "admin":
#         if request.method == 'POST':
#             user_id = request.form['user_id']
#             user_data = {
#                 "email": request.form['email'],
#                 "user_name": request.form['user_name'],
#                 "first_name": request.form['first_name'],
#                 "last_name": request.form['last_name'],
#                 "user_role": request.form['user_role']
#             }
#             current_admin = get_current_user()
#             current_admin.modify_user(user_id, user_data)
#             return redirect(url_for('admin_panel'))
#         else:
#             user_id = request.args.get('user_id')
#             current_admin = get_current_user()
#             # _, user_data = current_admin.get_user(user_id)
#             # return render_template('modify_user.html', user_id=user_id, user_data=user_data)
#             success, user_data = current_admin.get_user(user_id)
#             if success:
#                 return render_template('modify_user.html', user_id=user_id, user_data=user_data)
#             else:
#                 # Handle the case when user data retrieval fails
#                 return redirect(url_for('admin_panel'))
#     else:
#         return redirect('/')

@app.route('/buyer')
def buyer_route():
    if get_current_user_role() == "buyer":
        buyer = get_current_user()
        # Retrieve and pass necessary data to the buyer template
        return render_template('buyer.html', buyer=buyer)
    else:
        return redirect('/')

@app.route('/seller')
def seller_route():
    if get_current_user_role() == "seller":
        seller = get_current_user()
        products = seller.get_my_products()
        return render_template('seller.html', seller=seller, products=products)
    else:
        return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)