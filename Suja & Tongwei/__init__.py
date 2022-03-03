from flask import Flask,render_template,request,redirect,url_for,session
from Forms import CreateReviewForm,CreateCustomerForm, LoginCustomerForm, LoginAdminForm, UpdateCustomerForm
from decimal import Decimal
from Forms import Createproduct, Uploadimage
import shelve, Review, Customer, os
from Products import Products
from datetime import datetime
from Forms import CreateTransactionForm

app = Flask(__name__, static_url_path='/static')
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.secret_key = r'.monke[yare)cute/'

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/base')
def base():
    return render_template('base.html')

# <------------------------------------------------------->
# <------------------ TONG WEI ------------------>
# <------------------------------------------------------->
# StoreManage ViewProductStore
@app.route('/storeManage')
def store_manage():
    print('load', flush=True)
    db = shelve.open('ProductStorage.db', 'c')
    try:
        products_dict = db['Products']
    except KeyError:
        print('error retrieving products dict')
        products_dict = {}

    print(products_dict, flush=True)
    products_list = []

    for key in products_dict:
        print(key, flush=True)
        product = products_dict[key]
        products_list.append(product)
        print(product, flush=True)
    print(products_list, flush=True)


    return render_template('storeManage/storeManage.html', products_list=products_list)

# UploadProduct
@app.route('/uploadProduct', methods=['GET', 'POST'])
def upload_product():
    print('upload', flush=True)
    form = Createproduct()
    Uploadfield = Uploadimage()
    # form.validate()
    # print(form.errors.items())

    if form.validate_on_submit() and Uploadfield.validate_on_submit():
        products_dict = {}
        db = shelve.open('ProductStorage.db', 'c')

        try:
            products_dict = db['Products']

        except:
            print("Error in retrieving Products from ProductStorage.db.")

        image = request.files[Uploadfield.productImage.name]
        # product is an object
        product = Products(form.productName.data, form.productPrice.data.quantize(Decimal("0.01")), form.productDescription.data, form.productQuantity.data)
        img_extension = image.filename.split('.')[-1]
        print(img_extension)
        image_name = str(product.get_products_id()) + '.' + str(img_extension)
        print(image_name)
        image.save(os.path.join(os.getcwd(), 'static', 'img', image_name))
        product.set_image(image_name)
        products_dict[product.get_products_id()] = product

        db['Products'] = products_dict

        db.close()
        print(product.get_products_id(), flush=True)
        return redirect(url_for('store_manage'))
    return render_template('storeManage/uploadProduct.html', form=form, Uploadfield=Uploadfield)


# EditProduct
@app.route('/editProduct/<id>', methods=['GET', 'POST'])
def edit_product(id):
    Editproduct = Createproduct()
    print(id, flush=True)
    print("Form done", flush=True)
    if request.method == 'POST' and Editproduct.validate():
        products_dict = {}
        db = shelve.open('ProductStorage.db', 'w')
        products_dict = db['Products']
        product = products_dict.get(id)
        image = request.files[Editproduct.updateImage.name]
        # product is an object
        if image.filename:
            img_extension = image.filename.split('.')[-1]
            image_name = str(product.get_products_id()) + '.' + str(img_extension)
            print(image_name)
            image.save(os.path.join(os.getcwd(), 'static', 'img', image_name))
            product.set_image(image_name)

        product.set_name(Editproduct.productName.data)
        product.set_price(Editproduct.productPrice.data.quantize(Decimal("0.01")))
        product.set_description(Editproduct.productDescription.data)
        product.set_quantity(Editproduct.productQuantity.data)
        db['Products'] = products_dict
        db.close()
        return redirect(url_for('store_manage'))
    else:
        products_dict = {}
        db = shelve.open('ProductStorage.db', 'r')
        products_dict = db['Products']
        db.close()

        product = products_dict.get(id)
        image = product.get_image()

        Editproduct.productName.data = product.get_name()
        Editproduct.productPrice.data = product.get_price()
        Editproduct.productDescription.data = product.get_description()
        Editproduct.productQuantity.data = product.get_quantity()

    return render_template('storeManage/editProduct.html', form=Editproduct, image=image)


