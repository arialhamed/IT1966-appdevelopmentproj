class CreateTransactionForm(Form):
    first_name = StringField('First Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    last_name = StringField('Last Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    username = StringField('Username', [validators.Length(min=1, max=150), validators.DataRequired()])
    email = StringField('Email', [validators.Length(min=1, max=150), validators.DataRequired(), validators.Email()])
    address = StringField('Address', [validators.Length(min=1, max=150), validators.DataRequired()])

    postal = IntegerField('Zip or postal code', [validators.Length(min=5, max=10), validators.DataRequired()])
    payment_type = SelectField('Payment Type', [validators.DataRequired()], choices=[('', 'Select'), ('Visa', 'Visa'), ('Mastercard', 'Mastercard'), ('American Express', 'American Express')], default='Visa')
    cc_name = StringField('Name on card', [validators.Length(min=1, max=150), validators.DataRequired()])
    card_number = IntegerField('Credit card number', [validators.Length(min=13, max=19), validators.DataRequired()])
    expiry = DateField('Expiry Date',[validators.DataRequired()])
    security_code = IntegerField('Security Code', [validators.Length(min=3, max=4), validators.DataRequired()])
