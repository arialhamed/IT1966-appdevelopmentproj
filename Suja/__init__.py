# <--- Start of Importations and Installations --->
try:
    from flask import Flask, render_template, request, redirect, url_for, session
    import wtforms
    import email_validator
    import wtforms_validators
    import os
    import datetime

    print("For Programmer: SUCCESS --> Modules present")
except ImportError:
    print("For Programmer: ERROR --> Modules not present")
    from os import system

    print("For Programmer: FIXING ERROR --> Installing now...")
    system("pip install -r requirements.txt")
    from flask import Flask, render_template, request, redirect, url_for, session
from Forms import CreateCustomerForm, LoginCustomerForm, LoginAdminForm, UpdateCustomerForm, CreateFaqForm, \
    ResetPasswordForm, ForgetPasswordForm, Createproduct, Uploadimage, CreateReviewForm

import shelve, Customer, Email, FAQ, Products, Review

# <--- End of Importations and Installations --->


app = Flask(__name__, static_url_path='/static')
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


# <------------------------------------------------------->
# <------------ General Routes (Jabez's Code) ------------>
# <------------------------------------------------------->
# <--- Start of 404 Error Page --->
@app.errorhandler(404)
def invalid_route(e):
    return render_template('404.html')


@app.route('/invalid_route')
def error_render():
    print("For Programmer: ERROR --> No such route")
    return render_template('404.html')


# <--- End of 404 Error Page --->


# <--- Start of Home Route --->
@app.route('/')
def home():
    return render_template("home.html")


# <--- End of Home Route --->


# <--- Start of About Route --->
@app.route('/about')
def about():
    return render_template("about.html")


# <--- End of About Route --->


# <--- Start of Contact Route --->
@app.route('/contact')
def contact():
    return render_template("contact.html")


# <--- End of Contact Route --->


# <------------------------------------------------------->
# <---------- Account Management (Jabez's Code) ---------->
# <------------------------------------------------------->
# <---Start of Customer Account Creation--->
@app.route('/createCustomer', methods=['GET', 'POST'])
def create_customer():
    create_customer_form = CreateCustomerForm(request.form)
    if request.method == 'POST' and create_customer_form.validate() and create_customer_form.validate_on_date() and create_customer_form.validate_on_phone():
        customer_dict = {}
        db = shelve.open('storage.db', 'c')

        try:
            customer_dict = db['Customers']
            print("For Programmer: SUCCESS --> Success in retrieving Customers from storage.db")
        except:
            print("For Programmer: ERROR --> Error in retrieving Customers from storage.db.")
        if customer_dict:
            for key in customer_dict:
                username = customer_dict[key].get_username()
                email = customer_dict[key].get_email()
                # Email and username validation (if username or email is taken)
                if username == create_customer_form.username.data and create_customer_form.email.data:
                    print("For Programmer: ERROR --> Username and Email taken!")
                    error = "Username and email is taken"
                    return render_template('createCustomer.html', form=create_customer_form, error=error)
                elif username == create_customer_form.username.data:
                    print("For Programmer: ERROR --> Username taken!")
                    error = "Username is taken"
                    return render_template('createCustomer.html', form=create_customer_form, error=error)
                elif email == create_customer_form.email.data:
                    print("For Programmer: ERROR --> Email is taken")
                    error = "Email is taken"
                    return render_template('createCustomer.html', form=create_customer_form, error=error)
                else:
                    customer = Customer.Customer(create_customer_form.first_name.data,
                                                 create_customer_form.last_name.data,
                                                 create_customer_form.username.data, create_customer_form.email.data,
                                                 create_customer_form.gender.data, create_customer_form.DOB.data,
                                                 create_customer_form.password.data,
                                                 create_customer_form.phone_number.data,
                                                 create_customer_form.address.data, create_customer_form.postal.data,
                                                 create_customer_form.payment_type.data,
                                                 create_customer_form.card_number.data,
                                                 create_customer_form.expiry.data,
                                                 create_customer_form.security_code.data,
                                                 create_customer_form.reset_pass)
                    customer_dict[customer.get_customer_id()] = customer
                    db['Customers'] = customer_dict

                    customer_dict = db['Customers']
                    customer = customer_dict[customer.get_customer_id()]
                    db.close()

                    print(
                        "For Programmer: SUCCESS --> {} has been successfully stored in storage.db. customer_id == {} and username == {}".format(
                            customer.get_firstName(), customer.get_customer_id(), customer.get_username()))
                    success = "Account Successfully Created!"
                    return redirect(url_for('login_customer', success=success))
        else:
            customer = Customer.Customer(create_customer_form.first_name.data, create_customer_form.last_name.data,
                                         create_customer_form.username.data, create_customer_form.email.data,
                                         create_customer_form.gender.data, create_customer_form.DOB.data,
                                         create_customer_form.password.data, create_customer_form.phone_number.data,
                                         create_customer_form.address.data, create_customer_form.postal.data,
                                         create_customer_form.payment_type.data, create_customer_form.card_number.data,
                                         create_customer_form.expiry.data, create_customer_form.security_code.data,
                                         create_customer_form.reset_pass)
            customer_dict[customer.get_customer_id()] = customer
            db['Customers'] = customer_dict

            customer_dict = db['Customers']
            customer = customer_dict[customer.get_customer_id()]
            db.close()

            print(
                "For Programmer: SUCCESS --> {} has been successfully stored in storage.db. customer_id == {} and username == {}".format(
                    customer.get_firstName(), customer.get_customer_id(), customer.get_username()))
            success = "Account Successfully Created!"
            return redirect(url_for('login_customer', success=success))
    return render_template('createCustomer.html', form=create_customer_form)


