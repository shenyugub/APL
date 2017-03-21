from flask_wtf import FlaskForm
from wtforms import StringField, HiddenField, IntegerField, FileField, SelectMultipleField, widgets, TextAreaField
from wtforms.validators import DataRequired, Email, Optional
from app.models import Industry, InvestmentPhase


class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


class ProfileForm(FlaskForm):
    avatar = HiddenField()
    email = StringField()
    name = StringField(validators=[DataRequired()])
    phone = StringField(validators=[DataRequired()])
    wechat = StringField()
    company = StringField()
    gender = StringField()
    resume = TextAreaField()

    interested = MultiCheckboxField(choices=[(name, member.value) for name, member in Industry.__members__.items()])
    invest_role = StringField()
    investment_min = IntegerField()
    investment_max = IntegerField()
    invest_phase = MultiCheckboxField(choices=[(name, member.value) for name, member in InvestmentPhase.__members__.items()])

    run_mode = HiddenField()
    oss_access_key_id = HiddenField(id='OSSAccessKeyId')
    token = HiddenField(id='x-oss-security-token')
    policy = HiddenField(id='policy')
    Signature = HiddenField('Signature')
    key = HiddenField(id='key')
    success_action_status = HiddenField(id='success_action_status')
    callback = HiddenField(id='callback')
    uid = HiddenField(id="x:uid")
    origin_filename = HiddenField(id='x:filename')

    def __str__(self):
        return 'email = {}\n name = {}\n phone = {}\n wechat = {}\n company = {}\n gender = {}\n ' \
               'avatar = {}\n resume = {}\n interested = {}\n invest_role = {}\n min = {}\n max = {}\n invest_phase = {}'\
            .format(self.email.data, self.name.data, self.phone.data, self.wechat.data, self.company.data, self.gender.data, self.avatar.data,
                    self.resume.data, self.interested.data, self.invest_role.data, self.investment_min.data, self.investment_max.data, self.invest_phase.data)


class CommentForm(FlaskForm):
    content = TextAreaField(validators=[DataRequired()])
    pid = HiddenField()
    source = HiddenField()
