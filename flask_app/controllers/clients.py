from flask_app import app
from flask import redirect,request,render_template,session,flash,url_for
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

import paypalrestsdk

from flask_app.models.client import Client
from flask_app.models.admin import Admin
from flask_app.models.product import Product
from flask_app.models.analyse import Analyse
from flask_app.models.order import Order

@app.route('/')
def index():
    if 'client_id' in session:
        return redirect('/dashboard')
    return redirect('/loginPage')

#kthen login page per client
@app.route('/loginPage')
def loginPage():
    if 'client_id' in session:
        return redirect('/')
    return render_template('login.html')

#kthen register page per client
@app.route('/registerPage')
def registerPage():
    if 'client_id' in session:
        return redirect('/')
    return render_template('register.html')

#ben logimin si client
@app.route('/login', methods = ['POST'])
def login():
    if 'client_id' in session:
        return redirect('/')
    client = Client.get_client_by_email(request.form)
    if not client:
        flash('This email does not exist.', 'emailLogin')
        return redirect(request.referrer)
    if not bcrypt.check_password_hash(client['password'], request.form['password']):
        flash('Your password is wrong!', 'passwordLogin')
        return redirect(request.referrer)
    session['client_id'] = client['id']
    return redirect('/')

#ben regjistrimin si client
@app.route('/register', methods= ['POST'])
def register():
    if 'client_id' in session:
        return redirect('/')
    
    
    if Client.get_client_by_email(request.form):
        flash('This email already exists. Try another one.', 'emailRegister')
        return redirect(request.referrer)
    
    if not Client.validate_user(request.form):
        return redirect(request.referrer)
    
    data = {
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'customer' : request.form['customer'],
        'email': request.form['email'],
        'password': bcrypt.generate_password_hash(request.form['password']),
        'confirmpassword': bcrypt.generate_password_hash(request.form['confirmpassword'])
    }
    Client.create_client(data)
    flash('User succefully created', 'clientRegister')
    return redirect('/')

#dashboard qe kontrollon nqs jemi te loguar ose jo dhe na con te homepage
@app.route('/dashboard')
def dashboard():
    if 'client_id' not in session:
        return redirect('/')
    loggedClientData = {
        'client_id': session['client_id']
    } 
    loggedClient = Client.get_client_by_id(loggedClientData)
    return render_template('homepage.html',loggedClient = Client.get_client_by_id(loggedClientData))


#logout
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/loginPage')


#ketu jane routet per admin
#kthen login page per admin
@app.route('/loginPage/admin')
def loginPageAdmin():
    if 'admin_id' in session:
        return redirect('/')
    return render_template('loginAdmin.html')

#ben login si admin
@app.route('/login/admin', methods = ['POST'])
def loginAdmin():
    if 'admin_id' in session:
        return redirect('/')
    if not Admin.validate_user(request.form):
        return redirect(request.referrer)
    admin = Admin.get_admin_by_email(request.form)
    if not admin:
        flash('This email doesnt exist', 'emailLogin')
        return redirect(request.referrer)
    if not bcrypt.check_password_hash(admin['password'], request.form['password']):
        flash('Incorrect password', 'passwordLogin')
        return redirect(request.referrer)
    
    session['admin_id']= admin['id']
    return redirect('/admin')


#controlleri per adminin dhe shfaq homepage e admin
@app.route('/admin')
def adminPage():
    if 'admin_id' not in session:
        return redirect('/')
    data = {
        'id': session['admin_id']
    }
    admin = Admin.get_admin_by_id(data)
    return render_template('welcomeAdmin.html', loggedAdmin = admin)

#per stock
#kthen stockpage ku admini shton produkte
@app.route('/admin/stockPage')
def adminStock():
    if 'admin_id' not in session:
        return redirect('/')
    return render_template('adminStock.html')