# <--- End of Customer Account Creation --->


# <--- Start of Customer Login --->
@app.route('/loginCustomer', methods=['GET', 'POST'])
def login_customer():
    login_customer_form = LoginCustomerForm(request.form)
    if request.method == 'POST' and login_customer_form.validate():
        customer_dict = {}
        db = shelve.open('storage.db', 'c')
        try:
            customer_dict = db['Customers']
            print("For Programmer: SUCCESS --> Success in retrieving Customers from storage.db")
        except:
            print("For Programmer: ERROR --> Error in retrieving Customers from storage.db")
        if customer_dict:
            for key in customer_dict:
                username = customer_dict[key].get_username()
                password = customer_dict[key].get_password()
                reset_pass = customer_dict[key].get_reset_pass()
                # Login validation (checking if username matches the dictionary username)
                if username == login_customer_form.username.data and password == login_customer_form.password.data:
                    print("For Programmer: SUCCESS --> {} has Successfully Login".format(username))
                    session['logged_in'] = True
                    session['admin_logged_in'] = False
                    session['username'] = username
                    session['user_id'] = customer_dict[key].get_customer_id()
                    # Start of Michael's cart codes
                    user_id = session['user_id']
                    db = shelve.open('cart.db', 'c')
                    try:
                        db['cart'] = {}
                        cart_dict = db['cart']
                        cart_dict[user_id] = {}
                        db['cart'] = cart_dict
                        db.close()
                    except:
                        print("For Programmer: ERROR --> Error in retrieving")
                    # End of Michael's cart codes
                    print("For Programmer: LOGS --> logged_in = TRUE")
                    print("For Programmer: LOGS --> admin_logged_in = FALSE")
                    # Compulsory reset password validation
                    if reset_pass is False:
                        print("For Programmer: SUCCESS --> {} has successfully logged in".format(username))
                        success = "Login successfully!"
                        db.close()
                        return redirect(url_for('home', success=success))
                    else:
                        print("For Programmer: SUCCESS --> {} has successfully logged in".format(username))
                        print("For Programmer: INFORMATION --> User({}) needs to update password".format(username))
                        error = "Please reset your password"
                        db.close()
                        return redirect(url_for('reset_password', error=error))
                elif username == login_customer_form.username.data:
                    print("For Programmer: ERROR --> Incorrect Password; Username == {}".format(username))
                    error = "Invalid Login. Incorrect Username or Password!"
                    db.close()
                    return render_template('loginCustomer.html', form=login_customer_form, error=error)
                else:
                    print("For Programmer: ERROR --> No User Found")
                    error = "Invalid Login. Incorrect Username or Password!"
                    db.close()
                    return render_template('loginCustomer.html', form=login_customer_form, error=error)
        else:
            # If dictionary was empty
            print("For Programmer: ERROR --> No Records in Shelve")
            error = "Invalid Login. Incorrect Username or Password!"
            db.close()
            return render_template('loginCustomer.html', form=login_customer_form, error=error)

        db.close()
    return render_template('loginCustomer.html', form=login_customer_form)


