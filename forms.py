from flask.ext.wtf import Form
from wtforms.fields import IntegerField
from wtforms.validators import Required
from weather_app.models import User

class EditAlertForm(Form):

    hrs = IntegerField('hrs', validators = [Required()])
    pop = IntegerField('pop', validators = [Required()])