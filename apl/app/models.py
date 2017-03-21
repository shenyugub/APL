#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/2/25 下午3:16
# @Author  : Rain
# @Desc    : 模型类
# @File    : models.py

from . import db
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, SignatureExpired, BadSignature
from flask import current_app
from flask_loginmanager import UserMixin
from enum import unique, Enum
from marshmallow import fields, Schema
from app.utils.utils import check_permission_values
from datetime import datetime
from sqlalchemy.orm import validates, MapperExtension


# 性别
class Gender(Enum):
    Male = '男'
    Female = '女'


# 项目所属行业
class Industry(Enum):
    IntelligentMake = '智能制造'
    IntelligentHardware = '智能硬件'
    AI = '人工智能'
    IoT = '物联网'
    Sensor = '传感器技术'
    NewMaterial = '新材料新能源'
    ArVr = 'AR/VR'
    Drone = '无人机'
    BigData = '大数据'
    Medicine = '医疗'
    Education = '教育'
    Finance = '金融'
    ConsumptionUpgrading = '消费升级'
    O2O = 'O2O'
    BlackTechnology = '黑科技'
    Others = '其他'


# 公司阶段
class CompanyPhase(Enum):
    Initial = '初创期'
    Seed = '种子期'
    Growing = '成长期'
    Extanding = '扩张期'
    Mature = '成熟期'
    PreIPO = 'Pre-IPO'


# 投资阶段
class InvestmentPhase(Enum):
    Seed = '种子轮'
    Angel = '天使轮'
    PreA = 'Pre-A 轮'
    RoundA = 'A 轮'
    RoundB = 'B 轮'
    RoundC = 'C 轮'
    RoundD = 'D 轮'
    RoundE = 'E 轮'


# 交付物状态
class AttachmentStatus(Enum):
    Submitting = '待提交'
    Submitted = '已提交'
    Rejected = '已驳回'
    Confirmed = '已确认'


# 服务项状态
class ServiceStatus(Enum):
    Submitting = '待提交'
    Submitted = '已提交'
    Ignoring = '请求忽略'
    Ignored = '已忽略'
    Rejected = '已驳回'
    Confirmed = '已确认'
    Finished = '已完成'


# 服务需求分类
class ServiceCategory(Enum):
    APL = 'APL 系统服务'
    Review = '研发评审'
    Development = '开发支持'
    Manufacture = '制造及供应链服务'
    Media = '媒体宣传'
    Others = '其他'


# 投资类型
class InvestmentType(Enum):
    Individual = '个人'
    Organization = '机构'


# 项目状态
class ProjectStatus(Enum):
    Submitting = '待提交'     # 提交前，或者提交后撤销了想修改，都是这个状态
    Submitted = '已提交'   # 已提交，待审核
    Rejected = '已驳回'
    Accepted = '已通过'


# 因为 MySQL BigInt 类型限制，权限项最多 （64 - 1） 个
@check_permission_values
@unique
class Permissions(Enum):
    ResetPassword = 1 << 0
    CreateUser = 1 << 1
    CreateAdmin = 1 << 2
    AuditProject = 1 << 3


class Const(object):
    RESULT_KEY = 'result'
    MESSAGE_KEY = 'message'
    STATUS_NOTFOUND = 404
    STATUS_ERROR = 400
    STATUS_DENIED = 401
    STATUS_OK = 200


class StartupExtension(MapperExtension):
    def before_insert(self, mapper, connection, instance):
        pass

    def before_update(self, mapper, connection, instance):
        instance.gmt_modified = datetime.now()


# 用户表
class Startup(db.Model, UserMixin):
    __tablename__ = 'startup'
    __mapper_args__ = {'extension': StartupExtension()}

    #系统信息
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    password = db.Column(db.String(32))
    permissions = db.Column(db.Integer)
    confirmed = db.Column(db.Boolean, default=True)                     # 初期应该用不到，因为没有开放注册，不需要邮件或短信确认
    initialized = db.Column(db.Boolean, default=False)                  # 第一次登录时需要填写个人资料、修改密码等
    active = db.Column(db.Boolean, default=True)                       # 被禁用的账户不能登陆、提示账户已被禁用
    gmt_create = db.Column(db.TIMESTAMP, nullable=False, default=db.func.now())
    gmt_modified = db.Column(db.TIMESTAMP, nullable=False, onupdate=db.func.now())
    last_login_time = db.Column(db.TIMESTAMP, nullable=False, default=db.func.now())   # 最后登录时间

    name = db.Column(db.String(10), default='')
    email = db.Column(db.String(50), unique=True)
    phone = db.Column(db.String(20), default='')
    wechat = db.Column(db.String(20), default='')                       # 微信号
    company = db.Column(db.String(40), default='')                      # 公司及职位
    gender = db.Column(db.Enum(Gender), default=Gender.Male)
    avatar = db.Column(db.String(200), default='')                      #头像 URL
    resume = db.Column(db.String(500), default='')                      #个人简介

    company_name = db.Column(db.String(30), default='')                 # 企业名称
    company_desc = db.Column(db.String(400), default='')                # 企业简介
    company_industry = db.Column(db.Enum(Industry), default=Industry.Others)                     # 所属行业

    projects = db.relationship('Project', backref='owner', lazy='dynamic')
    files = db.relationship('File', backref='owner', lazy='dynamic')
    tickets = db.relationship('Ticket', backref='owner', lazy='dynamic')
    schedules = db.relationship('Schedule', backref='startup', lazy='dynamic')

    @validates('state')
    def update_state(self, key, value):
        self.task.state = value
        return value

    def get_id(self):

        return self.id

    def get_permissions(self):
        return self.permissions

    def verify_password(self, password):
        return self.password == password

    def generate_auth_token(self, expiration):
        s = Serializer(current_app.config['SECRET_KEY'], expires_in=expiration)
        return s.dumps({'email': self.email}).decode('ascii')

    @staticmethod
    def verify_auth_token(token, expiration):

        s = Serializer(current_app.config['SECRET_KEY'], expires_in=expiration)

        try:
            print(s)
            data = s.loads(token)

        except SignatureExpired:
            return None
        except BadSignature:
            return None

        if 'email' in data:
            return Startup.query.filter_by(email=data['email']).first()
        return None

    def interested_value(self):
        values = self.interested.strip().split(',')
        result = []
        for v in values:
            if v.strip():
                result.append(Industry[v].value)
        return result

    def invest_phase_value(self):
        values = self.invest_phase.strip().split(',')
        result = []
        for v in values:
            if v.strip():
                result.append(InvestmentPhase[v].value)

        return result