# <--- End of Customer Login --->


# <--- Start of Customer Profile --->
@app.route('/customerProfile')
def customer_profile():
    try:
        if session['logged_in']:
            customer_dict = {}
            db = shelve.open('storage.db', 'r')
            try:
                customer_dict = db['Customers']
                print("For Programmer: SUCCESS --> Success in retrieving Customers from storage.db")
            except:
                print("For Programmer: ERROR --> Error in retrieving Customers from storage.db")
            db.close()

            customer_list = []
            for key in customer_dict:
                customer = customer_dict.get(key)
                customer_list.append(customer)

            return render_template('customerProfile.html', count=len(customer_list), customer_list=customer_list)
    except:
        print("For Programmer: THREAT --> Someone is trying to break the system")
        return redirect(url_for('error_render'))


# <--- End of Customer Profile --->


# <--- Start of Customer Profile Update --->
@app.route('/updateCustomer/<int:id>/', methods=['GET', 'POST'])
def update_customer(id):
    try:
        if session['admin_logged_in'] or session['logged_in']:
            update_customer_form = UpdateCustomerForm(request.form)
            if request.method == 'POST' and update_customer_form.validate() and update_customer_form.validate_on_date() and update_customer_form.validate_on_phone():
                customer_dict = {}
                db = shelve.open('storage.db', 'w')
                try:
                    customer_dict = db['Customers']
                    print("For Programmer: SUCCESS --> Success in retrieving Customers from storage.db")
                except:
                    print("For Programmer: ERROR --> Error in retrieving Customers from storage.db")

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
                print("For Programmer: SUCCESS --> User's({}) information have been successfully updated")
                success = "Information successfully updated"
                # Checking if admin is accessing
                if session['admin_logged_in']:
                    return redirect((url_for('customer_account', success=success)))
                else:
                    return redirect(url_for('customer_profile', success=success))
            else:
                customer_dict = {}
                db = shelve.open('storage.db', 'r')
                try:
                    customer_dict = db['Customers']
                    print("For Programmer: SUCCESS --> Success in retrieving Customers from storage.db")
                except:
                    print("For Programmer: ERROR --> Error in retrieving Customers from storage.db")
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
    except:
        print("For Programmer: THREAT --> Someone is trying to break the system")
        return redirect(url_for('error_render'))


# <--- Start of Customer Profile Update --->


# <--- Start of Customer Delete Account --->
@app.route('/deleteCustomer/<int:id>', methods=['POST'])
def delete_customer(id):
    customer_dict = {}
    db = shelve.open('storage.db', 'w')
    try:
        customer_dict = db['Customers']
        print("For Programmer: SUCCESS --> Success in retrieving Customers from storage.db")
    except:
        print("For Programmer: ERROR --> Error in retrieving Customers from storage.db")

    customer_dict.pop(id)
    db['Customers'] = customer_dict
    print("For Programmer: SUCCESS --> An Account has been deleted")
    db.close()

    success = "Account successfully deleted"
    # Validation on who is logged in (Checking if admin is accessing)
    if session['admin_logged_in']:
        return redirect(url_for('customer_account', success=success))
    else:
        session.clear()
        return redirect(url_for('home', success=success))


