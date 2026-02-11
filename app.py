from flask import Flask, render_template, request, redirect, session

app = Flask(__name__)
app.secret_key = "secret"

# Dummy users
users = {
    "admin": {"password": "admin123", "role": "admin"},
    "vendor": {"password": "vendor123", "role": "vendor"},
    "user": {"password": "user123", "role": "user"}
}

products = []
orders = []

# INDEX
@app.route("/")
def index():
    return render_template("index.html")

# LOGIN
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if username in users and users[username]["password"] == password:
            session["role"] = users[username]["role"]

            if session["role"] == "admin":
                return redirect("/admin")
            elif session["role"] == "vendor":
                return redirect("/vendor")
            elif session["role"] == "user":
                return redirect("/user")

        return "Invalid Credentials"

    return render_template("login.html")

# ADMIN
@app.route("/admin")
def admin():
    return render_template("admin_dashboard.html")

# VENDOR DASHBOARD
@app.route("/vendor")
def vendor():
    return render_template("vendor_dashboard.html", products=products)

# INSERT PRODUCT
@app.route("/insert_product", methods=["POST"])
def insert_product():
    name = request.form["name"]
    products.append(name)
    return redirect("/vendor")

# DELETE PRODUCT
@app.route("/delete_product/<int:index>")
def delete_product(index):
    if index < len(products):
        products.pop(index)
    return redirect("/vendor")

# USER DASHBOARD
@app.route("/user")
def user():
    return render_template("user_dashboard.html", products=products)

# CART
@app.route("/cart/<product>")
def cart(product):
    return render_template("cart.html", product=product)

# PAYMENT
@app.route("/payment", methods=["POST"])
def payment():
    order = {
        "name": request.form["name"],
        "product": request.form["product"],
        "status": "Received"
    }
    orders.append(order)
    return render_template("payment.html", order=order)

# PRODUCT STATUS (Vendor)
@app.route("/product_status")
def product_status():
    return render_template("product_status.html", orders=orders)

# UPDATE STATUS
@app.route("/update/<int:index>", methods=["GET", "POST"])
def update(index):
    if request.method == "POST":
        new_status = request.form["status"]
        orders[index]["status"] = new_status
        return redirect("/product_status")

    return render_template("update_status.html")

# DELETE ORDER
@app.route("/delete/<int:index>")
def delete(index):
    if index < len(orders):
        orders.pop(index)
    return redirect("/product_status")

# ORDER STATUS (User)
@app.route("/order_status")
def order_status():
    return render_template("order_status.html", orders=orders)

# LOGOUT
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

@app.route("/membership")
def membership():
    return "<h2>Add / Update Membership Page</h2>"

@app.route("/manage_user")
def manage_user():
    return "<h2>Add / Update User Page</h2>"

@app.route("/manage_vendor")
def manage_vendor():
    return "<h2>Add / Update Vendor Page</h2>"

@app.route("/user_management")
def user_management():
    return "<h2>User Management Page</h2>"

@app.route("/vendor_management")
def vendor_management():
    return "<h2>Vendor Management Page</h2>"

@app.route("/add_vendor_membership")
def add_vendor_membership():
    return "<h2>Add Membership for Vendor Page</h2>"

@app.route("/update_vendor_membership")
def update_vendor_membership():
    return "<h2>Update Membership for Vendor Page</h2>"


if __name__ == "__main__":
    app.run(debug=True)
