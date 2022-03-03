from flask import Flask, render_template, request, redirect, url_for
from Forms import Createproduct, Uploadimage
import shelve, os
from Products import Products

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.secret_key = r'.monke[yare)cute/'


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/base')
def base():
    return render_template('base.html')

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
        product = Products(form.productName.data, form.productPrice.data, form.productDescription.data, form.productQuantity.data)
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


    return render_template('storeManage/customerProduct.html', products_list=products_list)
if __name__ == '__main__':
    app.run(debug=True)