class StartupSchema(Schema):
    type = fields.String()
    gender = fields.String()
    company_industry = fields.String()

    class Meta:
        additional = ('id', 'permissions', 'confirmed', 'initialized', 'active', 'gmt_create', 'gmt_modified', 'last_login_time',
                      'name', 'email', 'phone', 'wechat', 'company', 'avatar', 'resume',
                      'company_name', 'company_desc')

        ordered = True


class InvestorExtension(MapperExtension):
    def before_insert(self, mapper, connection, instance):
        pass

    def before_update(self, mapper, connection, instance):
        instance.gmt_modified = datetime.now()


class Investor(db.Model):
    __tablename__ = 'investor'
    __mapper_args__ = {'extension': InvestorExtension()}

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(10), default='')
    gmt_create = db.Column(db.TIMESTAMP, nullable=False, default=db.func.now())
    gmt_modified = db.Column(db.TIMESTAMP, nullable=False, onupdate=db.func.now())

    schedules = db.relationship('Schedule', backref='investor', lazy='dynamic')

    comments = db.relationship('Comment', backref='author', lazy='dynamic')


class ProjectExtension(MapperExtension):
    def before_insert(self, mapper, connection, instance):
        pass

    def before_update(self, mapper, connection, instance):
        instance.gmt_modified = datetime.now()


# 项目表
class Project(db.Model):
    __tablename__ = 'projects'
    __mapper_args__ = {'extension': ProjectExtension()}

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    owner_id = db.Column(db.Integer, db.ForeignKey(Startup.id))
    icon_url = db.Column(db.String(50), default='')
    name = db.Column(db.String(50), nullable=False)     # 项目名称
    description = db.Column(db.String(500))             # 项目介绍
    advantage = db.Column(db.String(100))               # 项目优势
    industry = db.Column(db.Enum(Industry), default=Industry.Others)             # 所属行业
    company_phase = db.Column(db.Enum(CompanyPhase), default=CompanyPhase.Initial)    # 创业阶段
    financing_sum = db.Column(db.Integer)               # 融资目标
    #项目阶段放到单独的表里
    bp_url = db.Column(db.String(50))                  # 商业计划书
    phase_start = db.Column(db.Integer)  # 阶段开始索引
    phase_index = db.Column(db.Integer)  # 阶段当前索引
    duration = db.Column(db.Integer)  #当前阶段预计开发时间
    financing_status = db.Column(db.String(100))
    contact_name = db.Column(db.String(50), nullable=False)     # 项目名称
    contact_phone = db.Column(db.String(50), nullable=False)     # 项目名称
    contact_email = db.Column(db.String(50), nullable=False)     # 项目名称
    deadline = db.Column(db.DateTime, default=datetime.now())
    status = db.Column(db.Enum(ProjectStatus), default=ProjectStatus.Submitting)
    gmt_create = db.Column(db.TIMESTAMP, nullable=False, default=db.func.now())
    gmt_modified = db.Column(db.TIMESTAMP, nullable=False, onupdate=db.func.now())

    # Checked
    comments = db.relationship('Comment', backref='project', lazy='dynamic')
    # Checked
    phases = db.relationship('ProjectPhase', back_populates='project')
    # Checked
    schedules = db.relationship('Schedule', backref='project', lazy='dynamic')


class ProjectSchema(Schema):
    industry = fields.String()
    company_phase = fields.String()
    status = fields.String()
    comments = fields.Nested('CommentSchema', many=True)
    phases = fields.Nested('ProjectPhaseSchema', many=True)

    class Meta:
        additional = ('id', 'owner_id', 'icon_url', 'name', 'description', 'advantage', 'financing_sum',
                      'bp_url', 'phase_start', 'phase_index', 'duration', 'financing_status', 'deadline', 'contact_name',
                      'contact_phone', 'contact_email', 'gmt_create', 'gmt_modified')