#DeleteProduct
@app.route('/deleteProduct/<id>', methods=['POST'])
def delete_products(id):
    products_dict = {}
    db = shelve.open('ProductStorage.db', 'w')
    products_dict = db['Products']

    image = products_dict[id].get_image()
    os.remove(os.path.join(os.getcwd(), 'static', 'img', image))

    products_dict.pop(id)

    db['Products'] = products_dict
    db.close()

    return redirect(url_for('store_manage'))


# ViewProductStore
@app.route('/storeView/<id>/', methods=['GET'])
def store_view(id):
    db = shelve.open('ProductStorage.db', 'c')
    try:
        products_dict = db['Products']
    except KeyError:
        print('error retrieving products dict')
        products_dict = {}

    print(products_dict, flush=True)

    product = products_dict[id]

    return render_template('storeManage/storeView.html', product=product)


# ViewProductCustomer
@app.route('/customerView/<id>/', methods=['GET'])
def customer_view(id):
    db = shelve.open('ProductStorage.db', 'c')
    try:
        products_dict = db['Products']
    except KeyError:
        print('error retrieving products dict')
        products_dict = {}

    print(products_dict, flush=True)

    product = products_dict[id]

    return render_template('storeManage/customerView.html', product=product)


# ViewStoreCustomer
@app.route('/customerProduct', methods=['GET'])
def customer_product():
    db = shelve.open('ProductStorage.db', 'c')
    try:
        products_dict = db['Products']
    except KeyError:
        print('error retrieving products dict')
        products_dict = {}

    print(products_dict, flush=True)
    products_list = []

    for key in products_dict:
        print(key, flush=True)
        product = products_dict[key]
        products_list.append(product)
        print(product, flush=True)
    print(products_list, flush=True)


    return render_template('storeManage/customerProduct.html', products_list=products_list)

# <------------------------------------------------------->
# <------------------      MICHAEL      ------------------>
# <------------------------------------------------------->
@app.route('/addCart/<id>/<int:qty>', methods=['GET'])
def addCart(id,qty):
    user_id = session['user_id']
    product_id = id
    quantity = qty
    if request.method == 'GET':
        product_dict = {}
        try:
            db = shelve.open('storage.db', 'r')
            product_dict = db['Products']
        except:
            print("Error in retrieving Users from storage.db.")
        item = product_dict[product_id]
        cart_dict = {}
        try:
            db = shelve.open('cart.db', 'c')
            cart_dict = db['cart']
        except:
            print("Error in retrieving Users from cart.db.")
        inCartAlr = 0
        user_cart = cart_dict.get(user_id)
        for key in user_cart:
            if product_id == key:
                inCartAlr = 1
        if inCartAlr == 1:
            item = user_cart[product_id]
            Nqty = item.add_qty(qty)
            total = item.set_total(Nqty)
            user_cart[item.get_products_id()] = item
            cart_dict[user_id] = user_cart
            db['cart'] = cart_dict
            db.close()
        else:
            item.set_qty(qty)
            total = item.set_total(qty)
            user_cart[item.get_products_id()] = item
            cart_dict[user_id] = user_cart
            db['cart'] = cart_dict
            db.close()
    return redirect(url_for('Cart'))

@app.route('/updateCart/<id>/<int:qty>', methods=['POST'])
def updateCart(id,qty):
    user_id = session['user_id']
    product_id = id
    quantity = qty
    cart_dict = {}
    db = shelve.open('cart.db', 'c')
    cart_dict = db['cart']
    user_cart = cart_dict[user_id]
    item = user_cart[product_id]

    user_cart[item.get_products_id()] = item
    item.set_qty(qty)
    item.set_total(qty)
    user_cart[product_id] = item
    cart_dict[user_id] = user_cart
    db['cart'] = cart_dict
    db.close()
    return("",204)

@app.route('/deleteCart/<id>', methods=['POST'])
def delete_cart(id):
    cart_dict = {}
    user_id = session['user_id']
    db = shelve.open('cart.db', 'w')
    cart_dict = db['cart']
    user_cart = cart_dict[user_id]
    user_cart.pop(id)

    cart_dict[user_id] = user_cart
    db['cart'] = cart_dict
    db.close()

    return redirect(url_for('Cart'))

