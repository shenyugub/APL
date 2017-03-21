from . import db
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, SignatureExpired, BadSignature
from flask import current_app
from flask_loginmanager import UserMixin
from enum import unique, Enum
from marshmallow import fields, Schema
from app.utils.utils import safe_session
from datetime import datetime


# 用户类型
class UserType(Enum):
    Startup = '创业者'
    Investor = '投资人'


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


# 融资方式
class FinancingMode(Enum):
    Obligation = '债权融资'
    Stock = '股权融资'
    

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
@unique
class Permissions(Enum):
    ResetPassword = 1 << 0
    CreateUser = 1 << 1
    CreateAdmin = 1 << 2
    AuditProject = 1 << 3


favorite_investors_table = db.Table(
    'favorite_investors',
    db.Column('id', db.Integer, primary_key=True, autoincrement=True),
    db.Column('startup_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('investor_id', db.Integer, db.ForeignKey('users.id'), primary_key=True)
)


favorite_projects_table = db.Table(
    'favorite_projects',
    db.Column('id', db.Integer, primary_key=True, autoincrement=True),
    db.Column('investor_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('project_id', db.Integer, db.ForeignKey('projects.id'), primary_key=True)
    )


# 用户表
class User(db.Model, UserMixin):
    __tablename__ = 'users'

    #系统信息
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    password = db.Column(db.String(32))
    permissions = db.Column(db.Integer)
    type = db.Column(db.Enum(UserType), default=UserType.Investor)
    confirmed = db.Column(db.Boolean, default=True)                     # 初期应该用不到，因为没有开放注册，不需要邮件或短信确认
    initialized = db.Column(db.Boolean, default=False)                  # 第一次登录时需要填写个人资料、修改密码等
    active = db.Column(db.Boolean, default=True)                       # 被禁用的账户不能登陆、提示账户已被禁用
    register_time = db.Column(db.TIMESTAMP, server_default=db.func.now())     # 注册时间
    last_login_time = db.Column(db.TIMESTAMP, server_default=db.func.now())   # 最后登录时间

    #基本信息，投资人和创业者都有
    name = db.Column(db.String(10), default='')
    email = db.Column(db.String(50), unique=True)
    phone = db.Column(db.String(20), default='')
    wechat = db.Column(db.String(20), default='')                       # 微信号
    company = db.Column(db.String(40), default='')                      # 公司及职位
    gender = db.Column(db.Enum(Gender), default=Gender.Male)
    avatar = db.Column(db.String(200), default='')                      #头像 URL
    resume = db.Column(db.String(500), default='')                      #个人简介

    #创业者信息
    company_name = db.Column(db.String(30), default='')                 # 企业名称
    company_desc = db.Column(db.String(400), default='')                # 企业简介
    company_industry = db.Column(db.Enum(Industry), default=Industry.Others)                     # 所属行业

    #投资人信息
    interested = db.Column(db.String(200), default='')                  # 关注的领域
    invest_role = db.Column(db.Enum(InvestmentType), default=InvestmentType.Individual)                  # 投资身份，个人还是机构
    investment_min = db.Column(db.Integer, default=0)                   # 投资额最小值
    investment_max = db.Column(db.Integer, default=0)                   # 投资额最大值
    invest_phase = db.Column(db.String(200), default='')                # 投资阶段

    projects = db.relationship('Project', backref='owner', lazy='dynamic')
    comments = db.relationship('Comment', backref='author', lazy='dynamic')
    files = db.relationship('File', backref='owner', lazy='dynamic')

    #投资人关注的项目
    favorite_projects = db.relationship('Project', secondary=favorite_projects_table, backref=db.backref('followers', lazy='dynamic'), lazy='dynamic')

    #创业者关注的投资人
    favorite_investors = db.relationship('User', secondary=favorite_investors_table, primaryjoin=id == favorite_investors_table.c.startup_id, secondaryjoin=id == favorite_investors_table.c.investor_id)

    bps = db.relationship('BusinessPlan', backref='owner', lazy='dynamic')
    tickets = db.relationship('Ticket', backref='owner', lazy='dynamic')

    #对应上面的 permissions，也就是 falsk-loginmanager 中 login_required 的参数
    Startup = 1 << 1
    Investor = 1 << 2

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
            return User.query.filter_by(email=data['email']).first()
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

    # 创业者关注投资人
    def follow_investor(self, user):
        if not self.is_following_investor(user):
            self.favorite_investors.append(user)

            with safe_session(db):
                db.session.add(self)

    def unfollow_investor(self, user):

        self.favorite_investors.remove(user)

        with safe_session(db):
            db.session.add(self)

    def is_following_investor(self, user):

        return user in self.favorite_investors

    # 投资人关注项目
    def follow_project(self, project):
        if not self.is_following_project(project):
            self.favorite_projects.append(project)
            with safe_session(db):
                db.session.add(self)

    def unfollow_project(self, project):
        self.favorite_projects.remove(project)

        with safe_session(db):
            db.session.add(self)

    def is_following_project(self, project):
        return project in self.favorite_projects.all()


class StartupSchema(Schema):
    type = fields.String()
    gender = fields.String()
    company_industry = fields.String()

    class Meta:
        additional = ('id', 'permissions', 'confirmed', 'initialized', 'active', 'register_time', 'last_login_time',
                      'name', 'email', 'phone', 'wechat', 'company', 'avatar', 'resume',
                      'company_name', 'company_desc')

        ordered = True


class InvestorSchema(Schema):
    type = fields.String()
    gender = fields.String()
    invest_role = fields.String()

    class Meta:
        additional = ('id', 'permissions', 'confirmed', 'initialized', 'active', 'register_time', 'last_login_time',
                      'name', 'email', 'phone', 'wechat', 'company', 'avatar', 'resume',
                      'interested', 'investment_min', 'investment_max', 'invest_phase')

        ordered = True


# 项目表
class Project(db.Model):
    __tablename__ = 'projects'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    owner_id = db.Column(db.Integer, db.ForeignKey(User.id))
    icon_url = db.Column(db.String(200), default='')
    name = db.Column(db.String(50), nullable=False)     # 项目名称
    description = db.Column(db.String(500))             # 项目介绍
    advantage = db.Column(db.String(100))               # 项目优势
    industry = db.Column(db.Enum(Industry), default=Industry.Others)             # 所属行业
    company_phase = db.Column(db.Enum(CompanyPhase), default=CompanyPhase.Initial)    # 创业阶段
    financing_sum = db.Column(db.Integer)               # 融资目标
    #项目阶段放到单独的表里
    bp_url = db.Column(db.String(200))                  # 商业计划书
    phase_index = db.Column(db.Integer)  #当前所处阶段索引
    duration = db.Column(db.Integer)  #当前阶段预计开发时间
    phase_start = db.Column(db.DateTime, default=datetime.now())  #当前阶段开始日期
    financing_mode = db.Column(db.Enum(FinancingMode), default=FinancingMode.Stock)
    financing_status = db.Column(db.String(100))
    deadline = db.Column(db.DateTime, default=datetime.now())
    contact_name = db.Column(db.String(10))
    contact_phone = db.Column(db.String(20))
    contact_email = db.Column(db.String(40))
    status = db.Column(db.Enum(ProjectStatus), default=ProjectStatus.Submitting)
    create_at = db.Column(db.TIMESTAMP, server_default=db.func.now())

    # Checked
    comments = db.relationship('Comment', backref='project', lazy='dynamic')
    # Checked
    phases = db.relationship('ProjectPhase', back_populates='project')
    # Checked
    schedules = db.relationship('Schedule', backref='project', lazy='dynamic')


class ProjectSchema(Schema):
    industry = fields.String()
    company_phase = fields.String()
    financing_mode = fields.String()
    status = fields.String()
    comments = fields.Nested('CommentSchema', many=True)
    phases = fields.Nested('ProjectPhaseSchema', many=True)

    class Meta:
        additional = ('id', 'owner_id', 'icon_url', 'name', 'description', 'advantage', 'financing_sum',
                      'bp_url', 'phase_index', 'duration', 'financing_status', 'deadline', 'contact_name',
                      'contact_phone', 'contact_email', 'create_at')


# 项目阶段表
class Phase(db.Model):
    __tablename__ = 'phases'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(20))
    description = db.Column(db.String(200))

    # Checked
    projects = db.relationship('ProjectPhase', back_populates='phase')
    # Checked
    attachments = db.relationship('PhaseAttachment', back_populates='phase')


class PhaseSchema(Schema):
    atts = fields.Nested('AttachmentSchema', many=True)

    class Meta:
        additional = ('id', 'name', 'description')
        ordered = False


# 系统的交付物表
class Attachment(db.Model):
    __tablename__ = 'attachments'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(20))
    description = db.Column(db.String(50))

    # Checked
    phases = db.relationship('PhaseAttachment', back_populates='attachment')
    user_attachments = db.relationship('UserAttachment', backref='attachment', lazy='dynamic')


