from wtforms import Form, StringField, SelectField, validators, PasswordField, TextAreaField, DecimalField, FileField, IntegerField, RadioField
from wtforms_validators import Alpha, AlphaNumeric, Integer
from wtforms.validators import DataRequired, NumberRange
from wtforms.fields.html5 import EmailField, DateField
from datetime import date
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileRequired  # for upload of image restrict only images jpg png


# Customer Register Form
class CreateCustomerForm(Form):
    first_name = StringField('First Name*', [validators.Length(min=1, max=50, message='Must only have 1-50 characters'),
                                             Alpha(message='Must only contain letters with no spacing'),
                                             validators.DataRequired()])
    last_name = StringField('Last Name*', [validators.Length(min=1, max=50, message='Must only have 1-50 characters'),
                                           Alpha(message='Must only contain letters with no spacing'),
                                           validators.DataRequired()])
    username = StringField('Username*', [validators.Length(min=4, max=25, message='Must only have 4-25 characters'),
                                         AlphaNumeric(message='Must only contain letters and numbers'),
                                         validators.DataRequired()])
    email = EmailField('Email Address*', [validators.DataRequired(message='Please enter a valid Email')])
    gender = SelectField('Gender*', [validators.DataRequired()],
                         choices=[('', 'Select'), ('Male', 'Male'), ('Female', 'Female')], default='Male')
    DOB = DateField('Date of Birth*', [validators.DataRequired()], default=date.today())
    password = PasswordField('Password*', [validators.Length(min=8, max=50), validators.DataRequired(),
                                           validators.EqualTo('confirm', message='password do not match')])
    confirm = PasswordField('Confirm Password*', [validators.Length(min=8, max=50), validators.DataRequired()])
    phone_number = StringField('Phone Number*', [validators.Length(min=8, max=10), validators.DataRequired()])

    # Payment part
    address = StringField('Address', [validators.Length(min=1, max=50)])
    postal = StringField('Zip or Postal Code', [validators.Length(min=6, max=6, message='There must only be 6 digits'),
                                                Integer(message='There must only be 6 digits')])
    payment_type = SelectField('Payment Type', [validators.DataRequired()],
                               choices=[('', 'Select'), ('Visa', 'Visa'), ('Mastercard', 'Mastercard'),
                                        ('American Express', 'American Express')], default='Visa')
    card_number = StringField('Credit Card Number',
                              [validators.Length(min=16, max=16, message='There must only be 16 digits'),
                               Integer(message='There must only be 16 digits')])
    # Dropdown list for month and year
    expiry = DateField('Expiry Date')
    security_code = StringField('Security Code', [validators.Length(min=3, max=3), Integer()])
    reset_pass = False

    # Validation on date and phone
    def validate_on_date(self):
        result = super(CreateCustomerForm, self).validate()
        if self.DOB.data >= date.today() or self.expiry.data <= date.today():
            print("invalid date")
            return False
        else:
            return result

    def validate_on_phone(self):
        result = super(CreateCustomerForm, self).validate()
        if not (self.phone_number.data[0] in ("6", "8", "9")):
            print("invalid number")
            return False
        else:
            return result


class UpdateCustomerForm(Form):
    first_name = StringField('', [validators.Length(min=1, max=50, message='Must only have 1-50 characters'),
                                  Alpha(message='Must only contain letters with no spacing'),
                                  validators.DataRequired()])
    last_name = StringField('', [validators.Length(min=1, max=50, message='Must only have 1-50 characters'),
                                 Alpha(message='Must only contain letters with no spacing'), validators.DataRequired()])
    username = StringField('', [validators.Length(min=4, max=25, message='Must only have 4-25 characters'),
                                AlphaNumeric(message='Must only contain letters and numbers'),
                                validators.DataRequired()])
    email = EmailField('', [validators.DataRequired(message='Please enter a valid Email')])
    gender = SelectField('', [validators.DataRequired()],
                         choices=[('', 'Select'), ('Male', 'Male'), ('Female', 'Female')], default='Male')
    DOB = DateField('', [validators.DataRequired()])
    phone_number = StringField('', [validators.Length(min=8, max=10), validators.DataRequired()])

    # Payment part
    address = StringField('', [validators.Length(min=1, max=50)])
    postal = StringField('', [validators.Length(min=6, max=6, message='There must only be 6 digits'),
                              Integer(message='There must only be 6 digits')])
    payment_type = SelectField('', [validators.DataRequired()],
                               choices=[('', 'Select'), ('Visa', 'Visa'), ('Mastercard', 'Mastercard'),
                                        ('American Express', 'American Express')], default='Visa')
    card_number = StringField('', [validators.Length(min=16, max=16, message='There must only be 16 digits'),
                                   Integer(message='There must only be 16 digits')])
    # Might have a dropdown list
    expiry = DateField("")
    security_code = StringField('', [validators.Length(min=3, max=3), Integer()])

    # Validation on date and phone
    def validate_on_date(self):
        result = super(UpdateCustomerForm, self).validate()
        if self.DOB.data >= date.today() or self.expiry.data <= date.today():
            print("invalid date")
            return False
        else:
            return result

    def validate_on_phone(self):
        result = super(UpdateCustomerForm, self).validate()
        if not (self.phone_number.data[0] in ("6", "8", "9")):
            print("invalid number")
            return False
        else:
            return result