#shton produkte
@app.route('/admin/stock', methods= ['POST'])
def add_stock():
    if 'admin_id' not in session:
        return redirect('/')
    
    if not Product.validate_user(request.form):
        return redirect(request.referrer)

    data = {
        'product_name': request.form['product_name'],
        'quantity': request.form['quantity'],
        'storage' : request.form['storage'],
        'price': request.form['price'],
    }
    Product.create_product(data)
    return redirect('/stock')

#shfaq te gjitha produktet
@app.route('/stock')
def stock():
    
    products = Product.get_all_products()
    return render_template('stock.html',  products = products)

#shfaq edit page

@app.route('/edit/product/<int:id>')
def editProduct(id):
    if 'admin_id' in session:
        data = {
            'admin_id': session['admin_id'],
            'product_id': id
        }
        loggedAdmin = Admin.get_admin_by_id(data)
        product = Product.get_product_by_id(data)
        return render_template('editStock.html', loggedAdmin = loggedAdmin, product= product)
    return redirect('/dashboard')

#update the data of the products

@app.route('/edit/product/<int:id>', methods = ['POST'])
def updateProduct(id):
    if 'admin_id' in session:
        data = {
            'product_id': id
        }
        product = Product.get_product_by_id(data)
        if not Product.validate_user(request.form):
            return redirect(request.referrer)
        if product:
            data = {
                'product_name': request.form['product_name'],
                'quantity': request.form['quantity'],
                'storage' : request.form['storage'],
                'price': request.form['price'],
                'product_id' : id
            }
            Product.update_product(data)
            return redirect('/stock')
        return redirect('/stock')
    return redirect('/stock')



#fshin product nga stock
@app.route('/delete/product/<int:id>')
def remove_product(id):
    if 'admin_id' in session:
        data = {
            'product_id': id
        }
        product = Product.get_product_by_id(data)
        if product:
            Analyse.delete_all_product_analyses(data)
            Product.delete(data)
            return redirect(request.referrer)
        return redirect('/stock')
    return redirect('/stock')




#per analyses
#shfaq add Analyse page 
@app.route('/admin/analysePage')
def adminAnalyse():
    if 'admin_id' not in session:
        return redirect('/')
    return render_template('adminAnalyses.html')

#merr dhe ruan analyses
@app.route('/admin/analyse', methods= ['POST'])
def add_analyse():
    if 'admin_id' not in session:
        return redirect('/')
    
    if not Analyse.validate_user(request.form):
        return redirect(request.referrer)
    data = {
        'product_name': request.form['product_name'],
        'pesticide': request.form['pesticide'],
        'allowed' : request.form['allowed'],
        'allowedAmount': request.form['allowedAmount'],
        'constatedAmount' : request.form['constatedAmount'],
        'control' : request.form['control'],
        'product_id' : request.form['product_id']
    }
    Analyse.create_analyse(data)
    return redirect('/analyses')

#shaq te gjitha rezultatet e analizave
@app.route('/analyses')
def analyse():
    
    analyses = Analyse.get_all_analyses()
    return render_template('analyses.html',  analyses = analyses)

#shfaq edit Analyse page 
@app.route('/edit/analyse/<int:id>')
def editAnalyse(id):
    if 'admin_id' in session:
        data = {
            'admin_id': session['admin_id'],
            'product_id': id,
            'analyse_id' : id
        }
        loggedAdmin = Admin.get_admin_by_id(data)
        product = Product.get_product_by_id(data)
        analyse = Analyse.get_analyse_by_id(data)
        return render_template('editAnalyse.html', loggedAdmin = loggedAdmin, product= product,analyse = analyse)
    return redirect('/analyses')

#Ben update e analyse
@app.route('/edit/analyse/<int:id>', methods = ['POST'])
def updateAnalyse(id):
    if 'admin_id' in session:
        data = {
            'analyse_id': id
        }
        analyse = Analyse.get_analyse_by_id(data)
        if not Analyse.validate_user(request.form):
            return redirect(request.referrer)
        if analyse:
            data = {
                'product_name': request.form['product_name'],
                'pesticide': request.form['pesticide'],
                'allowed' : request.form['allowed'],
                'allowedAmount': request.form['allowedAmount'],
                'constatedAmount' : request.form['constatedAmount'],
                'control' : request.form['control'],
                'product_id' : request.form['product_id'],
                'analyse_id' : id
            }
            Analyse.update_analyse(data)
            return redirect('/analyses')
        return redirect('/analyses')
    return redirect('/analyses') 