class AttachmentSchema(Schema):
    details = fields.Nested('PhaseAttachmentDetailSchema', many=True)

    class Meta:
        additional = ('id', 'name', 'description')
        ordered = False


class PhaseAttachmentDetail(db.Model):
    __tablename__ = 'phase_attachment_details'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    uaid = db.Column(db.Integer, db.ForeignKey('user_attachments.id'))
    url = db.Column(db.String(50))
    comment = db.Column(db.String(200))
    timestamp = db.Column(db.TIMESTAMP, server_default=db.func.now())


class PhaseAttachmentDetailSchema(Schema):
    class Meta:
        fields = ('id', 'uaid', 'url', 'comment', 'timestamp')
        ordered = False


class ProjectPhase(db.Model):
    __tablename__ = 'projects_phases'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'))
    phase_id = db.Column(db.Integer, db.ForeignKey('phases.id'))
    days = db.Column(db.Integer)
    status = db.Column(db.Integer)

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
        additional = ('id', 'project_id', 'phase_id', 'days', 'status')
        ordered = False


class PhaseAttachment(db.Model):
    __tablename__ = 'phases_attachments'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    phase_id = db.Column(db.Integer, db.ForeignKey('phases.id'))
    attachment_id = db.Column(db.Integer, db.ForeignKey('attachments.id'))
    status = db.Column(db.Enum(AttachmentStatus), default=AttachmentStatus.Submitting)
    timestamp = db.Column(db.TIMESTAMP, server_default=db.func.now())

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
        additional = ('id', 'phase_id', 'attachment_id', 'timestamp')
        ordered = False


