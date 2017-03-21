from flask import Blueprint, render_template, current_app, url_for, redirect
from app import user_manager, db
from app.investor.forms import ProfileForm, CommentForm
from app.main.forms import ResetPasswordForm
from app.models import User, Industry, InvestmentPhase, Gender, InvestmentType, Project, Comment, File
import time
import json
import base64
from app.utils.utils import get_iso_8601, get_sign_policy, safe_session
from app.utils.sts import request_sts_token, get_file_url


investor = Blueprint('investor', __name__)


@investor.route('/')
@user_manager.login_required(User.Investor)
def index():
    return render_template('investor/index.html')


@investor.route('/profile/', methods=['GET', 'POST'])
@user_manager.login_required(User.Investor)
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

        user.interested = ','.join(form.interested.data)
        user.invest_role = form.invest_role.data
        user.investment_min = form.investment_min.data
        user.investment_max = form.investment_max.data
        user.invest_phase = ','.join(form.invest_phase.data)

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

    form.investment_min.data = user.investment_min
    form.investment_max.data = user.investment_max

    industries = [[name, member.value, 'unchecked'] for name, member in Industry.__members__.items()]
    phases = [[name, member.value, 'unchecked'] for name, member in InvestmentPhase.__members__.items()]
    gender = [[name, member.value, 'unchecked'] for name, member in Gender.__members__.items()]
    investment_type = [[name, member.value, 'unchecked'] for name, member in InvestmentType.__members__.items()]

    for i in investment_type:
        if i[0] == user.invest_role.name:
            i[2] = 'checked'
            break

    for i in gender:
        if i[0] == user.gender.name:
            i[2] = 'checked'
            break

    industries_selected = [] if not user.interested else user.interested.split(',')

    for i in industries:
        for j in industries_selected:
            if i[0] == j:
                i[2] = 'checked'
                continue

    phases_select = [] if not user.invest_phase else user.invest_phase.split(',')

    for i in phases:
        for j in phases_select:
            if i[0] == j:
                i[2] = 'checked'

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

    return render_template('investor/profile.html', form=form, industries=industries, phases=phases, gender=gender, investment_type=investment_type)


@investor.route('/projects/')
@user_manager.login_required(User.Investor)
def project_list_all():

    projects = Project.query.all()

    for project in projects:
        if project.bp_url:
            bp_file = File.query.filter_by(server_name=project.bp_url).first()
            if bp_file:
                bp_url = get_file_url(bp_file.server_name, bp_file.local_name)
                project.bp_url = bp_url

        if project.icon_url:
            icon_file = File.query.filter_by(server_name=project.icon_url).first()
            if icon_file:
                icon_url = get_file_url(icon_file.server_name, icon_file.server_name)
                project.icon_url = icon_url

    return render_template('investor/project_list_all.html', projects=projects)


@investor.route('/projects/<int:pid>')
@user_manager.login_required(User.Investor)
def show_project(pid):

    project = Project.query.filter_by(id=pid).first()

    if project.bp_url:
        bp_file = File.query.filter_by(server_name=project.bp_url).first()
        bp_url = get_file_url(bp_file.server_name, bp_file.local_name)
        project.bp_url = bp_url

    if project.icon_url:
        icon_file = File.query.filter_by(server_name=project.icon_url).first()
        icon_url = get_file_url(icon_file.server_name, icon_file.server_name)
        project.icon_url = icon_url

    return render_template('investor/project_detail.html', project=project)


@investor.route('/projects_mine/')
@user_manager.login_required(User.Investor)
def project_list_mine():

    # projects = Project.query.filter(Project.id.in_([f.project_id for f in FavoriteProjects.query.filter_by(investor_id=user_manager.current_user.id).all()])).all()

    projects = user_manager.current_user.favorite_projects

    for project in projects:
        if project.bp_url:
            bp_file = File.query.filter_by(server_name=project.bp_url).first()
            bp_url = get_file_url(bp_file.server_name, bp_file.local_name)
            project.bp_url = bp_url

        if project.icon_url:
            icon_file = File.query.filter_by(server_name=project.icon_url).first()
            icon_url = get_file_url(icon_file.server_name, icon_file.server_name)
            project.icon_url = icon_url

    return render_template('investor/project_list_mine.html', projects=projects)


@investor.route('/projects_mine_detail/<int:pid>')
@user_manager.login_required(User.Investor)
def project_list_mine_detail(pid):
    p = Project.query.filter_by(id=pid).first_or_404()

    if p.bp_url:
        bp_file = File.query.filter_by(server_name=p.bp_url).first()
        bp_url = get_file_url(bp_file.server_name, bp_file.local_name)
        p.bp_url = bp_url

    if p.icon_url:
        icon_file = File.query.filter_by(server_name=p.icon_url).first()
        icon_url = get_file_url(icon_file.server_name, icon_file.server_name)
        p.icon_url = icon_url

    return render_template('investor/project_list_mine_detail.html', project=p)


@investor.route('/schedules/', methods=['GET'])
@user_manager.login_required(User.Investor)
def show_schedules():
    return render_template('investor/schedule_list.html')


@investor.route('/schedules/', methods=['POST'])
@user_manager.login_required(User.Investor)
def new_schedule():
    return '约谈列表页'


@investor.route('/settings/', methods=['GET'])
@user_manager.login_required(User.Investor)
def show_settings():
    form = ResetPasswordForm()

    if form.validate_on_submit():
        pass
    return render_template('investor/settings.html', form=form)


@investor.route('/settings/', methods=['POST'])
@user_manager.login_required(User.Investor)
def edit_settings():
    return '更改投资人设置'


@investor.route('/post_comment/', methods=['POST'])
@user_manager.login_required(User.Investor)
def post_comment():

    form = CommentForm()

    pid = 1
    source = 'my'

    if form.validate_on_submit():
        pid = form.pid.data
        p = Project.query.filter_by(id=pid).first_or_404()
        source = form.source.data

        c = Comment()
        c.project = p
        c.author_id = user_manager.current_user.get_id()
        c.content = form.content.data
        # c.timestamp = time.time()

        with safe_session(db):
            db.session.add(c)

    url = 'investor.show_project'

    if source == 'my':
        url = 'investor.project_list_mine_detail'

    return redirect(url_for(url, pid=pid))


# 关注或取消关注项目
@investor.route('/follow/<int:pid>/<source>', methods=['GET'])
@user_manager.login_required(User.Investor)
def follow(pid, source):
    project = Project.query.filter_by(id=pid).first_or_404()
    if user_manager.current_user.is_following_project(project):
        user_manager.current_user.unfollow_project(project)
    else:
        user_manager.current_user.follow_project(project)

    url = 'investor.project_list_mine_detail'
    if source == 'all':
        url = 'investor.show_project'

    return redirect(url_for(url, pid=project.id))
