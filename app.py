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


# Highlight: Added format_email function
def format_email(email):
    return email.replace(',', '.')


@app.route('/admin', methods=['GET', 'POST'])
def admin_panel():
    if get_current_user_role() == "admin":
        current_admin = get_current_user()
        
        if request.method == 'POST':
            if 'delete_user' in request.form:
                email = request.form['email']
                current_admin.delete_user(email)
            elif 'delete_product' in request.form:
                item_id = request.form['item_id']
                current_admin.delete_product(item_id)
            elif 'delete_order' in request.form:
                order_id = request.form['order_id']
                current_admin.delete_order(order_id)
        
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

            # Retrieve the updated user data
            updated_user_data = current_admin.get_user(email)

            # Pass the updated user data to the admin_panel route
            return redirect(url_for('admin_panel', updated_user=updated_user_data))

        else:
            email = request.args.get('email')
            current_admin = get_current_user()
            user_data = current_admin.get_user(email)
            if user_data:
                return render_template('modify_user.html', user_data=user_data)
            else:
                return redirect(url_for('admin_panel'))
    else:
        return redirect('/')


@app.route('/insert_user', methods=['GET', 'POST'])
def insert_user():
    if get_current_user_role() == "admin":
        if request.method == 'POST':
            user_data = {
                "email": request.form['email'],
                "user_name": request.form['user_name'],
                "first_name": request.form['first_name'],
                "last_name": request.form['last_name'],
                "sha_hashed_password": hash_password(request.form['password']),
                "user_role": request.form['user_role']
            }
            current_admin = get_current_user()
            current_admin.insert_user(user_data)
            return redirect(url_for('admin_panel'))
        else:
            return render_template('insert_user.html')
    else:
        return redirect('/')


@app.route('/modify_product', methods=['GET', 'POST'])
def modify_product():
    if get_current_user_role() == "admin":
        if request.method == 'POST':
            item_id = request.form['item_id']
            product_data = {
                "item_name": request.form['item_name'],
                "price": request.form['price'],
                "description": request.form['description'],
                "category": request.form['category'],
                "inventory": request.form['inventory']
            }
            current_admin = get_current_user()
            current_admin.modify_product(item_id, product_data)
            return redirect(url_for('admin_panel'))
        else:
            item_id = request.args.get('item_id')
            current_admin = get_current_user()
            product_data = current_admin.get_product(item_id)
            return render_template('modify_product.html', item_id=item_id, product_data=product_data)
    else:
        return redirect('/')


@app.route('/insert_product', methods=['GET', 'POST'])
def insert_product():
    if get_current_user_role() == "admin":
        if request.method == 'POST':
            product_data = {
                "item_name": request.form['item_name'],
                "price": request.form['price'],
                "description": request.form['description'],
                "category": request.form['category'],
                "inventory": request.form['inventory'],
                "seller_id": request.form['seller_id']
            }
            current_admin = get_current_user()
            current_admin.insert_product(product_data)
            return redirect(url_for('admin_panel'))
        else:
            return render_template('insert_product.html')
    else:
        return redirect('/')


@app.route('/modify_order', methods=['GET', 'POST'])
def modify_order():
    if get_current_user_role() == "admin":
        if request.method == 'POST':
            order_id = request.form['order_id']
            order_data = {
                "buyer_id": request.form['buyer_id'],
                "seller_id": request.form['seller_id'],
                "item_id": request.form['item_id'],
                "status": request.form['status']
            }
            current_admin = get_current_user()
            current_admin.modify_order(order_id, order_data)
            return redirect(url_for('admin_panel'))
        else:
            order_id = request.args.get('order_id')
            current_admin = get_current_user()
            order_data = current_admin.get_order(order_id)
            return render_template('modify_order.html', order_id=order_id, order_data=order_data)
    else:
        return redirect('/')


@app.route('/insert_order', methods=['GET', 'POST'])
def insert_order():
    if get_current_user_role() == "admin":
        if request.method == 'POST':
            buyer_id = request.form['buyer_id']
            item_id = request.form['item_id']
            order_data = {
                "buyer_id": buyer_id,
                "seller_id": request.form['seller_id'],
                "item_id": item_id,
                "status": request.form['status']
            }
            current_admin = get_current_user()
            current_admin.insert_order(order_data)
            
            return redirect(url_for('admin_panel'))
        else:
            return render_template('insert_order.html')
    else:
        return redirect('/')



# ====================buyer====================
@app.route('/buyer')
def buyer_route():
    if get_current_user_role() == "buyer":
        buyer = get_current_user()
        category = request.args.get('category')
        search_term = request.args.get('search')
        
        if category:
            success, products = browse_products_by_category(category)
        elif search_term:
            success, products = search_products(search_term)
        else:
            success, products = browse_products_by_category("")  # Retrieve all products
        
        if success:
            return render_template('buyer.html', buyer=buyer, products=products)
        else:
            return render_template('buyer.html', buyer=buyer, products=[])
    else:
        return redirect('/')
    
@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    if get_current_user_role() == "buyer":
        buyer = get_current_user()
        item_id = request.form['item_id']
        success, message = buyer.add_to_cart(item_id)
        return {"success": success, "message": message}
    else:
        return redirect('/')

@app.route('/remove_from_cart', methods=['POST'])
def remove_from_cart():
    if get_current_user_role() == "buyer":
        buyer = get_current_user()
        item_id = request.form['item_id']
        success, message = buyer.remove_from_cart(item_id)
        return {"success": success, "message": message}
    else:
        return redirect('/')
    
@app.route('/make_order', methods=['POST'])
def make_order():
    if get_current_user_role() == "buyer":
        buyer = get_current_user()
        item_id = request.form['item_id']
        success, message = buyer.make_order(item_id)
        return {"success": success, "message": message}
    else:
        return redirect('/')

@app.route('/checkout', methods=['POST'])
def checkout():
    if get_current_user_role() == "buyer":
        buyer = get_current_user()
        success, message = buyer.checkout()
        return {"success": success, "message": message}
    else:
        return redirect('/')



# =================seller======================
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