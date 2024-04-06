import streamlit as st
from backend.user import * 
from backend.order import * 
from backend.product import * 



def main():
    # Sidebar for navigation
    st.sidebar.title("Navigation")
    activities = ["Login", "Manage Users", "Manage Products", "Manage Orders"]
    choice = st.sidebar.selectbox("Select Activity", activities)

    if choice == "Login":
        email = st.sidebar.text_input("Email")
        password = st.sidebar.text_input("Password", type="password")
        if st.sidebar.button("Login"):
            authenticated, message = signin(email, password)
            if authenticated:
                current_admin = get_current_user()
                if current_admin.user_role == "admin":
                    st.success(message)
                else:
                    st.error("Not Admin")
                    current_admin = None
            else:
                st.error(message)
                
    elif choice == "Manage Users":
        if get_current_user_role() == "admin":
            current_admin = get_current_user()
            st.subheader("User Management")
            # Example of fetching and displaying users
            users = current_admin.get_all_users()
            for user_id, user_data in users.items():
                st.write(user_data)
            # Add functionality to insert, modify, delete users
            
    elif choice == "Manage Products":
        if get_current_user_role() == "admin":
            current_admin = get_current_user()
            st.subheader("Product Management")
            # Fetch and display products
            products = current_admin.get_all_products()
            for product_id, product_data in products.items():
                st.write(product_data)
            # Add CRUD functionality for products
            
    elif choice == "Manage Orders":
        if get_current_user_role() == "admin":
            current_admin = get_current_user()
            st.subheader("Order Management")
            # Fetch and display orders
            orders = current_admin.get_all_orders()
            for order_id, order_data in orders.items():
                st.write(order_data)
            # Implement CRUD for orders
            
if __name__ == "__main__":
    main()
