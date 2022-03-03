from wtforms import StringField, validators, DecimalField, FileField, IntegerField
from decimal import ROUND_HALF_UP
from wtforms.validators import DataRequired, NumberRange
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileRequired  # for upload of image restrict only images jpg png

class Createproduct(FlaskForm):
    productName = StringField('Product Name', validators=[validators.Length(min=1, max=100), DataRequired()])
    productPrice = DecimalField('Product Price', places=2, rounding=ROUND_HALF_UP, use_locale=False, number_format=None, validators=[DataRequired(message='Please key in 2 decimal point')])
    productDescription = StringField('Product Description', validators=[DataRequired()])
    productQuantity = IntegerField('Quantity', validators=[NumberRange(min=1)])
    updateImage = FileField('', validators=[FileAllowed(['jpg', 'png'], 'IMAGES ONLY')])

class Uploadimage(FlaskForm):
    productImage = FileField('', validators=[FileAllowed(['jpg', 'png'], 'IMAGES ONLY'), FileRequired()])
