from flask import Blueprint, render_template, request, current_app, redirect, url_for
from app import user_manager, db
from app.startup.forms import ProfileForm, ProjectForm, ServiceCustom
from app.models import User, Gender, Project, Industry, FinancingMode, CompanyPhase, UserType, File, ServiceItem, Phase, ProjectPhase, PhaseAttachment, Attachment, UserServiceItem
import base64
import time
import json
from app.utils.sts import request_sts_token, get_file_url
from app.utils.utils import get_iso_8601, get_sign_policy, safe_session
import datetime


startup = Blueprint('startup', __name__)


@startup.route('/profile/', methods=['GET', 'POST'])
@user_manager.login_required(User.Startup)
def show_profile():
    form = ProfileForm()

    user = user_manager.current_user

    if form.validate_on_submit():
        # user.email = form.email.data  # 不允许修改邮箱
        user.name = form.name.data
        user.phone = form.phone.data
        user.wechat = form.wechat.data
        user.company = form.company.data
        user.gender = form.gender.data
        user.avatar = form.avatar.data
        user.resume = form.resume.data

        user.company_name = form.company_name.data
        user.company_desc = form.company_desc.data
        user.company_industry = form.company_industry.data

        with safe_session(db):
            db.session.add(user)

    form.email.data = user.email
    form.name.data = user.name
    form.phone.data = user.phone
    form.wechat.data = user.wechat
    form.company.data = user.company
    form.gender.data = user.gender
    form.avatar.data = user.avatar
    form.resume.data = user.resume

    form.company_name.data = user.company_name
    form.company_desc.data = user.company_desc
    form.company_industry.data = user.company_industry.name

    gender = [[name, member.value, 'unchecked'] for name, member in Gender.__members__.items()]

    for i in gender:
        if i[0] == user.gender.name:
            i[2] = 'checked'
            break

    # 处理文件上传相关逻辑
    now = int(time.time())
    expire_syncpoint = now + 1800
    expire = get_iso_8601(expire_syncpoint)

    policy_dict = {}
    policy_dict["expiration"] = expire
    condition_array = []
    array_item = []
    array_item.append("content-length-range")
    array_item.append(0)
    array_item.append(104857600)
    condition_array.append(array_item)

    policy_dict["conditions"] = condition_array

    policy = json.dumps(policy_dict).strip()
    policy_encode = base64.b64encode(bytes(policy, 'utf-8'))

    sts = request_sts_token('rain')

    signature = get_sign_policy(sts.access_key_secret, policy_encode)

    callback_dict = {}
    callback_dict["callbackUrl"] = "https://apl.apluslabs.com/after_upload"
    callback_dict["callbackBody"] = "bucket=${bucket}&object=${object}&etag=${etag}&size=${size}&mimeType=${mimeType}&filename=${x:filename}&uid=${x:uid}"
    callback_dict["callbackBodyType"] = "application/x-www-form-urlencoded"
    callback_param = json.dumps(callback_dict).strip()
    base64_callback_body = base64.b64encode(bytes(callback_param, 'utf-8'))

    form.run_mode.data = current_app.config['DEBUG']
    form.oss_access_key_id.data = sts.access_key_id
    form.token.data = sts.security_token
    form.policy.data = policy_encode.decode()
    form.Signature.data = signature.decode()
    # form.key.data = str(uuid.uuid1()).replace('-', '')
    form.success_action_status.data = '201'
    form.callback.data = base64_callback_body.decode()
    form.uid.data = user_manager.current_user.get_id()
    form.origin_filename.data = ''

    return render_template('startup/profile.html', form=form, gender=gender)


