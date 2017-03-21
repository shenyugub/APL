from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, HiddenField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, Length


class LoginForm(FlaskForm):
    email = StringField(validators=[DataRequired('请输入 Email'), Email('请输入 Email')])
    password = PasswordField(validators=[DataRequired('请输入密码')])
    vcode = StringField(validators=[DataRequired('请输入4位验证码'), Length(4, 4, '请输入4位验证码')])


class ResetPasswordForm(FlaskForm):
    old_password = PasswordField(validators=[DataRequired()])
    new_password = PasswordField(validators=[DataRequired()])


class ForgetPasswordForm(FlaskForm):
    email = StringField(validators=[DataRequired('请输入 Email'), Email()])
    code = StringField(validators=[DataRequired('请输入4位验证码'), Length(4, 4, '请输入4位验证码')])
    password = PasswordField(validators=[DataRequired('请输入密码')])
