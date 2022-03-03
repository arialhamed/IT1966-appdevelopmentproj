try:
    from flask import Flask, render_template, request, redirect, url_for, session
    import wtforms
    from country_list import countries_for_language
    import email_validator
    import wtforms_validators

    print("Modules present")
except ImportError:
    print("Modules not present.")
    from os import system

    print("Installing now.")
    system("pip install -r requirements.txt")
    from flask import Flask, render_template, request, redirect, url_for, session
from Forms import CreateCustomerForm, LoginCustomerForm, LoginAdminForm, UpdateCustomerForm, CreateFaqForm

import shelve
import Customer, FAQ


app = Flask(__name__, static_url_path='/static')
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


# Promotion and Product Page
@app.route('/')
def home():
    return render_template("home.html")


# Customer Account Creation
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

@app.route('/FAQ', methods=['GET', 'POST'])
def faq():
    faq_dict = {}
    create_faq_form = CreateFaqForm(request.form)
    try:
        db = shelve.open('storage.db',
                         'c')  # argument is 'c', so guaranteed that it will create, concerning a warning from another line
        faq_dict = db["FAQ"]
    # db.close()
    except KeyError:
        print("Error in retrieving FAQStorage.db, recreating FAQStorage.db.")
    #     return redirect(url_for('create_faq'))

    if request.method == 'POST' and create_faq_form.validate():  # and request.id == 'question':
        if create_faq_form.question.data != '' and create_faq_form.answer.data == '':
            faq_details = FAQ.FAQ(create_faq_form.question.data)
            faq_dict[faq_details.get_id()] = faq_details
            create_faq_form.question.data = ''

        db['FAQ'] = faq_dict

        # Test codes
        faq_dict = db['FAQ']
        try:
            faq = faq_dict[faq_details.get_id()]
            print("\"" + str(faq.get_question()) + "\" question was stored in storage.db successfully with id ==",
                  faq.get_id())
        except KeyError:
            print("KeyError in retrieving latest input, likely it was blank. This error is expected.")
        except UnboundLocalError:
            print("UnboundLocalError in retrieving latest input, likely it was blank. This error is expected.")

    question_list = []
    unanswered_count = 0
    for key in faq_dict:
        question = faq_dict.get(key)
        question_list.append(question)
        if question.get_answer() == '':
            unanswered_count += 1
    db.close()

    return render_template("faq.html", form=create_faq_form, count=len(question_list), question_list=question_list,
                           unanswered_count=unanswered_count)


@app.route('/FAQanswering/<int:id>/', methods=['GET', 'POST'])
def faqanswering(id):
    faq_answer = CreateFaqForm(request.form)
    if request.method == 'POST' and faq_answer.validate():
        faq_dict = {}
        db = shelve.open('storage.db', 'w')
        faq_dict = db['FAQ']

        faq = faq_dict.get(id)
        # print(type(faq))
        # print(faq)
        faq.set_question(faq_answer.question.data)
        faq.set_answer(faq_answer.answer.data)

        db['FAQ'] = faq_dict
        db.close()

        return redirect(url_for('faq'))
    else:
        faq_dict = {}
        db = shelve.open('storage.db', 'r')
        faq_dict = db['FAQ']
        db.close()

        faq = faq_dict.get(id)
        faq_answer.question.data = faq.get_question()
        faq_answer.answer.data = faq.get_answer()
        return render_template('faq_answering.html', form=faq_answer)


@app.route("/FAQdelete/<int:id>/", methods=['POST'])
def faqdelete(id):
    faq_dict = {}
    db = shelve.open("storage.db", 'w')
    faq_dict = db["FAQ"]

    faq = faq_dict.pop(id)

    db['FAQ'] = faq_dict
    db.close()

    return redirect(url_for("faq"))




if __name__ == "__main__":
    app.run(debug=True)