class PhaseExtension(MapperExtension):
    def before_insert(self, mapper, connection, instance):
        pass

    def before_update(self, mapper, connection, instance):
        instance.gmt_modified = datetime.now()


# 项目阶段表
class Phase(db.Model):
    __tablename__ = 'phases'
    __mapper_args__ = {'extension': PhaseExtension()}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(20))
    description = db.Column(db.String(200))
    gmt_create = db.Column(db.TIMESTAMP, nullable=False, default=db.func.now())
    gmt_modified = db.Column(db.TIMESTAMP, nullable=False, onupdate=db.func.now())

    # Checked
    projects = db.relationship('ProjectPhase', back_populates='phase')
    # Checked
    attachments = db.relationship('PhaseAttachment', back_populates='phase')


class PhaseSchema(Schema):
    atts = fields.Nested('AttachmentSchema', many=True)

    class Meta:
        additional = ('id', 'name', 'description', 'gmt_create', 'gmt_modified')
        ordered = False


class AttachmentExtension(MapperExtension):
    def before_insert(self, mapper, connection, instance):
        pass

    def before_update(self, mapper, connection, instance):
        instance.gmt_modified = datetime.now()


# 系统的交付物表
class Attachment(db.Model):
    __tablename__ = 'attachments'
    __mapper_args__ = {'extension': AttachmentExtension()}

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(20))
    description = db.Column(db.String(50))
    url = db.Column(db.String(50))
    gmt_create = db.Column(db.TIMESTAMP, nullable=False, default=db.func.now())
    gmt_modified = db.Column(db.TIMESTAMP, nullable=False, onupdate=db.func.now())

    # Checked
    phases = db.relationship('PhaseAttachment', back_populates='attachment')
    user_attachments = db.relationship('UserAttachment', backref='attachment', lazy='dynamic')


class AttachmentSchema(Schema):
    details = fields.Nested('PhaseAttachmentDetailSchema', many=True)

    class Meta:
        additional = ('id', 'name', 'description', 'gmt_create', 'gmt_modified')
        ordered = False


class PhaseAttachmentDetailExtension(MapperExtension):
    def before_insert(self, mapper, connection, instance):
        pass

    def before_update(self, mapper, connection, instance):
        instance.gmt_modified = datetime.now()


class PhaseAttachmentDetail(db.Model):
    __tablename__ = 'phase_attachment_details'
    __mapper_args__ = {'extension': PhaseAttachmentDetailExtension()}

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    uaid = db.Column(db.Integer, db.ForeignKey('user_attachments.id'))
    url = db.Column(db.String(50))
    comment = db.Column(db.String(200))
    gmt_create = db.Column(db.TIMESTAMP, nullable=False, default=db.func.now())
    gmt_modified = db.Column(db.TIMESTAMP, nullable=False, onupdate=db.func.now())


class PhaseAttachmentDetailSchema(Schema):
    class Meta:
        fields = ('id', 'uaid', 'url', 'comment', 'gmt_create', 'gmt_modified')
        ordered = False


class ProjectPhaseExtension(MapperExtension):
    def before_insert(self, mapper, connection, instance):
        instance.project_name = Project.query.get_or_404(instance.project_id).name
        instance.phase_name = Phase.query.get_or_404(instance.phase_id).name

    def before_update(self, mapper, connection, instance):
        instance.project_name = instance.project.name
        instance.phase_name = instance.phase.name

        instance.gmt_modified = datetime.now()


class ProjectPhase(db.Model):
    __tablename__ = 'projects_phases'
    __mapper_args__ = {'extension': ProjectPhaseExtension()}

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'))
    project_name = db.Column(db.String(30))
    phase_id = db.Column(db.Integer, db.ForeignKey('phases.id'))
    phase_name = db.Column(db.String(20))
    days = db.Column(db.Integer)
    status = db.Column(db.Integer)
    gmt_create = db.Column(db.TIMESTAMP, nullable=False, default=db.func.now())
    gmt_modified = db.Column(db.TIMESTAMP, nullable=False, onupdate=db.func.now())

    # Checked
    project = db.relationship('Project', back_populates='phases')
    # Checked
    phase = db.relationship('Phase', back_populates='projects')

    user_service_items = db.relationship('UserServiceItem', backref='project_phase', lazy='dynamic')

    custom_service_items = db.relationship('CustomServiceItem', backref='project_phase', lazy='dynamic')

    user_attachments = db.relationship('UserAttachment', backref='project_phase', lazy='dynamic')


class ProjectPhaseSchema(Schema):
    phase_name = fields.String()

    class Meta:
        additional = ('id', 'project_id', 'project_name', 'phase_id', 'phase_name', 'days', 'status', 'gmt_create', 'gmt_modified')
        ordered = False