# Customer Login Form
class LoginCustomerForm(Form):
    username = StringField('Username', [validators.Length(min=1, max=25), validators.DataRequired()])
    password = PasswordField('Password', [validators.Length(min=1, max=50), validators.DataRequired()])


# Admin Login Form
class LoginAdminForm(Form):
    username = StringField('Username', [validators.Length(min=1, max=25), validators.DataRequired()])
    password = PasswordField('Password', [validators.Length(min=1, max=50), validators.DataRequired()])


# FAQ Creation Form
class CreateFaqForm(Form):
    question = StringField('', [validators.Optional()])
    answer = TextAreaField('Answer this question.', [validators.Optional()], render_kw={"rows": 10, "cols": 120})
    username = StringField('', [validators.Optional()])


# Forget Password Form
class ForgetPasswordForm(Form):
    email = EmailField('Email Address', [validators.DataRequired(message='Please enter a valid Email')])


# Reset Password Form
class ResetPasswordForm(Form):
    current_password = PasswordField('Current Password*', [validators.Length(min=8, max=50), validators.DataRequired()])
    new_password = PasswordField('New Password*', [validators.Length(min=8, max=50), validators.DataRequired(),
                                               validators.EqualTo('confirm_password', message='password do not match')])
    confirm_password = PasswordField('Confirm New Password*', [validators.Length(min=8, max=50), validators.DataRequired()])


# Reviews
class CreateReviewForm(Form):
    ratings = RadioField('Ratings', [validators.DataRequired()], choices=[('5 stars', '5 stars'), ('4 stars', '4 stars'), ('3 stars', '3 stars'), ('2 stars', '2 stars'), ('1 star', '1 star')], default='5 stars')
    product_name = StringField('Product Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    email = EmailField('Email', [validators.DataRequired(message='Please enter a valid Email')])
    comments = TextAreaField('Comments', [validators.Optional()])


# StoreManage
class Createproduct(FlaskForm):
    productName = StringField('Product Name', validators=[validators.Length(min=1, max=100), DataRequired()])
    productPrice = DecimalField('Product Price', use_locale=False, number_format=None, validators=[DataRequired()])
    productDescription = StringField('Product Description', validators=[DataRequired()])
    stock = IntegerField('Stock', validators=[NumberRange(min=1)])
    updateImage = FileField('', validators=[FileAllowed(['jpg', 'png'], 'IMAGES ONLY')])


class Uploadimage(FlaskForm):
    productImage = FileField('', validators=[FileAllowed(['jpg', 'png'], 'IMAGES ONLY'), FileRequired()])
    
class CreateTransactionForm(Form):
    first_name = StringField('First Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    last_name = StringField('Last Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    username = StringField('Username', [validators.Length(min=1, max=150), validators.DataRequired()])
    email = StringField('Email', [validators.Length(min=1, max=150), validators.DataRequired(), validators.Email()])
    address = StringField('Address', [validators.Length(min=1, max=150), validators.DataRequired()])

    postal = IntegerField('Zip or postal code', [validators.Length(min=5, max=10), validators.DataRequired()])
    payment_method = SelectField('Method', [validators.DataRequired()], choices=["Credit card", "Debit card", "Paypal"])
    cc_name = StringField('Name on card', [validators.Length(min=1, max=150), validators.DataRequired()])
    cc_number = IntegerField('Credit card number', [validators.Length(min=13, max=19), validators.DataRequired()])
    cc_expiration = DateField('Expiration', [validators.DataRequired()])
    cc_cvv = IntegerField('CVV', [validators.Length(min=3, max=4), validators.DataRequired()])

