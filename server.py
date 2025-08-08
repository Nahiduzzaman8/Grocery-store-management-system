from flask import Flask, request,jsonify, json, render_template, redirect, url_for
from product_dao import get_all_data_from_product, insert_data_into_product, delete_data_from_product,update_data_in_product
from uom_dao import get_all_uom_names_data_from_uom, get_uom_id
from get_sql_connection import connect_to_db
app = Flask(__name__)
__cnx = connect_to_db()

#dashboard
@app.route('/')
def dashboard():
    return render_template('base.html')



#Products
@app.route("/products")
def products():
    products = get_all_data_from_product((__cnx))
    return render_template("products.html")


@app.route("/add", methods = ["POST", "GET"])
def add():
    if request.method == "POST":
        product_name = request.form.get("name")
        price_per_unit = request.form.get("price_per_unit")
        uom_name = request.form.get("uom_name")
        
        uom_id = get_uom_id(__cnx, uom_name)
        uom_id = uom_id[0][0]
        
        data_tup = (product_name,price_per_unit, uom_id)
        insert_data_into_product(__cnx,data_tup)
    return redirect(url_for("getallproducts"))



@app.route("/delete", methods=["POST"])
def delete():
    id = request.args.get('id') 
    delete_data_from_product(__cnx, id)
    return redirect("/")


@app.route("/update", methods = ["POST"])
def update():
    product_id = request.form['product_id']
    name = request.form['name']
    uom_name = request.form['uom_name']
    price_per_unit = request.form['price_per_unit']
    
    uom_id = get_uom_id(__cnx, uom_name)
    uom_id = uom_id[0][0]
    update_data_in_product(__cnx, ( name, price_per_unit, uom_id, product_id))
    return redirect("/")









##Customer 
@app.route('/customers')
def customers():
    # fetch customer data from DB, e.g. as list of dicts
    #customers_data = get_all_customers_from_db(__cnx)  # your DAO function here
    return render_template('customers.html')



#order
@app.route("/orders")
def orders():
    return render_template('base.html')
    
#settings
@app.route("/settings")
def settings():
    return render_template('base.html')   

    
    
if __name__ == "__main__":
    app.run(debug=True)