class PhaseAttachmentExtension(MapperExtension):
    def before_insert(self, mapper, connection, instance):
        instance.phase_name = Phase.query.get_or_404(instance.phase_id).name
        instance.attachment_name = Attachment.query.get_or_404(instance.attachment_id).name

    def before_update(self, mapper, connection, instance):
        instance.phase_name = instance.phase.name
        instance.attachment_name = instance.attachment.name

        instance.gmt_modified = datetime.now()


class PhaseAttachment(db.Model):
    __tablename__ = 'phases_attachments'
    __mapper_args__ = {'extension': PhaseAttachmentExtension()}

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    phase_id = db.Column(db.Integer, db.ForeignKey('phases.id'))
    phase_name = db.Column(db.String(20))
    attachment_id = db.Column(db.Integer, db.ForeignKey('attachments.id'))
    attachment_name = db.Column(db.String(20))
    status = db.Column(db.Enum(AttachmentStatus), default=AttachmentStatus.Submitting)
    gmt_create = db.Column(db.TIMESTAMP, nullable=False, default=db.func.now())
    gmt_modified = db.Column(db.TIMESTAMP, nullable=False, onupdate=db.func.now())

    # Checked
    phase = db.relationship('Phase', back_populates='attachments')
    # Checked
    attachment = db.relationship('Attachment', back_populates='phases')


class PhaseAttachmentSchema(Schema):
    status = fields.String()
    phase_name = fields.String()
    attachment_name = fields.String()
    project_name = fields.String()

    class Meta:
        additional = ('id', 'phase_id', 'attachment_id', 'gmt_create', 'gmt_modified')
        ordered = False


class UserAttachmentExtension(MapperExtension):
    def before_insert(self, mapper, connection, instance):
        pp = ProjectPhase.query.get_or_404(instance.ppid)
        instance.project_name = pp.project_name
        instance.phase_name = pp.phase_name
        instance.attachment_name = Attachment.query.get_or_404(instance.attachment_id).name

    def before_update(self, mapper, connection, instance):
        pp = instance.project_phase
        instance.project_name = pp.project_name
        instance.phase_name = pp.phase_name
        instance.attachment_name = instance.attachment.name

        instance.gmt_modified = datetime.now()


class UserAttachment(db.Model):
    __tablename__ = 'user_attachments'
    __mapper_args__ = {'extension': UserAttachmentExtension()}

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ppid = db.Column(db.Integer, db.ForeignKey('projects_phases.id'))
    project_name = db.Column(db.String(20))
    phase_name = db.Column(db.String(20))
    attachment_id = db.Column(db.Integer, db.ForeignKey('attachments.id'))
    attachment_name = db.Column(db.String(20))
    status = db.Column(db.Enum(ServiceStatus), default=ServiceStatus.Submitted)
    url = db.Column(db.String(50))
    comment = db.Column(db.String(100))
    gmt_create = db.Column(db.TIMESTAMP, nullable=False, default=db.func.now())
    gmt_modified = db.Column(db.TIMESTAMP, nullable=False, onupdate=db.func.now())

    details = db.relationship('PhaseAttachmentDetail', backref=db.backref('attachment'), lazy='dynamic')


class UserAttachmentSchema(Schema):
    project_name = fields.String()
    attachment_name = fields.String()
    infos = fields.Nested(PhaseAttachmentDetailSchema, many=True)

    class Meta:
        additional = ('id', 'ppid', 'project_name', 'phase_name', 'phase_name', 'attachment_id', 'attachment_name', 'url', 'comment', 'gmt_create', 'gmt_modified')


class ServiceItemCategoryExtension(MapperExtension):
    def before_insert(self, mapper, connection, instance):
        pass

    def before_update(self, mapper, connection, instance):
        instance.gmt_modified = datetime.now()


class ServiceItemCategory(db.Model):
    __tablename__ = 'service_categories'
    __mapper_args__ = {'extension': ServiceItemCategoryExtension()}

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(30))
    description = db.Column(db.String(100))
    gmt_create = db.Column(db.TIMESTAMP, nullable=False, default=db.func.now())
    gmt_modified = db.Column(db.TIMESTAMP, nullable=False, onupdate=db.func.now())
    # Checked
    items = db.relationship('ServiceItem', backref='category', lazy='dynamic')
    custom_service_items = db.relationship('CustomServiceItem', backref='category', lazy='dynamic')


class ServiceItemCategorySchema(Schema):
    class Meta:
        fields = ('id', 'name', 'description', 'gmt_create', 'gmt_modified')
        ordered = False


class ServiceItemExtension(MapperExtension):
    def before_insert(self, mapper, connection, instance):
        instance.category_name = ServiceItemCategory.query.get_or_404(instance.category_id).name

    def before_update(self, mapper, connection, instance):
        instance.category_name = instance.category.name

        instance.gmt_modified = datetime.now()


