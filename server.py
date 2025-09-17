from flask import Flask, request,jsonify, json, render_template, redirect, session, flash,url_for
from get_sql_connection import connect_to_db


from dao_product import get_all_data_from_product ,insert_data_into_product, delete_data_from_product,update_data_in_product
from dao_uom import get_all_uom_names_data_from_uom, get_uom_id_by_using_name
import dao_orders
import dao_customer
import dao_product

from flask_bcrypt import Bcrypt



app = Flask(__name__)
app.secret_key = "supersecret123" 
bcrypt = Bcrypt(app)
__cnx = connect_to_db()

####################################### -------- Login Route ----------###########################################################

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        
        conn = connect_to_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM admin_users WHERE username = %s", (username,))
        user = cursor.fetchone()
        conn.close()
        
    
        if user:
            if (user["password"] == password):
                session["admin"] = user["username"]
                return redirect(url_for("dashboard"))
            
            else:
                flash("Invalid username or password", "error")
            
        else:
            flash("Invalid username or password", "error")

    return render_template("login.html")



####################################### -------- logout Route ----------###########################################################


@app.route("/logout")
def logout():
    if "admin" not in session:
        return redirect(url_for("login"))
    session.pop("admin", None)
    return redirect(url_for("login"))


##########################################---------dashboard----------##############################################################

@app.route("/dashboard")
def dashboard():
    if "admin" not in session:
        return redirect(url_for("login"))
    
    return render_template("dashboard.html")






###################################-----orders-----###########################################################

@app.route("/orders")
def orders():
    if "admin" not in session:
        return redirect(url_for("login"))
    
    orders = dao_orders.get_all_data_from_orders(__cnx)
    return render_template('orders.html', orders = orders)



@app.route("/delete_order", methods=["POST"])
def delete_order():
    if "admin" not in session:
        return redirect(url_for("login"))
    
    order_id = request.args.get('order_id') 
    dao_orders.delete_data_from_orders(__cnx, order_id)
    
    return redirect("/orders")






#############################----------customers----------##################################

@app.route("/customers")
def customers():
    if "admin" not in session:
        return redirect(url_for("login"))
    
    
    customers = dao_customer.get_all_data_from_customers(__cnx)
    return render_template('customers.html', customers = customers)  


@app.route('/update_customer/<int:customer_id>', methods=['GET', 'POST'])
def update_customer(customer_id):
    if "admin" not in session:
        return redirect(url_for("login"))
    
    if request.method == "POST":
        customer_name = request.form['customer_name']
        email = request.form['email']
        contact = request.form['contact']
        address = request.form['address']

        dao_customer.update_data_in_customers(__cnx, ( customer_name, email, contact, address, customer_id))
        return redirect("/customers")
    customer = dao_customer.get_customer_by_id(__cnx, customer_id) 
    return render_template('customers_update.html',customer = customer)



@app.route("/customers/delete/<int:customer_id>", methods=["POST"])
def delete_customer(customer_id):
    if "admin" not in session:
        return redirect(url_for("login"))
    
    cnx = connect_to_db()
    cursor = cnx.cursor(dictionary=True)

    try:
        cursor.execute("SELECT COUNT(*) AS order_count FROM orders WHERE customers_id = %s", (customer_id,))
        result = cursor.fetchone()

        if result["order_count"] > 0:
            customer = dao_customer.get_customer_by_id(cnx, customer_id)
            customer_name = customer['customer_name']
            flash(f"Deletion failed: Customer '{customer_name}' has existing orders.", "error")
            return redirect("/customers")
        
        
        cursor.execute("DELETE FROM customers WHERE customer_id = %s", (customer_id,))
        cnx.commit()
        flash("Customer deleted successfully!", "success")
    except Exception as e:
        flash(f"Error deleting customer: {e}", "error")
    finally:
        cursor.close()
        cnx.close()

    return redirect("/customers")