class UserAttachment(db.Model):
    __tablename__ = 'user_attachments'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ppid = db.Column(db.Integer, db.ForeignKey('projects_phases.id'))
    attachment_id = db.Column(db.Integer, db.ForeignKey('attachments.id'))
    status = db.Column(db.Enum(ServiceStatus), default=ServiceStatus.Submitted)
    url = db.Column(db.String(50))
    comment = db.Column(db.String(100))

    details = db.relationship('PhaseAttachmentDetail', backref=db.backref('attachment'), lazy='dynamic')


class UserAttachmentSchema(Schema):
    project_name = fields.String()
    attachment_name = fields.String()
    infos = fields.Nested(PhaseAttachmentDetailSchema, many=True)

    class Meta:
        additional = ('id', 'ppid', 'attachment_id', 'url', 'comment')


class ServiceItemCategory(db.Model):
    __tablename__ = 'service_categories'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(30))
    description = db.Column(db.String(100))
    # Checked
    items = db.relationship('ServiceItem', backref='category', lazy='dynamic')
    custom_service_items = db.relationship('CustomServiceItem', backref='category', lazy='dynamic')


class ServiceItemCategorySchema(Schema):
    class Meta:
        fields = ('id', 'name', 'description')
        ordered = False


# 服务项
class ServiceItem(db.Model):
    __tablename__ = 'service_items'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    category_id = db.Column(db.Integer, db.ForeignKey(ServiceItemCategory.id))  #服务项类别
    name = db.Column(db.String(50), nullable=False)
    desc = db.Column(db.String(150))
    price = db.Column(db.Integer, nullable=False, default=0)

    user_service_items = db.relationship('UserServiceItem', backref='service_item', lazy='dynamic')