# 服务项
class ServiceItem(db.Model):
    __tablename__ = 'service_items'
    __mapper_args__ = {'extension': ServiceItemExtension()}

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    desc = db.Column(db.String(150))
    category_id = db.Column(db.Integer, db.ForeignKey(ServiceItemCategory.id))  #服务项类别
    category_name = db.Column(db.String(20))
    price = db.Column(db.Integer, nullable=False, default=0)
    gmt_create = db.Column(db.TIMESTAMP, nullable=False, default=db.func.now())
    gmt_modified = db.Column(db.TIMESTAMP, nullable=False, onupdate=db.func.now())

    user_service_items = db.relationship('UserServiceItem', backref='service_item', lazy='dynamic')


class ServiceItemSchema(Schema):
    status = fields.String()

    class Meta:
        additional = ('id', 'category_id', 'category_name', 'name', 'desc', 'price', 'gmt_create', 'gmt_modified')
        ordered = False


class UserServiceItemExtension(MapperExtension):
    def before_insert(self, mapper, connection, instance):
        pp = ProjectPhase.query.get_or_404(instance.ppid)
        instance.project_name = pp.project_name
        instance.phase_name = pp.phase_name

        si = ServiceItem.query.get_or_404(instance.service_id)
        instance.service_name = si.name
        instance.service_category_name = si.category_name

    def before_update(self, mapper, connection, instance):
        instance.project_name = instance.project_phase.project_name
        instance.phase_name = instance.project_phase.phase_name
        instance.service_name = instance.service_item.name
        instance.service_category_name = instance.service_item.category_name

        instance.gmt_modified = datetime.now()


class UserServiceItem(db.Model):
    __tablename__ = 'user_service_items'
    __mapper_args__ = {'extension': UserServiceItemExtension()}

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ppid = db.Column(db.Integer, db.ForeignKey('projects_phases.id'))
    project_name = db.Column(db.String(20))
    phase_name = db.Column(db.String(20))
    service_id = db.Column(db.Integer, db.ForeignKey('service_items.id'))
    service_name = db.Column(db.String(30))
    service_category_id = db.Column(db.Integer)
    service_category_name = db.Column(db.String(30))
    price = db.Column(db.Integer)  # 实际价格，可能与标准价格不同
    status = db.Column(db.Enum(ServiceStatus),  default=ServiceStatus.Submitting)
    gmt_create = db.Column(db.TIMESTAMP, nullable=False, default=db.func.now())
    gmt_modified = db.Column(db.TIMESTAMP, nullable=False, onupdate=db.func.now())


class UserServiceItemSchema(Schema):
    status = fields.String()

    class Meta:
        additional = ('id', 'ppid', 'project_name', 'phase_name', 'service_name', 'price', 'gmt_create', 'gmt_modified')
        ordered = False


class CustomServiceItemExtension(MapperExtension):
    def before_insert(self, mapper, connection, instance):
        pp = ProjectPhase.query.get_or_404(instance.ppid)
        instance.project_name = pp.project_name
        instance.phase_name = pp.phase_name
        instance.category_name = ServiceItemCategory.query.get_or_404(instance.category_id).name

    def before_update(self, mapper, connection, instance):
        instance.project_name = instance.project_phase.project_name
        instance.phase_name = instance.project_phase.phase_name
        instance.category_name = instance.category.name

        instance.gmt_modified = datetime.now()


class CustomServiceItem(db.Model):
    __tablename__ = 'custom_service_items'
    __mapper_args__ = {'extension': CustomServiceItemExtension()}

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ppid = db.Column(db.Integer, db.ForeignKey('projects_phases.id'))
    project_name = db.Column(db.String(30))
    phase_name = db.Column(db.String(30))
    category_id = db.Column(db.Integer, db.ForeignKey(ServiceItemCategory.id))  # 服务项类别
    category_name = db.Column(db.String(30))
    title = db.Column(db.String(20))
    description = db.Column(db.String(100))
    price = db.Column(db.Integer)  # 实际价格，可能与标准价格不同
    status = db.Column(db.Enum(ServiceStatus), default=ServiceStatus.Submitting)
    gmt_create = db.Column(db.TIMESTAMP, nullable=False, default=db.func.now())
    gmt_modified = db.Column(db.TIMESTAMP, nullable=False, onupdate=db.func.now())


class CustomServiceItemSchema(Schema):
    status = fields.String()

    class Meta:
        additional = ('id', 'ppid', 'project_name', 'phase_name', 'category_id', 'category_name', 'title', 'description', 'price', 'gmt_create', 'gmt_modified')
        ordered = False


class ScheduleExtension(MapperExtension):
    def before_insert(self, mapper, connection, instance):
        instance.user1_name = Startup.query.get_or_404(instance.user1_id).name
        instance.user2_name = Investor.query.get_or_404(instance.user2_id).name
        instance.project_name = Project.query.get_or_404(instance.project_id).name

    def before_update(self, mapper, connection, instance):
        instance.user1_name = instance.startup.name
        instance.user2_name = instance.investor.name
        instance.project_name = instance.project.name

        instance.gmt_modified = datetime.now()