# <--- End of Customer Delete Account --->


# <--- Start of Logout (Admin and Customer) --->
@app.route('/logout')
def logout():
    username = session['username']
    print("For Programmer: SUCCESS --> {} has Successfully Logout".format(username))
    session.clear()
    success = "You have successfully logged out"
    return redirect(url_for('home', success=success))


# <--- End of Logout (Admin and Customer) --->


# <--- Start of Admin Login --->
@app.route('/loginAdmin', methods=['GET', 'POST'])
def login_admin():
    login_admin_form = LoginAdminForm(request.form)
    if request.method == 'POST' and login_admin_form.validate():
        # Admin Username and Password (Hardcoded)
        admin = "Admin"
        password = "12345678"
        # Login validation (Checking if matches with username and password)
        if admin == login_admin_form.username.data and password == login_admin_form.password.data:
            session['admin_logged_in'] = True
            session['username'] = "Admin"
            print("For Programmer: SUCCESS --> Admin has successfully logged in (Authority)")
            print("For Programmer: INFORMATION --> admin_logged_in = TRUE")
            success = "You have successfully logged in"
            return redirect(url_for('home', success=success))
        else:
            print("For Programmer: ERROR --> Invalid Admin login")
            error = "Invalid login"
            return render_template('loginAdmin.html', form=login_admin_form, error=error)
    return render_template('loginAdmin.html', form=login_admin_form)


# <--- End of Admin Login --->


# <--- Start of Admin Account Management --->
@app.route('/customerAccount')
def customer_account():
    try:
        if session['admin_logged_in']:
            customer_dict = {}
            db = shelve.open('storage.db', 'c')
            session['username'] = "Admin"
            try:
                customer_dict = db['Customers']
                print("For Programmer: SUCCESS --> Success in retrieving Customers from storage.db")
            except:
                print("For Programmer: ERROR --> Error in retrieving Customers from storage.db")
            db.close()

            customer_list = []
            if customer_dict:
                for key in customer_dict:
                    customer = customer_dict.get(key)
                    customer_list.append(customer)
                return render_template('customerAccount.html', count=len(customer_list), customer_list=customer_list)
            else:
                print("For Programmer: INFORMATION --> There are zero records")
                return render_template('customerAccount.html', count=0)
    except:
        print("For Programmer: THREAT --> Someone is trying to break the system")
        return redirect(url_for('error_render'))


# <--- End of Admin Account Management --->


# <--- Start of Customer Forget Password --->
@app.route('/forgetPassword', methods=['GET', 'POST'])
def forget_password():
    forget_password_form = ForgetPasswordForm(request.form)
    if request.method == 'POST' and forget_password_form.validate():
        customer_dict = {}
        db = shelve.open('storage.db', 'c')
        try:
            customer_dict = db['Customers']
            print("For Programmer: SUCCESS --> Success in retrieving Customers from storage.db")
        except:
            print("For Programmer: ERROR --> Error in retrieving Customers from storage.db")
        if customer_dict:
            for key in customer_dict:
                email = customer_dict[key].get_email()
                firstname = customer_dict[key].get_firstName()
                lastname = customer_dict[key].get_lastName()
                # Email Validation (Check if email entered is in records)
                if email == forget_password_form.email.data:
                    new_password = Email.Email(email, firstname, lastname)
                    customer_dict[key].set_password(new_password)
                    print('For Programmer: SUCCESS --> Password has been successfully changed')
                    # Set to true so that user will have to reset their password
                    customer_dict[key].set_reset_pass(True)
                    db['Customers'] = customer_dict
                    success = "An email have been sent to {}".format(forget_password_form.email.data)
                    return render_template('forgetPassword.html', form=forget_password_form, success=success)
                else:
                    print("For Programmer: Invalid email")
                    error = "Invalid Email"
                    return render_template('forgetPassword.html', form=forget_password_form, error=error)
        else:
            # If dictionary was empty
            print("For Programmer: ERROR --> No record found")
            error = "Invalid Email"
            return render_template('forgetPassword.html', form=forget_password_form, error=error)
        db.close()
    return render_template('forgetPassword.html', form=forget_password_form)


