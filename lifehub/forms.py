from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, SubmitField, DateField
from wtforms.validators import DataRequired

class TodoForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    completed = SelectField('Completed', choices=[("False", "False"), ("True", "True")], validators=[DataRequired()])
    due_date = DateField('Due Date', format='%Y-%m-%d', validators=[DataRequired()])
    priority = SelectField(
        'Priority', 
        choices=[("Low", "Low"), ("Medium", "Medium"), ("High", "High")], 
        validators=[DataRequired()]
    )
    submit = SubmitField("Add Todo")