class ServiceItemSchema(Schema):
    status = fields.String()
    category_name = fields.String()

    class Meta:
        additional = ('id', 'category_id', 'name', 'desc', 'price')
        ordered = False


class UserServiceItem(db.Model):
    __tablename__ = 'user_service_items'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ppid = db.Column(db.Integer, db.ForeignKey('projects_phases.id'))
    service_id = db.Column(db.Integer, db.ForeignKey('service_items.id'))
    price = db.Column(db.Integer)  # 实际价格，可能与标准价格不同
    status = db.Column(db.Enum(ServiceStatus),  default=ServiceStatus.Submitting)
    timestamp = db.Column(db.TIMESTAMP, server_default=db.func.now())


class UserServiceItemSchema(Schema):
    status = fields.String()
    project_name = fields.String()
    service_name = fields.String()

    class Meta:
        additional = ('id', 'ppid', 'price', 'timestamp')
        ordered = False


class CustomServiceItem(db.Model):
    __tablename__ = 'custom_service_items'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ppid = db.Column(db.Integer, db.ForeignKey('projects_phases.id'))
    category_id = db.Column(db.Integer, db.ForeignKey(ServiceItemCategory.id))  # 服务项类别
    title = db.Column(db.String(20))
    description = db.Column(db.String(100))
    price = db.Column(db.Integer)  # 实际价格，可能与标准价格不同
    status = db.Column(db.Enum(ServiceStatus), default=ServiceStatus.Submitting)
    timestamp = db.Column(db.TIMESTAMP, server_default=db.func.now())


class CustomServiceItemSchema(Schema):
    status = fields.String()
    project_name = fields.String()
    category_name = fields.String()

    class Meta:
        additional = ('id', 'ppid', 'category_id', 'title', 'description', 'price', 'timestamp')
        ordered = False


# 约谈表
class Schedule(db.Model):
    __tablename__ = 'schedules'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    time = db.Column(db.DateTime, nullable=False)
    from_id = db.Column(db.Integer, db.ForeignKey(User.id))
    to_id = db.Column(db.Integer, db.ForeignKey(User.id))
    project_id = db.Column(db.Integer, db.ForeignKey(Project.id))


class ScheduleSchema(Schema):
    class Meta:
        fields = ('id', 'time', 'from_id', 'to_id', 'project_id')
        ordered = False


# 工单表(求助表)
class Ticket(db.Model):
    __tablename__ = 'tickets'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    author_id = db.Column(db.Integer, db.ForeignKey(User.id))
    title = db.Column(db.String(50))
    content = db.Column(db.String(1000))
    url = db.Column(db.String(50))
    contact_name = db.Column(db.String(10))
    contact_phone = db.Column(db.String(20))
    timestamp = db.Column(db.TIMESTAMP)


class TicketSchema(Schema):
    class Meta:
        fields = ('id', 'author_id', 'title', 'content', 'contact_name', 'contact_phone', 'timestamp')
        ordered = False


# 上传的文件表
class File(db.Model):
    __tablename__ = 'files'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    owner_id = db.Column(db.Integer, db.ForeignKey(User.id))
    local_name = db.Column(db.String(100))  # 用户上传的文件的原始名字
    server_name = db.Column(db.String(50))  # 用UUID命名
    timestamp = db.Column(db.TIMESTAMP, server_default=db.func.now())


# 项目评论表
class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    project_id = db.Column(db.Integer, db.ForeignKey(Project.id))
    author_id = db.Column(db.Integer, db.ForeignKey(User.id))
    content = db.Column(db.String(500))
    timestamp = db.Column(db.TIMESTAMP, server_default=db.func.now())


class CommentSchema(Schema):
    project_name = fields.String()
    author_name = fields.String()

    class Meta:
        additional = ('id', 'content', 'timestamp')
        ordered = False