# <--- End of Customer Forget Password --->


# <--- Start of Customer Reset Password --->
@app.route('/resetPassword', methods=['GET', 'POST'])
def reset_password():
    try:
        if session['logged_in']:

            reset_password_form = ResetPasswordForm(request.form)
            if request.method == 'POST' and reset_password_form.validate():
                customer_dict = {}
                db = shelve.open('storage.db', 'c')
                try:
                    customer_dict = db['Customers']
                    print("For Programmer: SUCCESS --> Success in retrieving Customers from storage.db")
                except:
                    print("For Programmer: ERROR --> Error in retrieving Customers from storage.db")
                for key in customer_dict:
                    password = customer_dict[key].get_password()
                    new_password = reset_password_form.confirm_password.data
                    # Current password validation (Check if current password entered by user matches in dictionary)
                    if password == reset_password_form.current_password.data:
                        customer_dict[key].set_password(new_password)
                        customer_dict[key].set_reset_pass(False)
                        db['Customers'] = customer_dict
                        print("For Programmer: SUCCESS --> {} password has been changed".format(
                            customer_dict[key].get_username()))
                        success = "Your password has been changed"
                        return redirect(url_for('customer_profile', success=success))
                    else:
                        print("For Programmer: ERROR --> Invalid Password")
                        error = "Invalid Password"
                        return render_template('resetPassword.html', form=reset_password_form, error=error)
            return render_template('resetPassword.html', form=reset_password_form)
    except:
        print("For Programmer: THREAT --> Someone is trying to break the system")
        return redirect(url_for('error_render'))


# <--- End of Customer Reset Password --->


# <------------------------------------------------------->
# <------------------ FAQ (Arif's Code) ------------------>
# <------------------------------------------------------->
# <--- Start of FAQ Display page with form --->
@app.route('/FAQ', methods=['GET', 'POST'])
def faq():
    faq_dict = {}
    create_faq_form = CreateFaqForm(request.form)
    try:
        db = shelve.open('storage.db',
                         'c')  # argument is 'c', so guaranteed that it will create, concerning a warning from another line
        faq_dict = db["FAQ"]
    except KeyError:
        print("Error in retrieving storage.db, recreating storage.db.")

    # Function below used multiple times, only for translation of data
    def displayers(faq_dict_func):
        q_list = []
        u_count = 0
        a_count = 0
        for key in faq_dict_func:
            question = faq_dict_func.get(key)
            q_list.append(question)
            if question.get_answer() == '':
                u_count += 1
            else:
                a_count += 1
        return q_list, u_count, a_count

    if request.method == 'POST' and create_faq_form.validate():
        if create_faq_form.question.data != '' and create_faq_form.answer.data == '':
            faq_details = FAQ.FAQ(create_faq_form.question.data, session['username'])
            faq_dict[faq_details.get_id()] = faq_details
            create_faq_form.question.data = ''

        db['FAQ'] = faq_dict

        faq_dict = db['FAQ']
        try:
            faq = faq_dict[faq_details.get_id()]
            print("\"" + str(faq.get_question()) + "\" question was stored in storage.db successfully with id ==",
                  faq.get_id())
        except KeyError:
            error = "Question failed to upload (KeyError). Log out and sign in again"
            print("KeyError in retrieving latest input, likely it was blank. This error is expected.")
            question_list, unanswered_count, answered_count = displayers(faq_dict)
            return render_template("faq.html", form=create_faq_form, count=len(question_list),
                                   question_list=question_list,
                                   unanswered_count=unanswered_count,
                                   answered_count=answered_count,
                                   error=error)
        except UnboundLocalError:
            error = "Question failed to upload (UnboundLocalError). Log out and sign in again"
            print("UnboundLocalError in retrieving latest input, likely it was blank. This error is expected.")
            question_list, unanswered_count, answered_count = displayers(faq_dict)
            return render_template("faq.html", form=create_faq_form, count=len(question_list),
                                   question_list=question_list,
                                   unanswered_count=unanswered_count,
                                   answered_count=answered_count,
                                   error=error)
        else:
            success = 'Your question has been uploaded! The admins will upload their answer soon within the week!'
            question_list, unanswered_count, answered_count = displayers(faq_dict)
            return render_template("faq.html", form=create_faq_form, count=len(question_list),
                                   question_list=question_list,
                                   unanswered_count=unanswered_count,
                                   answered_count=answered_count,
                                   success=success)
    question_list, unanswered_count, answered_count = displayers(faq_dict)
    db.close()

    return render_template("faq.html", form=create_faq_form, count=len(question_list),
                           question_list=question_list,
                           unanswered_count=unanswered_count,
                           answered_count=answered_count)


