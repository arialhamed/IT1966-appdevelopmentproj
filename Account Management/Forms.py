# Forms using wtforms
from wtforms import Form, StringField, SelectField, validators, PasswordField
from wtforms_validators import Alpha, AlphaNumeric, Integer
from wtforms.fields.html5 import EmailField, DateField
from datetime import date


# Customer Register Form
class CreateCustomerForm(Form):
    first_name = StringField('First Name*', [validators.Length(min=1, max=50, message='Must only have 1-50 characters'), Alpha(message='Must only contain letters with no spacing'), validators.DataRequired()])
    last_name = StringField('Last Name*', [validators.Length(min=1, max=50, message='Must only have 1-50 characters'), Alpha(message='Must only contain letters with no spacing'), validators.DataRequired()])
    username = StringField('Username*', [validators.Length(min=4, max=25, message='Must only have 4-25 characters'), AlphaNumeric(message='Must only contain letters and numbers'), validators.DataRequired()])
    email = EmailField('Email Address*', [validators.DataRequired(message='Please enter a valid Email')])
    gender = SelectField('Gender*', [validators.DataRequired()], choices=[('', 'Select'), ('Male', 'Male'), ('Female', 'Female')], default='Male')
    DOB = DateField('Date of Birth*', [validators.DataRequired()], default=date.today())
    password = PasswordField('Password*', [validators.Length(min=8, max=50), validators.DataRequired(), validators.EqualTo('confirm', message='password do not match')])
    confirm = PasswordField('Confirm Password*', [validators.Length(min=8, max=50), validators.DataRequired()])
    phone_number = StringField('Phone Number*', [validators.Length(min=8, max=10), validators.DataRequired()])

    # Payment part
    address = StringField('Address', [validators.Length(min=1, max=50)])
    postal = StringField('Zip or Postal Code', [validators.Length(min=6, max=6, message='There must only be 6 digits'), Integer(message='There must only be 6 digits')])
    payment_type = SelectField('Payment Type', [validators.DataRequired()], choices=[('', 'Select'), ('Visa', 'Visa'), ('Mastercard', 'Mastercard'), ('American Express', 'American Express')], default='Visa')
    card_number = StringField('Credit Card Number', [validators.Length(min=16, max=16, message='There must only be 16 digits'), Integer(message='There must only be 16 digits')])
    expiry = DateField('Expiry Date')
    security_code = StringField('Security Code', [validators.Length(min=3, max=3), Integer()])

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
    first_name = StringField('', [validators.Length(min=1, max=50, message='Must only have 1-50 characters'), Alpha(message='Must only contain letters with no spacing'), validators.DataRequired()])
    last_name = StringField('', [validators.Length(min=1, max=50, message='Must only have 1-50 characters'), Alpha(message='Must only contain letters with no spacing'), validators.DataRequired()])
    username = StringField('', [validators.Length(min=4, max=25, message='Must only have 4-25 characters'), AlphaNumeric(message='Must only contain letters and numbers'), validators.DataRequired()])
    email = EmailField('', [validators.DataRequired(message='Please enter a valid Email')])
    gender = SelectField('', [validators.DataRequired()], choices=[('', 'Select'), ('Male', 'Male'), ('Female', 'Female')], default='Male')
    DOB = DateField('', [validators.DataRequired()])
    phone_number = StringField('', [validators.Length(min=8, max=10), validators.DataRequired()])

    # Payment part
    address = StringField('', [validators.Length(min=1, max=50)])
    postal = StringField('', [validators.Length(min=6, max=6, message='There must only be 6 digits'), Integer(message='There must only be 6 digits')])
    payment_type = SelectField('', [validators.DataRequired()], choices=[('', 'Select'), ('Visa', 'Visa'), ('Mastercard', 'Mastercard'), ('American Express', 'American Express')], default='Visa')
    card_number = StringField('', [validators.Length(min=16, max=16, message='There must only be 16 digits'), Integer(message='There must only be 16 digits')])
    expiry = DateField('', )
    security_code = StringField('', [validators.Length(min=3, max=3), Integer()])

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


# Forget Password Form
class ForgetPasswordForm(Form):
    email = EmailField('Email Address', [validators.DataRequired(message='Please enter a valid Email')])


class ResetPasswordForm(Form):
    current_password = PasswordField('Current Password*', [validators.Length(min=8, max=50), validators.DataRequired()])
    new_password = PasswordField('Password*', [validators.Length(min=8, max=50), validators.DataRequired(), validators.EqualTo('confirm_password', message='password do not match')])
    confirm_password = PasswordField('Confirm Password*', [validators.Length(min=8, max=50), validators.DataRequired()])
