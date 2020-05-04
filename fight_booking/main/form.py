from flask_wtf import Form
from wtforms import StringField, SubmitField, validators, SelectField, TextAreaField, SelectMultipleField ,widgets
from wtforms.fields.html5 import EmailField


class FormUserInfo(Form):
    """
    notes：使用者資料編修
    edit_date：20180317
    editor：Shaoe.Chen
    """

    user_fullname = StringField('Full name', validators=[
        validators.DataRequired()
    ])

    passportID = StringField('Passport', validators=[
        validators.DataRequired()
    ])

    contactNo = StringField('Contact number', validators=[
        validators.DataRequired()
    ])



    address = TextAreaField('Address', validators=[
        validators.DataRequired(),
        validators.Length(1, 20)
    ])

    #  使用下拉選單來選擇性別
    gender = SelectField('Gender', validators=[
        validators.DataRequired()
     ], choices=[('F', 'Female'), ('M', 'Man')])
    submit = SubmitField('Submit UserInfo')

    #  建立MultiCheckboxField
class MultiCheckboxField(SelectMultipleField):
        widget = widgets.ListWidget(prefix_label=False)
        option_widget = widgets.CheckboxInput()

class FormRole_Func_manager(Form):
        """
        角色權限管理界面
        """
        all_function_option = MultiCheckboxField('all_function', coerce=int)
        submit = SubmitField('submit')

class Form_User_Role_manager(Form):
    """
    使用者角色管理界面
    """
    all_role_option = MultiCheckboxField('all_role', coerce=int)
    submit = SubmitField('submit')