# <--- End of FAQ Display page with form --->


# <--- Start of FAQ answering page with form, for admin --->
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


# <--- End of FAQ answering page with form, for admin --->


# <--- Start of FAQ deletion page, for admin --->
@app.route("/FAQdelete/<int:id>/", methods=['POST'])
def faqdelete(id):
    faq_dict = {}
    db = shelve.open("storage.db", 'w')
    faq_dict = db["FAQ"]

    faq = faq_dict.pop(id)

    db['FAQ'] = faq_dict
    db.close()

    return redirect(url_for("faq"))


# <--- End of FAQ deletion page, for admin --->

# <------------------------------------------------------->
# <--------- Store Management (Tong Wei's Codes)---------->
# <------------------------------------------------------->

@app.route('/storeManage')
def store_manage():
    print('load', flush=True)
    db = shelve.open('storage.db', 'c')
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


@app.route('/uploadProduct', methods=['GET', 'POST'])
def upload_product():
    print('upload', flush=True)
    form = Createproduct()
    Uploadfield = Uploadimage()
    # form.validate()
    # print(form.errors.items())

    if form.validate_on_submit() and Uploadfield.validate_on_submit():
        products_dict = {}
        db = shelve.open('storage.db', 'c')

        try:
            products_dict = db['Products']

        except:
            print("Error in retrieving Products from storage.db.")

        image = request.files[Uploadfield.productImage.name]
        # product is an object
        product = Products.Products(form.productName.data, form.productPrice.data, form.productDescription.data,
                                    form.productQuantity.data)
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


@app.route('/editProduct/<id>', methods=['GET', 'POST'])
def edit_product(id):
    Editproduct = Createproduct()
    print(id, flush=True)
    print("Form done", flush=True)
    if request.method == 'POST' and Editproduct.validate():
        products_dict = {}
        db = shelve.open('storage.db', 'w')
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
        product.set_price(Editproduct.productPrice.data)
        product.set_description(Editproduct.productDescription.data)
        product.set_quantity(Editproduct.productQuantity.data)
        db['Products'] = products_dict
        db.close()
        return redirect(url_for('store_manage'))
    else:
        products_dict = {}
        db = shelve.open('storage.db', 'r')
        products_dict = db['Products']
        db.close()

        product = products_dict.get(id)
        image = product.get_image()

        Editproduct.productName.data = product.get_name()
        Editproduct.productPrice.data = product.get_price()
        Editproduct.productDescription.data = product.get_description()
        Editproduct.productQuantity.data = product.get_quantity()

    return render_template('storeManage/editProduct.html', form=Editproduct, image=image)