# 约谈表
class Schedule(db.Model):
    __tablename__ = 'schedules'
    __mapper_args__ = {'extension': ScheduleExtension()}

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    time = db.Column(db.DateTime, nullable=False)
    user1_id = db.Column(db.Integer, db.ForeignKey(Startup.id))
    user1_name = db.Column(db.String(10))
    user2_id = db.Column(db.Integer, db.ForeignKey(Investor.id))
    user2_name = db.Column(db.String(10))
    from_to = db.Column(db.Integer)  # 0: investor->startup, 1: startup->investor
    project_id = db.Column(db.Integer, db.ForeignKey(Project.id))
    project_name = db.Column(db.String(50))
    gmt_create = db.Column(db.TIMESTAMP, nullable=False, default=db.func.now())
    gmt_modified = db.Column(db.TIMESTAMP, nullable=False, onupdate=db.func.now())


class ScheduleSchema(Schema):
    class Meta:
        fields = ('id', 'time', 'from_id', 'to_id', 'project_id', 'gmt_create', 'gmt_modified')
        ordered = False


class TicketExtension(MapperExtension):
    def before_insert(self, mapper, connection, instance):
        instance.author_name = Startup.query.get_or_404(instance.author_id).name

    def before_update(self, mapper, connection, instance):
        # instance.author_name = instance.owner.name

        instance.gmt_modified = datetime.now()


# 工单表(求助表)
class Ticket(db.Model):
    __tablename__ = 'tickets'
    __mapper_args__ = {'extension': TicketExtension()}

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    author_id = db.Column(db.Integer, db.ForeignKey(Startup.id))
    author_name = db.Column(db.String(10))
    title = db.Column(db.String(50))
    content = db.Column(db.String(1000))
    url = db.Column(db.String(50))
    contact_name = db.Column(db.String(10))
    contact_phone = db.Column(db.String(20))
    gmt_create = db.Column(db.TIMESTAMP, nullable=False, default=db.func.now())
    gmt_modified = db.Column(db.TIMESTAMP, nullable=False, onupdate=db.func.now())


class TicketSchema(Schema):
    class Meta:
        fields = ('id', 'author_id', 'title', 'content', 'contact_name', 'contact_phone', 'gmt_create', 'gmt_modified')
        ordered = False


class FileExtension(MapperExtension):
    def before_insert(self, mapper, connection, instance):
        instance.owner_name = Startup.query.get_or_404(instance.owner_id).name

    def before_update(self, mapper, connection, instance):
        # instance.owner_name = instance.owner.name

        instance.gmt_modified = datetime.now()


# 上传的文件表
class File(db.Model):
    __tablename__ = 'files'
    __mapper_args__ = {'extension': FileExtension()}

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    owner_id = db.Column(db.Integer, db.ForeignKey(Startup.id))
    owner_name = db.Column(db.String(10))
    local_name = db.Column(db.String(100))  # 用户上传的文件的原始名字
    server_name = db.Column(db.String(50))  # 用UUID命名
    gmt_create = db.Column(db.TIMESTAMP, nullable=False, default=db.func.now())
    gmt_modified = db.Column(db.TIMESTAMP, nullable=False, onupdate=db.func.now())


class CommentExtension(MapperExtension):
    def before_insert(self, mapper, connection, instance):
        instance.project_name = Project.query.get_or_404(instance.project_id).name
        instance.author_name = Investor.query.get_or_404(instance.author_id).name

    def before_update(self, mapper, connection, instance):
        instance.gmt_modified = datetime.now()


# 项目评论表
class Comment(db.Model):
    __tablename__ = 'comments'
    __mapper_args__ = {'extension': CommentExtension()}

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    project_id = db.Column(db.Integer, db.ForeignKey(Project.id))
    project_name = db.Column(db.String(50))
    author_id = db.Column(db.Integer, db.ForeignKey(Investor.id))
    author_name = db.Column(db.String(10))
    content = db.Column(db.String(500))
    gmt_create = db.Column(db.TIMESTAMP, nullable=False, default=db.func.now())
    gmt_modified = db.Column(db.TIMESTAMP, nullable=False, onupdate=db.func.now())


class CommentSchema(Schema):
    class Meta:
        # additional = ('id', 'project_name', 'author_name', 'content', 'gmt_create', 'gmt_modified')
        additional = ('id', 'content', 'gmt_create', 'gmt_modified')
        ordered = False


class DepartmentExtension(MapperExtension):
    def before_insert(self, mapper, connection, instance):
        pass

    def before_update(self, mapper, connection, instance):
        instance.gmt_modified = datetime.now()


# 部门表
class Department(db.Model):
    __tablename__ = 'departments'
    __mapper_args__ = {'extension': DepartmentExtension()}

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(20))
    description = db.Column(db.String(30))
    status = db.Column(db.Boolean(True))
    gmt_create = db.Column(db.TIMESTAMP, nullable=False, default=db.func.now())
    gmt_modified = db.Column(db.TIMESTAMP, nullable=False, onupdate=db.func.now())
    # Checked
    admins = db.relationship('Admin', backref='department', lazy='dynamic')


class DepartmentSchema(Schema):
    class Meta:
        fields = ('id', 'name', 'description', 'status', 'gmt_create', 'gmt_modified')
        ordered = False


class RoleExtension(MapperExtension):
    def before_insert(self, mapper, connection, instance):
        pass

    def before_update(self, mapper, connection, instance):
        instance.gmt_modified = datetime.now()