#fshin analyse nga analyses
@app.route('/delete/analyse/<int:id>')
def remove_analyse(id):
    if 'admin_id' in session:
        data = {
            'analyse_id': id
        }
        analyse = Analyse.get_analyse_by_id(data)
        if analyse:
            Analyse.delete_analyse(data)
            return redirect(request.referrer)
        return redirect('/analyses')
    return redirect('/analyses')

#shfaq template kur haset ndonje error
@app.errorhandler(404)
def invalid_route(e):
     return render_template("404.html")

#shfaq template ku ndodhen partneret
@app.route('/partners')
def partners():
    return render_template('partners.html')

#per order
#kthen orderpage ku client ben porosi
@app.route('/client/orderPage')
def order():
    if 'client_id' not in session:
        return redirect('/')
    products = Product.get_all_products()
    loggedClientData = {
        'client_id': session['client_id']
    } 
    loggedClient = Client.get_client_by_id(loggedClientData)
    return render_template('order.html', products = products,loggedClient = loggedClient )


#ben order
@app.route('/client/order', methods= ['POST'])
def add_order():
    if 'client_id' not in session:
        return redirect('/')
    
    if not Order.validate_user(request.form):
        return redirect(request.referrer)


    data = {
        'customer': request.form['customer'],
        'product_name': request.form['product_name'],
        'quantity': request.form['quantity'],
        'location' : request.form['location'],
        'product_id' : request.form['product_id'],
        'client_id': session['client_id']
    }


    Order.make_order(data)
    return redirect('/myOrders')

#shfaq faqen ku jane myorders
@app.route('/myOrders')
def Myorders():
    data = {
        'client_id': session['client_id']
    } 
    orders = Order.get_all_client_orders(data)
    return render_template('myOrders.html', orders = orders)

#shfaq edit Order page 
@app.route('/edit/order/<int:id>')
def editOrder(id):
    if 'client_id' in session:

        data = {
            'order_id': id
        }
        data1 = {
            'client_id': session['client_id']
        }
        products = Product.get_all_products()
        loggedClient = Client.get_client_by_id(data1)
        order = Order.get_order_by_id(data)
        return render_template('editOrder.html', loggedClient = loggedClient, order= order, products = products)
    return redirect('/myOrders')

#Ben update e orders
@app.route('/edit/order/<int:id>', methods = ['POST'])
def updateOrder(id):
    if 'client_id' in session:
        data = {
            'order_id': id
        }
        order = Order.get_order_by_id(data)
        
        if not Order.validate_user(request.form):
            return redirect(request.referrer)
        if order:
            data = {
                'customer': request.form['customer'],
                'product_name': request.form['product_name'],
                'quantity': request.form['quantity'],
                'location' : request.form['location'],
                'product_id' : request.form['product_id'],
                'client_id': session['client_id'],
                'order_id' : id
            }
            Order.update_order(data)
            return redirect('/myOrders')
        return redirect('/myOrders')
    return redirect('/myOrders') 

#fshin analyse nga analyses
@app.route('/delete/order/<int:id>')
def remove_order(id):
    if 'client_id' in session:
        data = {
            'order_id': id
        }
        order = Order.get_order_by_id(data)
        if order:
            Order.delete_order(data)
            return redirect(request.referrer)
        return redirect('/myOrders')
    return redirect('/myOrders')

#shfaq te gjithe orders qe jane bere
@app.route('/allOrders')
def Admin_orders():
    if 'admin_id' not in session:
        return render_template('loginAdmin.html')
    orders = Order.get_all_orders()
    return render_template('AllOrders.html', orders = orders)