@app.route('/shoppingCart')
def Cart():
    cart_dict = {}
    if 'user_id' in session:
        user_id = session['user_id']
        db = shelve.open('cart.db', 'r')
        cart_dict = db['cart']
        db.close()
        user_cart = cart_dict.get(user_id)
        if len(user_cart) == 0:
            cart_list = []
            total = 0
        else:
            cart_list = []
            total = 0
            for key in user_cart:
                product = user_cart.get(key)
                total = total + product.get_total()
                cart_list.append(product)
    else:
        cart_list = []
        total = 0
    return render_template('shoppingCart.html', count=len(cart_list), cart_list=cart_list, total=total)
# <------------------------------------------------------->
# <------------------ MICHAEL TRANSACTIONS  -------------->
# <------------------------------------------------------->
@app.route("/transaction", methods=['GET','POST'])
def transactions():
    Create_Transaction_Form = CreateTransactionForm(request.form)
    user_id = session['user_id']
    if request.method == 'POST':
        customer_dict = {}
        db = shelve.open('storage.db', 'w')
        customer_dict = db['Customers']
        db.close()
        customer = customer_dict.get(user_id)
        test = customer.get_expiry()
        test_str = 'yes'
        if type(test) == type(test_str):
            test = datetime.strptime(test, '%Y-%m-%d')
            customer.set_expiry(test)


        Create_Transaction_Form.first_name.data = customer.get_firstName()
        Create_Transaction_Form.last_name.data = customer.get_lastName()
        Create_Transaction_Form.username.data = customer.get_username()
        Create_Transaction_Form.email.data = customer.get_email()
        Create_Transaction_Form.address.data = customer.get_address()
        Create_Transaction_Form.postal.data = customer.get_postal()
        Create_Transaction_Form.payment_method.data = customer.get_payment_method()
        Create_Transaction_Form.cc_number.data = customer.get_card_number()
        Create_Transaction_Form.cc_expiration.data = customer.get_expiry()
        Create_Transaction_Form.cc_cvv.data = customer.get_security_code()
        # return redirect(url_for('checkout_confirmation'))

    cart_dict = {}
    db = shelve.open('cart.db', 'r')
    cart_dict = db['cart']
    user_cart = cart_dict.get(user_id)
    db.close()
    cart_list = []
    total = 0
    for key in user_cart:
        product = user_cart.get(key)
        total = total + product.get_total()
        cart_list.append(product)

    if request.method == 'GET':
        first_name = str(request.args.get('first_name'))
        last_name = str(request.args.get('last_name'))
        username = str(request.args.get('username'))
        email = str(request.args.get('email'))
        address = str(request.args.get('address'))
        payment_method = request.args.get('payment_method')
        cc_number = int(request.args.get('cc_number'))
        cc_expiration = request.args.get('cc_expiration')
        cc_cvv = int(request.args.get('cc_cvv'))

        customer_dict = {}
        db = shelve.open('storage.db', 'w')
        customer_dict = db['Customers']

        customer = customer_dict.get(user_id)
        customer.set_firstName(first_name)
        customer.set_lastName(last_name)
        customer.set_username(username)
        customer.set_email(email)
        customer.set_address(address)
        customer.set_payment_method(payment_method)
        customer.set_card_number(cc_number)
        customer.set_expiry(cc_expiration)
        customer.set_security_code(cc_cvv)

        db['Customers'] = customer_dict
        db.close()
        return redirect(url_for('confirm_transaction'))

    return render_template('transaction/transaction.html',form=Create_Transaction_Form,cart_list = cart_list,total=total)

@app.route('/confirm',methods = ['GET','POST'])
def confirm_transaction():
    # if request.method == "POST":
    #     return transactions()
    user_id = session['user_id']
    customer_dict = {}
    db = shelve.open('storage.db', 'r')
    customer_dict = db['Customers']
    db.close()

    customer = customer_dict.get(user_id)

    cart_dict = {}
    db = shelve.open('cart.db', 'r')
    cart_dict = db['cart']
    user_cart = cart_dict[user_id]
    db.close()
    cart_list = []
    total = 0
    for key in user_cart:
        product = user_cart.get(key)
        total = total + product.get_total()
        cart_list.append(product)
    return render_template('transaction/confirmTransaction.html', products_list=cart_list, customer=customer, total=total)

