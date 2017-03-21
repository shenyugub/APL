from flask_wtf import FlaskForm
from wtforms import StringField, HiddenField, SelectField, DateField, BooleanField, TextAreaField, SelectMultipleField, widgets
from wtforms.validators import DataRequired, Email
from app.models import Industry, Gender, CompanyPhase, FinancingMode, ServiceCategory


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

    company_name = StringField()
    company_desc = TextAreaField()
    company_industry = SelectField(choices=[[name, member.value] for name, member in Industry.__members__.items()])

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
               'avatar = {}\n resume = {}\n company_name = {}\n company_desc = {}\n company_industry = {}' \
            .format(self.email.data, self.name.data, self.phone.data, self.wechat.data, self.company.data, self.gender.data, self.avatar.data,
                    self.resume.data, self.company_name.data, self.company_desc.data, self.company_industry.data)


class ProjectForm(FlaskForm):
    logo_url = HiddenField()
    name = StringField(validators=[DataRequired()])
    description = TextAreaField(validators=[DataRequired()])
    advantage = TextAreaField()
    industry = SelectField(validators=[DataRequired()], choices=[(name, member.value) for name, member in Industry.__members__.items()])
    company_phase = SelectField(choices=[(name, member.value) for name, member in CompanyPhase.__members__.items()])
    financing_sum = StringField(validators=[DataRequired()])
    # project_phase = StringField()
    bp_url = HiddenField()  # 考虑放hidden field里面
    duration = StringField()  # 概念阶段预计开发时间
    financing_mode = SelectField(choices=[(name, member.value) for name, member in FinancingMode.__members__.items()])
    financing_status = TextAreaField()  # 融资情况
    deadline = DateField()
    contact_name = StringField()
    contact_phone = StringField()
    contact_email = StringField(Email())
    project_phase = MultiCheckboxField(choices=[(str(x), str(x)) for x in range(10000)])

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


class ServiceCustom(FlaskForm):
    title = StringField(validators=[DataRequired()])
    category = SelectField(choices=[(name, member.value) for name, member in ServiceCategory.__members__.items()])
    content = TextAreaField(validators=[DataRequired()])