# 部门表
class Department(db.Model):
    __tablename__ = 'departments'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(20))
    description = db.Column(db.String(30))
    status = db.Column(db.Boolean(True))
    # Checked
    admins = db.relationship('Admin', backref='department', lazy='dynamic')


class DepartmentSchema(Schema):
    class Meta:
        fields = ('id', 'name', 'description', 'status')
        ordered = False


# 角色表
class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(20))
    description = db.Column(db.String(100))
    status = db.Column(db.Boolean(True))
    # Checked
    permissions = db.relationship('RolePermission', back_populates='role')
    # Checked
    admins = db.relationship('Admin', backref='role', lazy='dynamic')


class RoleSchema(Schema):
    permissions = fields.String()

    class Meta:
        additional = ('id', 'name', 'description', 'status')

        ordered = False


# 管理员表
class Admin(db.Model):
    __tablename__ = 'admins'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(10))
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(32))
    permissions = db.Column(db.BigInteger, nullable=False, default=0)
    dept_id = db.Column(db.Integer, db.ForeignKey('departments.id'))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    latest = db.Column(db.TIMESTAMP, server_default=db.func.now())
    status = db.Column(db.Boolean(True))

    def get_id(self):
        return self.id

    def get_permissions(self):
        return self.permissions

    def verify_password(self, password):
        return self.password == password


class AdminSchema(Schema):
    dept_name = fields.String()
    role_name = fields.String()

    class Meta:
        additional = ('id', 'name', 'email', 'latest', 'status')

        ordered = False


# 权限表，每个角色可以有多条记录，所以才有role_id这一列
class Permission(db.Model):
    __tablename__ = 'permissions'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(20))
    description = db.Column(db.String(100))
    value = db.Column(db.Integer, unique=True, nullable=False, default=0)
    status = db.Column(db.Boolean(True))
    # Checked
    roles = db.relationship('RolePermission', back_populates='permission')


class PermissionSchema(Schema):
    class Meta:
        fields = ('id', 'name', 'description', 'value', 'status')

        ordered = False


class RolePermission(db.Model):
    __tablename__ = 'roles_permissions'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    p_id = db.Column(db.Integer, db.ForeignKey('permissions.id'))
    permission = db.relationship('Permission', back_populates='roles')
    role = db.relationship('Role', back_populates='permissions')


class RolePermissionSchema(Schema):
    class Meta:
        fields = ('id', 'p_id', 'role_id')


class Const(object):
    MESSAGE_KEY = 'message'
    STATUS_ERROR = 400
    STATUS_DENIED = 401
    STATUS_OK = 200


class BusinessPlan(db.Model):
    __tablename__ = 'bps'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    owner_id = db.Column(db.Integer, db.ForeignKey(User.id))
    timestamp = db.Column(db.TIMESTAMP, server_default=db.func.now())
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
    bp_url = db.Column(db.String(40))               # BP的文件链接


class BusinessPlanSchema(Schema):
    industry = fields.String()

    class Meta:
        additional = ('id', 'project_name', 'company_name', 'financing_sum', 'valuation', 'description', 'contact', 'contact_title', 'contact_phone', 'employees', 'start_from', 'city', 'investors', 'organization', 'source', 'tags', 'comment',
                      'full_time', 'ceo', 'cto', 'cmo', 'industry_resource', 'stock_structure', 'team_desc',
                      'market_rate', 'market_capacity', 'market_proficiency', 'rival', 'pain_point', 'our_resource',
                      'product_status', 'business_mode', 'main_income', 'income_status', 'dest_customers', 'customers_resource', 'core_tech', 'tech_evaluation', 'core_resource', 'recent_plan', 'future_plan', 'future_aim',
                      'needs_desc', 'needs_support', 'financing_plan', 'potential_income', 'risk', 'risk_detail',
                      'score_needs', 'score_industry', 'score_product', 'score_team', 'score_resource', 'score_mode', 'score_evaluation', 'score_risk', 'bp_url')

        ordered = False

# 操作记录表(待定)