@startup.route('/project_new/', methods=['GET', 'POST'])
@user_manager.login_required(User.Startup)
def project_new():

    form = ProjectForm()
    p = Project()

    pid = request.args.get('pid', -1)

    if pid != -1:
        temp = Project.query.filter_by(id=pid, owner_id=user_manager.current_user.get_id()).first()

        if temp:
            p = temp

    if form.validate_on_submit():

        p.owner_id = user_manager.current_user.get_id()
        p.icon_url = form.logo_url.data
        p.name = form.name.data
        p.description = form.description.data
        p.advantage = form.advantage.data
        p.industry = form.industry.data
        p.company_phase = form.company_phase.data
        p.financing_sum = form.financing_sum.data
        p.bp_url = form.bp_url.data
        p.duration = form.duration.data
        p.financing_mode = form.financing_mode.data
        p.financing_status = form.financing_status.data
        p.deadline = form.deadline.data
        p.contact_name = form.contact_name.data
        p.contact_phone = form.contact_phone.data
        p.contact_email = form.contact_email.data

        # ProjectPhase.query.filter_by(project_id=p.id).delete()

        phase_id_list = form.project_phase.data

        if pid == -1:

            for ppid in phase_id_list:
                pp = ProjectPhase()
                pp.phase = Phase.query.get(int(ppid))
                p.phases.append(pp)

            sorted(phase_id_list)
            p.phase_index = phase_id_list[0]
            p.phase_start = datetime.datetime.now()

        with safe_session(db):
            db.session.add(p)

        return redirect(url_for('startup.show_project', pid=p.id))

    form.logo_url.data = p.icon_url
    form.name.data = p.name
    form.description.data = p.description
    form.advantage.data = p.advantage
    form.industry.data = Industry.IntelligentMake.name if not p.industry else p.industry.name
    form.company_phase.data = CompanyPhase.Initial.name if not p.company_phase else p.company_phase.name
    form.financing_sum.data = p.financing_sum
    form.bp_url.data = p.bp_url
    form.duration.data = p.duration
    form.financing_mode.data = FinancingMode.Stock if not p.financing_mode else p.financing_mode.name
    form.financing_status.data = p.financing_status
    form.deadline.data = p.deadline
    form.contact_name.data = p.contact_name
    form.contact_phone.data = p.contact_phone
    form.contact_email.data = p.contact_email

    # 处理项目阶段的显示
    phases = Phase.query.all()

    pps = ProjectPhase.query.filter_by(project_id=p.id).all()
    pp_checked = [pp.phase_id for pp in pps]

    # 处理文件上传相关逻辑
    now = int(time.time())
    expire_syncpoint = now + 1800
    expire = get_iso_8601(expire_syncpoint)

    policy_dict = {}
    policy_dict["expiration"] = expire
    condition_array = []
    array_item = []
    array_item.append("content-length-range")
    array_item.append(0)
    array_item.append(104857600)
    condition_array.append(array_item)

    policy_dict["conditions"] = condition_array

    policy = json.dumps(policy_dict).strip()
    policy_encode = base64.b64encode(bytes(policy, 'utf-8'))

    sts = request_sts_token('rain')

    signature = get_sign_policy(sts.access_key_secret, policy_encode)

    callback_dict = {}
    callback_dict["callbackUrl"] = "https://apl.apluslabs.com/after_upload"
    callback_dict["callbackBody"] = "bucket=${bucket}&object=${object}&etag=${etag}&size=${size}&mimeType=${mimeType}&filename=${x:filename}&uid=${x:uid}"
    callback_dict["callbackBodyType"] = "application/x-www-form-urlencoded"
    callback_param = json.dumps(callback_dict).strip()
    base64_callback_body = base64.b64encode(bytes(callback_param, 'utf-8'))

    form.run_mode.data = current_app.config['DEBUG']
    form.oss_access_key_id.data = sts.access_key_id
    form.token.data = sts.security_token
    form.policy.data = policy_encode.decode()
    form.Signature.data = signature.decode()
    # form.key.data = str(uuid.uuid1()).replace('-', '')
    form.success_action_status.data = '201'
    form.callback.data = base64_callback_body.decode()
    form.uid.data = user_manager.current_user.get_id()

    form.origin_filename.data = ''

    return render_template('startup/project_new.html', form=form, project=p, phases=phases, checked_phase=pp_checked)


@startup.route('/projects/', methods=['GET'])
@user_manager.login_required(User.Startup)
def project_list():

    projects = Project.query.filter_by(owner_id=user_manager.current_user.get_id()).all()

    for project in projects:
        if project.icon_url:
            icon_file = File.query.filter_by(server_name=project.icon_url).first()
            if icon_file:
                icon_url = get_file_url(icon_file.server_name, icon_file.server_name)
                project.icon_url = icon_url

    return render_template('startup/project_list.html', projects=projects)


@startup.route('/projects/', methods=['POST'])
@user_manager.login_required(User.Startup)
def new_project():
    return '新建项目页'


