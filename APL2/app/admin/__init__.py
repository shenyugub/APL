from flask import Blueprint, render_template, request, session, jsonify, current_app
from app import admin_manager
from app.models import Admin, File, Const
from flask_restful import Api, Resource
from app.admin.login_resource import LoginResource, ResetPasswordResource
from app.admin.project_resource import ProjectResource, ProjectListResource
from app.admin.role_resource import RoleResource, RoleListResource
from app.admin.admin_resource import AdminResource, AdminListResource
from app.admin.user_resource import UserResource, UserListResource
from app.admin.service_category_resource import ServiceCategoryResource, ServiceCategoryListResource
from app.admin.service_item_resource import ServiceItemResource, ServiceItemListResource
from app.admin.comment_resource import CommentResource, CommentListResource
from app.admin.phase_resource import PhaseResource, PhaseListResource
from app.admin.business_plan_resource import BusinessPlanResource, BusinessPlanListResource
from app.admin.schedule_resource import ScheduleResource, ScheduleListResource
from app.admin.ticket_resource import TicketResource, TicketListResource
from app.admin.attachment_resource import AttachmentResource, AttachmentListResource
from app.admin.phase_attachment_resource import PhaseAttachmentResource, PhaseAttachmentListResource
from app.admin.department_resource import DepartmentResource, DepartmentListResource
from app.admin.permission_resource import PermissionResource, PermissionListResource
from app.admin.project_phase_resource import ProjectPhaseResource, ProjectPhaseListResource
from app.admin.custom_service_item_resource import CustomServiceItemResource, CustomServiceItemListResource
from app.admin.phase_attachment_detail_resource import PhaseAttachmentDetailResource,  PhaseAttachmentDetailListResource
from app.admin.user_service_item_resource import UserServiceItemResource, UserServiceItemListResource, BillListResource
from app.admin.user_attachment_resource import UserAttachmentResource, UserAttachmentListResource
from app.utils.sts import request_sts_token, get_file_url
from app.utils.utils import get_iso_8601, get_sign_policy
from app.admin.dic1 import Dictionary
import time
import json
import base64
import uuid


admin = Blueprint('sudo', __name__)
api = Api(admin)


api.add_resource(LoginResource, '/')
api.add_resource(ResetPasswordResource, '/reset_password')

api.add_resource(ProjectListResource, '/projects')
api.add_resource(ProjectResource, '/projects/<int:pid>')

api.add_resource(RoleListResource, '/roles')
api.add_resource(RoleResource, '/roles/<int:rid>')

api.add_resource(AdminListResource, '/admins')
api.add_resource(AdminResource, '/admins/<int:aid>')

api.add_resource(UserListResource, '/users')
api.add_resource(UserResource, '/users/<int:uid>')

api.add_resource(ServiceCategoryListResource, '/service_categories')
api.add_resource(ServiceCategoryResource, '/service_categories/<int:sid>')

api.add_resource(ServiceItemResource, '/service_items/<int:sid>')
api.add_resource(ServiceItemListResource, '/service_items')

api.add_resource(CustomServiceItemResource, '/custom_service_items/<int:sid>')
api.add_resource(CustomServiceItemListResource, '/custom_service_items')

api.add_resource(CommentResource, '/comments/<int:cid>')
api.add_resource(CommentListResource, '/comments')

api.add_resource(PhaseResource, '/phases/<int:pid>')
api.add_resource(PhaseListResource, '/phases')

api.add_resource(AttachmentResource, '/attachments/<int:aid>')
api.add_resource(AttachmentListResource, '/attachments')

api.add_resource(PhaseAttachmentResource, '/phases_attachments/<int:paid>')
api.add_resource(PhaseAttachmentListResource, '/phases_attachments')

api.add_resource(BusinessPlanResource, '/bps/<int:bid>')
api.add_resource(BusinessPlanListResource, '/bps')

api.add_resource(ScheduleResource, '/schedules/<int:sid>')
api.add_resource(ScheduleListResource, '/schedules')

api.add_resource(TicketResource, '/tickets/<int:tid>')
api.add_resource(TicketListResource, '/tickets')

api.add_resource(DepartmentResource, '/departments/<int:did>')
api.add_resource(DepartmentListResource, '/departments')

api.add_resource(PermissionResource, '/permissions/<int:pid>')
api.add_resource(PermissionListResource, '/permissions')

api.add_resource(ProjectPhaseResource, '/projects_phases/<int:ppid>')
api.add_resource(ProjectPhaseListResource, '/projects_phases')

api.add_resource(PhaseAttachmentDetailResource, '/attachment_details/<int:padid>')
api.add_resource(PhaseAttachmentDetailListResource, '/attachment_details')

api.add_resource(UserServiceItemResource, '/user_service_items/<int:usiid>')
api.add_resource(UserServiceItemListResource, '/user_service_items')

api.add_resource(BillListResource, '/bills')

api.add_resource(UserAttachmentResource, '/user_attachments/<int:uaid>')
api.add_resource(UserAttachmentListResource, '/user_attachments')
api.add_resource(Dictionary, '/dic')

# @admin.route('/', methods=['GET'])
# def index():
#     return render_template('admin/index.html')
#
#
# @csrf.exempt
# @admin.route('/', methods=['POST'])
# def login():
#
#     username = request.json.get('username')
#     password = request.json.get('password')
#     vcode = request.json.get('vcode')
#
#     result = {}
#
#     if (not username.strip()) or (not password.strip()) or (not vcode.strip()):
#         pass
#     if vcode == session.get('vcode'):
#         pass
#     else:
#         result = {'errors': ['验证码错误']}
#     return jsonify(result)


@admin.route('/file/<name>', methods=['GET'])
def get_url(name):
    bp_file = File.query.filter_by(server_name=name).first()

    if bp_file:
        bp_url = get_file_url(bp_file.server_name, bp_file.local_name)
        return bp_url

    return None


@admin.route('/sts_info', methods=['GET'])
def get_upload_info():
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

    result = {}
    # result['run_mode'] = current_app.config['DEBUG']
    result['OSSAccessKeyId'] = sts.access_key_id
    result['x-oss-security-token'] = sts.security_token
    result['policy'] = policy_encode.decode()
    result['Signature'] = signature.decode()
    result['key'] = str(uuid.uuid1()).replace('-', '')
    result['success_action_status'] = '201'
    result['callback'] = base64_callback_body.decode()
    result['x:uid'] = 1  #admin_manager.current_user.get_id()
    result['x:filename'] = ''

    return jsonify(result)


@admin_manager.user_loader
def user_loader(uid):
    if uid is None:
        return None

    try:
        return Admin.query.get(uid)

    except TypeError:
        return None
    except ValueError:
        return None


@admin_manager.failure_handler
def failure_handler():
    return {Const.MESSAGE_KEY: '您尚未登录或权限不足'}, Const.STATUS_DENIED


@admin_manager.hash_generator
def hash_generator(user):
    from app.utils.utils import generate_user_hash

    return generate_user_hash(user.get_id(), user.password, admin_manager.expires, admin_manager.salt)
