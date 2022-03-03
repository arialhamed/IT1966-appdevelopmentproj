@app.route("/transaction", methods=['GET','POST'])
def transactions():
    Create_Transaction_Form = CreateTransactionForm(request.form)
    user_id = session['user_id']
    if request.method == 'POST':
        first_name = Create_Transaction_Form.first_name.data
        last_name = Create_Transaction_Form.last_name.data
        username = Create_Transaction_Form.username.data
        email = Create_Transaction_Form.email.data
        address = Create_Transaction_Form.address.data
        payment_method = Create_Transaction_Form.payment_type.data
        cc_number = Create_Transaction_Form.card_number.data
        cc_expiration = Create_Transaction_Form.expiry.data
        cc_cvv = Create_Transaction_Form.security_code.data

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
    else:
        db = shelve.open('storage.db', 'w')
        customer_dict = db['Customers']
        customer = customer_dict.get(user_id)

        Create_Transaction_Form.first_name.data = customer.get_firstName()
        Create_Transaction_Form.last_name.data = customer.get_lastName()
        Create_Transaction_Form.username.data = customer.get_username()
        Create_Transaction_Form.email.data = customer.get_email()
        Create_Transaction_Form.address.data = customer.get_address()
        Create_Transaction_Form.payment_type.data = customer.get_payment_method()
        Create_Transaction_Form.card_number.data = customer.get_card_number()
        Create_Transaction_Form.expiry.data = customer.get_expiry()
        Create_Transaction_Form.security_code.data = customer.get_security_code()

        cart_dict = {}
        db = shelve.open('cart.db', 'r')
        cart_dict = db['cart']
        db.close()
        user_cart = cart_dict.get(user_id)
        total = 0
        cart_list = []
        for key in user_cart:
            product = user_cart.get(key)
            total = total + product.get_total()
            cart_list.append(product)

    return render_template('transaction/transaction.html',form=Create_Transaction_Form,cart_list = cart_list,total=total)