@startup.route('/projects/<int:pid>', methods=['GET'])
@user_manager.login_required(User.Startup)
def show_project(pid):

    project = Project.query.filter_by(id=pid, owner_id=user_manager.current_user.get_id()).first_or_404()

    if project.bp_url:
        bp_file = File.query.filter_by(server_name=project.bp_url).first()
        if bp_file:
            bp_url = get_file_url(bp_file.server_name, bp_file.local_name)
            if bp_url:
                project.bp_url = bp_url

    if project.icon_url:
        icon_file = File.query.filter_by(server_name=project.icon_url).first()
        if icon_file:
            icon_url = get_file_url(icon_file.server_name, icon_file.server_name)
            if icon_url:
                project.icon_url = icon_url

    before = project.phase_start
    present = datetime.datetime.now()

    days = (present - before).days

    pp = ProjectPhase.query.filter_by(project_id=project.id, phase_id=project.phase_index).first()

    if pp:
        project.ppid = pp.id
    else:
        project.ppid = 0

    pas = PhaseAttachment.query.filter_by(phase_id=project.phase_index).all()

    attachments = Attachment.query.filter(Attachment.id.in_([pa.attachment_id for pa in pas])).all()

    return render_template('startup/project_detail.html', project=project, days=days, attachments=attachments)


@startup.route('/projects/<int:pid>', methods=['POST'])
@user_manager.login_required(User.Startup)
def edit_project(pid):
    return '项目编辑页 %d' % pid


@startup.route('/schedules/')
@user_manager.login_required(User.Startup)
def show_schedules():
    return render_template('startup/schedule_list.html')


@startup.route('/settings/', methods=['GET'])
@user_manager.login_required(User.Startup)
def show_settings():
    return render_template('startup/settings.html')


@startup.route('/settings/', methods=['POST'])
@user_manager.login_required(User.Startup)
def edit_settings():
    return '更改个人设置'


@startup.route('/bills/', methods=['GET'])
@user_manager.login_required(User.Startup)
def bill_list():
    sum = 500000
    cost = 0
    items = UserServiceItem.query.filter().all()
    for item in items:
        cost += item.price

    return render_template('startup/bill_list.html', sum=sum, cost=cost)


@startup.route('/bills/<int:bid>', methods=['GET'])
@user_manager.login_required(User.Startup)
def show_bill(bid):
    return render_template('startup/bill_detail.html')


@startup.route('/services/', methods=['GET'])
@user_manager.login_required(User.Startup)
def service_list():
    return render_template('startup/service_list.html')


@startup.route('/services/<int:sid>', methods=['GET'])
@user_manager.login_required(User.Startup)
def show_service(sid):
    return render_template('startup/service_detail.html')


@startup.route('/service_custom/', methods=['GET', 'POST'])
@user_manager.login_required(User.Startup)
def service_custom():

    pid = request.args.get('pid', -1)

    project = Project.query.filter_by(id=pid, owner_id=user_manager.current_user.get_id()).first_or_404()

    form = ServiceCustom()

    service = ServiceItem()

    if form.validate_on_submit():

        title = form.title.data
        content = form.content.data
        category = form.category.data

        service.project_id = project.id
        service.name = title
        service.desc = content
        service.type = category

        with safe_session(db):
            db.session.add(service)

        return redirect(url_for('startup.show_project', pid=pid))

    form.title.data = service.name
    form.content.data = service.desc
    form.category.data = service.type

    return render_template('startup/service_custom.html', form=form, pid=pid)


@startup.route('/investors/', methods=['GET'])
@user_manager.login_required(User.Startup)
def investor_list():
    investors = User.query.filter_by(type=UserType.Investor).all()

    return render_template('startup/investor_list.html', investors=investors)


@startup.route('/investors/<int:iid>', methods=['GET'])
@user_manager.login_required(User.Startup)
def show_investor(iid):
    investor = User.query.filter_by(type=UserType.Investor, id=iid).first_or_404()

    return render_template('startup/investor_detail.html', investor=investor)


#关注或取消关注投资人
@startup.route('/follow/<int:uid>', methods=['GET'])
@user_manager.login_required(User.Startup)
def follow(uid):
    investor = User.query.filter_by(id=uid).first_or_404()
    if user_manager.current_user.is_following_investor(investor):
        user_manager.current_user.unfollow_investor(investor)
    else:
        user_manager.current_user.follow_investor(investor)

    return redirect(url_for('startup.show_investor', iid=investor.id))