@app.route('/Paid')
def paid():
    user_id = session['user_id']
    db = shelve.open('storage.db', 'w')
    customer_dict = db['Customers']
    product_dict = db['Products']
    db.close()

    customer = customer_dict.get(user_id)

    cart_dict = {}
    db = shelve.open('cart.db', 'c')
    cart_dict = db['cart']
    user_cart = cart_dict[user_id]
    db.close()

    cart_list = []
    total = 0
    for key in user_cart:
        product = product_dict.get(key)
        cart_item = user_cart.get(key)
        stock = product.get_stock() - cart_item.get_qty()
        product.set_stock(stock)
        total = total + cart_item.get_total()
        cart_list.append(cart_item)
        product_dict[key] = product
    db = shelve.open('storage.db', 'c')
    db['Products'] = product_dict
    db.close()
    db = shelve.open('cart.db', 'c')
    cart_dict = db['cart']
    cart_dict[user_id] = ''
    db['cart'] = cart_dict
    db.close()
    return render_template('transaction/paid.html', products_list=cart_list, customer=customer, total=total)


@app.route('/createCustomer', methods=['GET', 'POST'])
def create_customer():
    create_customer_form = CreateCustomerForm(request.form)
    if request.method == 'POST' and create_customer_form.validate() and create_customer_form.validate_on_date() and create_customer_form.validate_on_phone():
        customer_dict = {}
        db = shelve.open('CustomerStorage.db', 'c')

        try:
            customer_dict = db['Customers']
        except:
            print("For Programmer: Error in retrieving Customers from CustomerStorage.db.")

        # If username == existing username ask user to choose another username, else create user

        customer = Customer.Customer(create_customer_form.first_name.data, create_customer_form.last_name.data, create_customer_form.username.data, create_customer_form.email.data, create_customer_form.gender.data, create_customer_form.DOB.data, create_customer_form.password.data, create_customer_form.phone_number.data, create_customer_form.address.data, create_customer_form.postal.data, create_customer_form.payment_type.data, create_customer_form.card_number.data, create_customer_form.expiry.data, create_customer_form.security_code.data)
        customer_dict[customer.get_customer_id()] = customer
        db['Customers'] = customer_dict

        customer_dict = db['Customers']
        customer = customer_dict[customer.get_customer_id()]
        print("For Programmer: {} has been stored in CustomerStorage.db successfully with customer_id == {} and username == {}".format(customer.get_firstName(), customer.get_customer_id(), customer.get_username()))

        db.close()

        return redirect(url_for('home'))
    return render_template('createCustomer.html', form=create_customer_form)

# Customer Account Login
@app.route('/loginCustomer', methods=['GET', 'POST'])
def login_customer():
    login_customer_form = LoginCustomerForm(request.form)
    if request.method == 'POST' and login_customer_form.validate():
        customer_dict = {}
        db = shelve.open('CustomerStorage.db', 'c')
        try:
            customer_dict = db['Customers']
        except:
            print("For Programmer: Error in retrieving Customers from storage.db")
        if customer_dict:
            for key in customer_dict:
                username = customer_dict[key].get_username()
                password = customer_dict[key].get_password()
                if username == login_customer_form.username.data and password == login_customer_form.password.data:
                    print("For Programmer: {} has Successfully Login".format(username))
                    session['logged_in'] = True
                    session['admin_logged_in'] = False
                    session['username'] = username
                    # flash('you are now logged in', 'success')
                    return redirect(url_for('home'))
                elif username == login_customer_form.username.data:
                    print("For Programmer: Incorrect Password; Username == {}".format(username))
                    # Need to show error to user
                    error = "Invalid Login. Incorrect Username or Password!"
                    return render_template('loginCustomer.html', form=login_customer_form, error=error)
                else:
                    print("For Programmer: No such Users")
                    error = "No User Found"
                    return render_template('loginCustomer.html', form=login_customer_form, error=error)
        else: # if dictionary was empty
            print("For Programmer: No such Users")
            error = "No User Found"
            return render_template('loginCustomer.html', form=login_customer_form, error=error)
        db.close()

    return render_template('loginCustomer.html', form=login_customer_form)