@app.route('/deleteProduct/<id>', methods=['POST'])
def delete_products(id):
    products_dict = {}
    db = shelve.open('storage.db', 'w')
    products_dict = db['Products']

    image = products_dict[id].get_image()
    os.remove(os.path.join(os.getcwd(), 'static', 'img', image))

    products_dict.pop(id)

    db['Products'] = products_dict
    db.close()

    return redirect(url_for('store_manage'))


@app.route('/storeView/<id>/', methods=['GET'])
def store_view(id):
    db = shelve.open('storage.db', 'c')
    try:
        products_dict = db['Products']
    except KeyError:
        print('error retrieving products dict')
        products_dict = {}

    print(products_dict, flush=True)

    product = products_dict[id]

    return render_template('storeManage/storeView.html', product=product)


@app.route('/customerView/<id>/', methods=['GET'])
def customer_view(id):
    db = shelve.open('storage.db', 'c')
    try:
        products_dict = db['Products']
    except KeyError:
        print('error retrieving products dict')
        products_dict = {}

    print(products_dict, flush=True)

    product = products_dict[id]

    return render_template('storeManage/customerView.html', product=product)


@app.route('/customerProduct', methods=['GET'])
def customer_product():
    db = shelve.open('storage.db', 'c')
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


# <------------------------------------------------------->
# <--------------- Reviews (Suja's Codes)----------------->
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


        review = Review.Review(create_review_form.ratings.data, create_review_form.product_name.data,
                               create_review_form.email.data, create_review_form.comments.data)
        reviews_dict[review.get_review_id()] = review
        db['Reviews'] = reviews_dict

        db.close()

        return redirect(url_for('retrieve_users'))
    return render_template('createreview.html', form=create_review_form)


@app.route('/allreviews')
def retrieve_users():
    reviews_dict = {}
    db = shelve.open('storage.db', 'r')
    try:
        reviews_dict = db['Reviews']
    except KeyError:
        print('error retrieving reviews dict')
        reviews_dict = {}

    reviews_list = []
    for key in reviews_dict:
        review = reviews_dict.get(key)
        reviews_list.append(review)

    return render_template('allreviews.html', count=len(reviews_list), reviews_list=reviews_list)


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

    return render_template('staffreview.html', count=len(reviews_list), reviews_list=reviews_list)


@app.route('/updatereview/<int:id>/', methods=['GET', 'POST'])
def update_review(id):
    update_review_form = CreateReviewForm(request.form)
    if request.method == 'POST' and update_review_form.validate():
        reviews_dict = {}
        db = shelve.open('storage.db', 'w')
        reviews_dict = db['Reviews']

        review = reviews_dict.get(id)
        review.set_ratings(update_review_form.ratings.data)
        review.set_product_name(update_review_form.product_name.data)
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
        update_review_form.product_name.data = review.get_product_name()
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



# <------------------------------------------------------->
# <--- Shopping Cart & Transaction (Michael's Codes) ----->
# <------------------------------------------------------->

@app.route('/addCart/<id>/<int:qty>', methods=['GET'])
def addCart(id, qty):
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
def updateCart(id, qty):
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
    return ("", 204)


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


@app.route("/transaction", methods=['GET', 'POST'])
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

    return render_template('transaction/transaction.html', form=Create_Transaction_Form, cart_list=cart_list,
                           total=total)


@app.route('/confirm', methods=['GET', 'POST'])
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
    return render_template('transaction/confirmTransaction.html', products_list=cart_list, customer=customer,
                           total=total)


@app.route('/Paid')
def paid():
    user_id = session['user_id']
    db = shelve.open('storage.db', 'r')
    customer_dict = db['Customers']
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
        product = user_cart.get(key)
        total = total + product.get_total()
        cart_list.append(product)
    db = shelve.open('cart.db', 'c')
    cart_dict = db['cart']
    cart_dict[user_id] = ''
    db['cart'] = cart_dict
    db.close()
    return render_template('transaction/paid.html', products_list=cart_list, customer=customer, total=total)


if __name__ == "__main__":
    app.run(debug=True)