#################################----------Products----------#########################################
@app.route("/products")
def products():
    if "admin" not in session:
        return redirect(url_for("login"))
    
    products = get_all_data_from_product((__cnx))
    all_uom_names = get_all_uom_names_data_from_uom(__cnx)
    return render_template("products.html", products = products, all_uom_names = all_uom_names)


@app.route("/add_product", methods = ["POST", "GET"])
def add_product():
    if "admin" not in session:
        return redirect(url_for("login"))
    
    uom_names = get_all_uom_names_data_from_uom(__cnx)
    if request.method == "POST":
        product_name = request.form.get("product_name")
        price_per_unit = request.form.get("price_per_unit")
        uom_name = request.form.get("uom_name")
        
        uom_id = get_uom_id_by_using_name(__cnx, uom_name)
        uom_id = uom_id[0][0]
        
        data_tup = (product_name,price_per_unit, uom_id)
        insert_data_into_product(__cnx,data_tup)
        #flash("Added succesfully !!")
        #session['last_added_product'] = product_name
        
        render_template("product_add.html", uom_names= uom_names)
    
    
    
    uom_names = get_all_uom_names_data_from_uom(__cnx)
    return render_template("product_add.html", uom_names= uom_names)


@app.route("/delete_product", methods=["POST"])
def delete_product():
    if "admin" not in session:
        return redirect(url_for("login"))
    
    id = request.args.get('id') 
    delete_data_from_product(__cnx, id)
    
    return redirect("/products")


@app.route('/update_product/<int:product_id>', methods=['GET', 'POST'])
def update_product(product_id):
    if "admin" not in session:
        return redirect(url_for("login"))
    
    if request.method == "POST":
        product_name = request.form['product_name']
        price_per_unit = request.form['price_per_unit']
        uom_name = request.form['uom_name']

        
        uom_id = get_uom_id_by_using_name(__cnx, uom_name)
        uom_id = uom_id['uom_id']
        
        update_data_in_product(__cnx, ( product_name, price_per_unit, uom_id, product_id))
        return redirect("/products")
    
    product = dao_product.get_product_details_using_product_id(__cnx, product_id)
    uom_names = get_all_uom_names_data_from_uom(__cnx)
    return render_template('product_update.html',product = product, uom_names = uom_names)



#################################----------settings----------##################################

@app.route("/settings")
def settings():
    if "admin" not in session:
        return redirect(url_for("login"))
    
    return render_template('settings.html')   



@app.route('/oldpass', methods=['GET', 'POST'])
def oldpass():
    if "admin" not in session:
        return redirect(url_for("login"))

    if request.method == 'POST':
        username = request.form.get('username')
        old_password = request.form.get('old_password')

        conn = connect_to_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM admin_users WHERE username = %s", (username,))
        user = cursor.fetchone()
        conn.close()

        if user and user['password'] == old_password:
            # Pass user ID to next page for updating
            return render_template('new_pass.html', user_id=user['id'])
        else:
            flash("Invalid username or password", "error")
            return redirect(url_for('oldpass'))
        
    return render_template('oldpass.html')


@app.route('/new_pass', methods=['POST'])
def new_pass():
    if "admin" not in session:
        return redirect(url_for("login"))

    user_id = request.form.get('user_id')
    new_password = request.form.get('new_password')
    confirm_password = request.form.get('confirm_password')

    if new_password != confirm_password:
        flash("Passwords do not match", "error")
        return redirect(url_for('oldpass'))

    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE admin_users SET password=%s WHERE id=%s", (new_password, user_id))
    conn.commit()
    conn.close()

    flash("Password updated successfully", "success")
    return redirect(url_for('oldpass'))

@app.route("/option1")
def option1():
    if "admin" not in session:
        return redirect(url_for("login"))
    
    return render_template('settings.html')   
    
####################################################################################  

if __name__ == "__main__":
    app.run(debug=True)
    app = Flask(__name__)
    app.config["DEBUG"] = True
    app.config["TEMPLATES_AUTO_RELOAD"] = True
    
    app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+mysqlconnector://root:root@localhost/gs"