# 角色表
class Role(db.Model):
    __tablename__ = 'roles'
    __mapper_args__ = {'extension': RoleExtension()}

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(20))
    description = db.Column(db.String(100))
    status = db.Column(db.Boolean(True))
    gmt_create = db.Column(db.TIMESTAMP, nullable=False, default=db.func.now())
    gmt_modified = db.Column(db.TIMESTAMP, nullable=False, onupdate=db.func.now())
    # Checked
    permissions = db.relationship('RolePermission', back_populates='role')
    # Checked
    admins = db.relationship('Admin', backref='role', lazy='dynamic')


class RoleSchema(Schema):
    permissions = fields.String()

    class Meta:
        additional = ('id', 'name', 'description', 'status', 'gmt_create', 'gmt_modified')

        ordered = False


class AdminExtension(MapperExtension):
    def before_insert(self, mapper, connection, instance):
        instance.dept_name = Department.query.get_or_404(instance.dept_id).name
        instance.role_name = Role.query.get_or_404(instance.role_id).name

    def before_update(self, mapper, connection, instance):
        instance.dept_name = instance.department.name
        instance.role_name = instance.role.name

        instance.gmt_modified = datetime.now()


# 管理员表
class Admin(db.Model):
    __tablename__ = 'admins'
    __mapper_args__ = {'extension': AdminExtension()}

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(10))
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(32))
    permissions = db.Column(db.BigInteger, nullable=False, default=0)
    dept_id = db.Column(db.Integer, db.ForeignKey('departments.id'))
    dept_name = db.Column(db.String(10))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    role_name = db.Column(db.String(10))
    status = db.Column(db.Boolean(True))
    gmt_create = db.Column(db.TIMESTAMP, nullable=False, default=db.func.now())
    gmt_modified = db.Column(db.TIMESTAMP, nullable=False, onupdate=db.func.now())

    bps = db.relationship('BusinessPlan', backref='owner', lazy='dynamic')

    def get_id(self):
        return self.id

    def get_permissions(self):
        return self.permissions

    def verify_password(self, password):
        return self.password == password


class AdminSchema(Schema):
    class Meta:
        additional = ('id', 'name', 'email', 'permissions', 'dept_name', 'role_name', 'status', 'gmt_create', 'gmt_modified')

        ordered = False


class PermissionExtension(MapperExtension):
    def before_insert(self, mapper, connection, instance):
        pass

    def before_update(self, mapper, connection, instance):
        instance.gmt_modified = datetime.now()


# 权限表，每个角色可以有多条记录，所以才有role_id这一列
class Permission(db.Model):
    __tablename__ = 'permissions'
    __mapper_args__ = {'extension': PermissionExtension()}

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(20))
    description = db.Column(db.String(100))
    value = db.Column(db.Integer, unique=True, nullable=False, default=0)
    status = db.Column(db.Boolean(True))
    gmt_create = db.Column(db.TIMESTAMP, nullable=False, default=db.func.now())
    gmt_modified = db.Column(db.TIMESTAMP, nullable=False, onupdate=db.func.now())

    # Checked
    roles = db.relationship('RolePermission', back_populates='permission')


class PermissionSchema(Schema):
    class Meta:
        fields = ('id', 'name', 'description', 'value', 'status', 'gmt_create', 'gmt_modified')

        ordered = False


class RolePermissionExtension(MapperExtension):
    def before_insert(self, mapper, connection, instance):
        pass

    def before_update(self, mapper, connection, instance):
        instance.gmt_modified = datetime.now()


class RolePermission(db.Model):
    __tablename__ = 'roles_permissions'
    __mapper_args__ = {'extension': RolePermissionExtension()}

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    p_id = db.Column(db.Integer, db.ForeignKey('permissions.id'))
    permission = db.relationship('Permission', back_populates='roles')
    role = db.relationship('Role', back_populates='permissions')
    gmt_create = db.Column(db.TIMESTAMP, nullable=False, default=db.func.now())
    gmt_modified = db.Column(db.TIMESTAMP, nullable=False, onupdate=db.func.now())


class RolePermissionSchema(Schema):
    class Meta:
        fields = ('id', 'p_id', 'role_id', 'gmt_create', 'gmt_modified')


class BusinessPlanExtension(MapperExtension):
    def before_insert(self, mapper, connection, instance):
        instance.owner_name = Admin.query.get_or_404(instance.owner_id).name

    def before_update(self, mapper, connection, instance):
        instance.owner_name = instance.owner.name
        instance.gmt_modified = datetime.now()