@app.route('/customerProfile')
def customer_profile():
    customer_dict = {}
    db = shelve.open('CustomerStorage.db', 'r')
    customer_dict = db['Customers']
    db.close()

    customer_list = []
    for key in customer_dict:
        customer = customer_dict.get(key)
        customer_list.append(customer)

    return render_template('customerProfile.html', count=len(customer_list), customer_list=customer_list)


@app.route('/updateCustomer/<int:id>/', methods=['GET', 'POST'])
def update_customer(id):
    update_customer_form = UpdateCustomerForm(request.form)
    if request.method == 'POST' and update_customer_form.validate() and update_customer_form.validate_on_date() and update_customer_form.validate_on_phone():
        customer_dict = {}
        db = shelve.open('CustomerStorage.db', 'w')
        customer_dict = db['Customers']

        customer = customer_dict.get(id)
        customer.set_firstName(update_customer_form.first_name.data)
        customer.set_lastName(update_customer_form.last_name.data)
        customer.set_username(update_customer_form.username.data)
        customer.set_email(update_customer_form.email.data)
        customer.set_gender(update_customer_form.gender.data)
        customer.set_birth(update_customer_form.DOB.data)
        customer.set_phone_number(update_customer_form.phone_number.data)
        customer.set_address(update_customer_form.address.data)
        customer.set_postal(update_customer_form.postal.data)
        customer.set_payment_method(update_customer_form.payment_type.data)
        customer.set_card_number(update_customer_form.card_number.data)
        customer.set_expiry(update_customer_form.expiry.data)
        customer.set_security_code(update_customer_form.security_code.data)

        db['Customers'] = customer_dict
        db.close()
        session['username'] = customer.get_username()
        if session['admin_logged_in']:
            return redirect((url_for('customer_account')))
        else:
            return redirect(url_for('customer_profile'))
    else:
        customer_dict = {}
        db = shelve.open('CustomerStorage.db', 'r')
        customer_dict = db['Customers']
        db.close()

        customer = customer_dict.get(id)
        update_customer_form.first_name.data = customer.get_firstName()
        update_customer_form.last_name.data = customer.get_lastName()
        update_customer_form.username.data = customer.get_username()
        update_customer_form.email.data = customer.get_email()
        update_customer_form.gender.data = customer.get_gender()
        update_customer_form.DOB.data = customer.get_birth()
        update_customer_form.phone_number.data = customer.get_phone_number()
        update_customer_form.address.data = customer.get_address()
        update_customer_form.postal.data = customer.get_postal()
        update_customer_form.payment_type.data = customer.get_payment_method()
        update_customer_form.card_number.data = customer.get_card_number()
        update_customer_form.expiry.data = customer.get_expiry()
        update_customer_form.security_code.data = customer.get_security_code()
        return render_template('updateCustomer.html', form=update_customer_form)


@app.route('/deleteCustomer/<int:id>', methods=['POST'])
def delete_customer(id):
    customer_dict = {}
    db = shelve.open('CustomerStorage.db', 'w')
    customer_dict = db['Customers']

    customer_dict.pop(id)

    db['Customers'] = customer_dict
    db.close()
    print("account has been deleted")

    if session['admin_logged_in']:
        pass
        return redirect(url_for('customer_account'))
    else:
        session.clear()
        return redirect(url_for('home'))


# Logout
@app.route('/logout')
def logout():
    username = session['username']
    print("For Programmer: {} has Successfully Logout".format(username))
    session.clear()
    # flash('You are now logged out', 'success')
    return redirect(url_for('home'))