#fshin orders
@app.route('/delete_as_Admin/order/<int:id>')
def remove_order_as_Admin(id):
    if 'admin_id' not in session:
        return render_template('loginAdmin.html')
    data = {
            'order_id': id
        }
    order = Order.get_order_by_id(data)
    if order:
        Order.delete_order(data)
        return redirect(request.referrer)
    return redirect('/myOrders')


#per payments
@app.route('/checkout/paypal/<int:order_id>')
def checkoutPaypal(order_id):
    if 'client_id' not in session:
            return redirect('/')
    data = {
        'id': order_id
    }
    orderInfo = Order.get_order_all_info_by_id(data)
    quantity = int(orderInfo['quantity'])
    price = int(orderInfo['price'])
    totalPrice = round(price * quantity)

    try:
        paypalrestsdk.configure({
            "mode": "sandbox", # Change this to "live" when you're ready to go live
            "client_id": "AaAboW-Zm-keB5Whvyl0GwG5XeYpWuJ4U3jvQt0AUK627JC6AhHYniH4HZV8bmHkFp-nNWoct0mZc0Js",
            "client_secret": "EO2Ub_NANk8rACsbCgAiZ-J3aUTtPCyDw3Ilr0qj74TS4NNQKxK340_3ulEqEN_hsaYpmWz3jH74oe1s"
        })

        payment = paypalrestsdk.Payment({
            "intent": "sale",
            "payer": {
                "payment_method": "paypal"
            },
            "transactions": [{
                "amount": {
                    "total": totalPrice,
                    "currency": "USD"  # Adjust based on your currency
                },
                "description": f"Pagese !"
            }],
            "redirect_urls": {
                "return_url": url_for('paymentSuccess', _external=True, totalPrice=totalPrice,order_id = order_id),
                "cancel_url": "http://example.com/cancel"
            }
        })

        if payment.create():
            approval_url = next(link.href for link in payment.links if link.rel == 'approval_url')
            return redirect(approval_url)
        else:
            flash('Something went wrong with your payment', 'creditCardDetails')
            return redirect(request.referrer)
    except paypalrestsdk.ResourceNotFound as e:
        flash('Something went wrong with your payment', 'creditCardDetails')
        return redirect(request.referrer)






@app.route("/success", methods=["GET"])
def paymentSuccess():
    payment_id = request.args.get('paymentId', '')
    payer_id = request.args.get('PayerID', '')
    try:
        paypalrestsdk.configure({
            "mode": "sandbox", # Change this to "live" when you're ready to go live
            "client_id": "AaAboW-Zm-keB5Whvyl0GwG5XeYpWuJ4U3jvQt0AUK627JC6AhHYniH4HZV8bmHkFp-nNWoct0mZc0Js",
            "client_secret": "EO2Ub_NANk8rACsbCgAiZ-J3aUTtPCyDw3Ilr0qj74TS4NNQKxK340_3ulEqEN_hsaYpmWz3jH74oe1s"
        })
        payment = paypalrestsdk.Payment.find(payment_id)
        if payment.execute({"payer_id": payer_id}):
            
            print("////////////////////////////////")
            
            amount = request.args.get('totalPrice')
            status = 'Paid'
            client_id = session['client_id']
            data = {
                'amount': amount,
                'status': status,
                'client_id': client_id,
                'order_id' : request.args.get('order_id')
            }
            Client.createPayment(data)
           
            flash('Your payment was successful!', 'paymentSuccessful')
            return redirect('/dashboard')
        else:
            print('*******************************************************')
            flash('Something went wrong with your payment', 'paymentNotSuccessful')
            return redirect('/')
    except paypalrestsdk.ResourceNotFound as e:
        flash('Something went wrong with your payment', 'paymentNotSuccessful')
        return redirect('/dashboard')

#anullon pagesen
@app.route("/cancel", methods=["GET"])
def paymentCancel():
    flash('Payment was canceled', 'paymentCanceled')
    return redirect('/dashboard')