class BusinessPlan(db.Model):
    __tablename__ = 'bps'
    __mapper_args__ = {'extension': BusinessPlanExtension()}

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    owner_id = db.Column(db.Integer, db.ForeignKey(Admin.id))
    owner_name = db.Column(db.String(10))
    project_name = db.Column(db.String(50))
    company_name = db.Column(db.String(50))
    financing_sum = db.Column(db.Integer)       # 预期融资额
    valuation = db.Column(db.Integer)           # 估值
    description = db.Column(db.String(100))     # 一句话介绍
    contact = db.Column(db.String(10))          # 联系人
    contact_title = db.Column(db.String(10))    # 联系人职位
    contact_phone = db.Column(db.String(15))    # 联系方式
    employees = db.Column(db.Integer)           # 员工人数
    start_from = db.Column(db.String(20))       # 成立时间
    city = db.Column(db.String(20))             # 所属城市
    investors = db.Column(db.String(50))        # 关联投资者
    organization = db.Column(db.String(50))     # 关联机构
    source = db.Column(db.String(20))           # 项目来源
    industry = db.Column(db.Enum(Industry), default=Industry.Others)
    tags = db.Column(db.String(30))             # 关键词
    # docs = db.Column(db.String(50))             # 项目调研资料
    # talker = db.Column(db.String(10))           # 约谈人
    comment = db.Column(db.String(200))         # 备注

    # 团队分析
    full_time = db.Column(db.String(50))        # 全职、兼职情况
    ceo = db.Column(db.String(10))              # CEO
    cto = db.Column(db.String(10))              # CTO
    cmo = db.Column(db.String(10))              # CMO
    industry_resource = db.Column(db.String(100))   # 行业资源
    stock_structure = db.Column(db.String(50))      # 股权结构
    team_desc = db.Column(db.String(100))           # 团队描述

    # 市场分析
    market_rate = db.Column(db.String(20))          # 市场占有率
    market_capacity = db.Column(db.String(20))      # 市场容量
    market_proficiency = db.Column(db.String(50))   # 市场增量
    rival = db.Column(db.String(300))               # 竞争对手分析
    pain_point = db.Column(db.String(100))          # 痛点及需求描述
    our_resource = db.Column(db.String(100))        # 我们的资源匹配情况

    # 投资亮点/关键技术
    product_status = db.Column(db.String(100))      # 产品形态
    business_mode = db.Column(db.String(100))       # 商业模式
    main_income = db.Column(db.String(100))         # 主要营收来源
    income_status = db.Column(db.String(100))       # 营收情况
    dest_customers = db.Column(db.String(50))       # 目标客户
    customers_resource = db.Column(db.String(50))   # 获取用户方式
    core_tech = db.Column(db.String(100))           # 核心技术
    tech_evaluation = db.Column(db.String(100))     # 技术评估
    core_resource = db.Column(db.String(50))        # 核心资源
    recent_plan = db.Column(db.String(100))         # 近期业务规划
    future_plan = db.Column(db.String(100))         # 中期业务规划
    future_aim = db.Column(db.String(100))          # 未来定位

    # 融资、需求方案
    needs_desc = db.Column(db.String(100))          # 需求描述
    needs_support = db.Column(db.String(100))       # 需求依据
    financing_plan = db.Column(db.String(100))      # 融资计划
    potential_income = db.Column(db.String(20))     # 财务预期营收
    risk = db.Column(db.String(50))                 # 风险及应对策略
    risk_detail = db.Column(db.String(100))         # 风险分析

    # 项目打分
    score_needs = db.Column(db.Integer)             # 需求
    score_industry = db.Column(db.Integer)          # 行业
    score_product = db.Column(db.Integer)           # 产品
    score_team = db.Column(db.Integer)              # 团队
    score_resource = db.Column(db.Integer)          # 资源
    score_mode = db.Column(db.Integer)              # 商业模式
    score_evaluation = db.Column(db.Integer)        # 估值
    score_risk = db.Column(db.Integer)              # 风险
    bp_url = db.Column(db.String(50))               # BP的文件链接

    gmt_create = db.Column(db.TIMESTAMP, nullable=False, default=db.func.now())
    gmt_modified = db.Column(db.TIMESTAMP, nullable=False, onupdate=db.func.now())


class BusinessPlanSchema(Schema):
    industry = fields.String()

    class Meta:
        additional = ('id', 'project_name', 'company_name', 'financing_sum', 'valuation', 'description', 'contact', 'contact_title', 'contact_phone', 'employees', 'start_from', 'city', 'investors', 'organization', 'source', 'tags', 'comment',
                      'full_time', 'ceo', 'cto', 'cmo', 'industry_resource', 'stock_structure', 'team_desc',
                      'market_rate', 'market_capacity', 'market_proficiency', 'rival', 'pain_point', 'our_resource',
                      'product_status', 'business_mode', 'main_income', 'income_status', 'dest_customers', 'customers_resource', 'core_tech', 'tech_evaluation', 'core_resource', 'recent_plan', 'future_plan', 'future_aim',
                      'needs_desc', 'needs_support', 'financing_plan', 'potential_income', 'risk', 'risk_detail',
                      'score_needs', 'score_industry', 'score_product', 'score_team', 'score_resource', 'score_mode', 'score_evaluation', 'score_risk', 'bp_url', 'gmt_create', 'gmt_modified')

        ordered = False


class PaginationSchema(Schema):
    # query = fields.String()

    class Meta:
        additional = ('page', 'prev_num', 'next_num', 'has_next', 'has_prev', 'pages', 'per_page', 'total')

# 操作记录表(待定)