@app.route('/loginAdmin', methods=['GET', 'POST'])
def login_admin():
    login_admin_form = LoginAdminForm(request.form)
    if request.method == 'POST' and login_admin_form.validate():
        username = "Admin"
        password = "12345678"
        if username == login_admin_form.username.data and password == login_admin_form.password.data:
            session['admin_logged_in'] = True
            session['username'] = "Admin"
            print("For Programmer: {} have successfully logged in".format(username))
            return redirect(url_for('home'))
        else:
            print("For Programmer: Invalid Admin")
            error = "Invalid Admin"
            return render_template('loginAdmin.html', form=login_admin_form, error=error)
    return render_template('loginAdmin.html', form=login_admin_form)


@app.route('/customerAccount')
def customer_account():
    customer_dict = {}
    db = shelve.open('CustomerStorage.db', 'r')
    session['username'] = "Admin"
    try:
        customer_dict = db['Customers']
    except:
        print("ERROR")
    db.close()

    customer_list = []
    for key in customer_dict:
        customer = customer_dict.get(key)
        customer_list.append(customer)

    return render_template('customerAccount.html', count=len(customer_list), customer_list=customer_list)

# <------------------------------------------------------->
# <------------------       SUJA        ------------------>
# <------------------------------------------------------->
@app.route('/createreview', methods=['GET', 'POST'])
def create_review():
    create_review_form = CreateReviewForm(request.form)
    if request.method == 'POST' and create_review_form.validate():
        reviews_dict = {}
        db = shelve.open('storage.db', 'c')

        try:
            reviews_dict = db['Reviews']
        except:
            print("Error in retrieving Reviews from storage.db.")

        review = Review.Review(create_review_form.ratings.data, create_review_form.product_id.data, create_review_form.email.data, create_review_form.comments.data)
        reviews_dict[review.get_product_id()] = review
        db['Reviews'] = reviews_dict



        db.close()

        return redirect(url_for('retrieve_users'))
    return render_template('createreview.html', form=create_review_form)

@app.route('/allreviews')
def retrieve_users():
    reviews_dict = {}
    db = shelve.open('storage.db', 'r')
    reviews_dict = db['Reviews']
    db.close()

    reviews_list = []
    for key in reviews_dict:
        review = reviews_dict.get(key)
        reviews_list.append(review)

    return render_template('allreviews.html',count=len(reviews_list), users_list=reviews_list)

@app.route('/staffreview')
def recover_reviews():
    reviews_dict = {}
    db = shelve.open('storage.db', 'r')
    reviews_dict = db['Reviews']
    db.close()

    reviews_list = []
    for key in reviews_dict:
        review = reviews_dict.get(key)
        reviews_list.append(review)

    return render_template('staffreview.html',count=len(reviews_list), reviews_list=reviews_list)

@app.route('/updatereview/<int:id>/', methods=['GET', 'POST'])
def update_review(id):
    update_review_form = CreateReviewForm(request.form)
    if request.method == 'POST' and update_review_form.validate():
        reviews_dict = {}
        db = shelve.open('storage.db', 'w')
        reviews_dict = db['Reviews']

        review = reviews_dict.get(id)
        review.set_ratings(update_review_form.ratings.data)
        review.set_product_id(update_review_form.product_id.data)
        review.set_email(update_review_form.email.data)
        review.set_comments(update_review_form.comments.data)

        db['Reviews'] = reviews_dict
        db.close()

        return redirect(url_for('retrieve_users'))
    else:
        reviews_dict = {}
        db = shelve.open('storage.db', 'r')
        reviews_dict = db['Reviews']
        db.close()

        review = reviews_dict.get(id)
        update_review_form.ratings.data = review.get_ratings()
        update_review_form.product_id.data = review.get_product_id()
        update_review_form.email.data = review.get_email()
        update_review_form.comments.data = review.get_comments()

        return render_template('updatereview.html', form=update_review_form)

@app.route('/deleteReview/<int:id>', methods=['POST'])
def delete_review(id):
    reviews_dict = {}
    db = shelve.open('storage.db', 'w')
    reviews_dict = db['Reviews']


    reviews_dict.pop(id)

    db['Reviews'] = reviews_dict
    db.close()

    return redirect(url_for('retrieve_users'))



if __name__ == '__main__':
    app.run(debug=True)
