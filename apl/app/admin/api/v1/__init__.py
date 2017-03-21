#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/2/21 上午12:17
# @Author  : Rain
# @Desc    :
# @File    : __init__.py.py


from .admin_resource import AdminResource, AdminListResource
from .attachment_resource import AttachmentResource, AttachmentListResource
from .business_plan_resource import BusinessPlanResource, BusinessPlanListResource
from .comment_resource import CommentResource, CommentListResource
from .custom_service_item_resource import CustomServiceItemResource, CustomServiceItemListResource
from .department_resource import DepartmentResource, DepartmentListResource
from .file_resource import FileResource
from .login_resource import LoginResource, ResetPasswordResource
from .permission_resource import PermissionResource, PermissionListResource
from .phase_attachment_detail_resource import PhaseAttachmentDetailResource, PhaseAttachmentDetailListResource
from .phase_attachment_resource import PhaseAttachmentResource, PhaseAttachmentListResource
from .phase_resource import PhaseResource, PhaseListResource
from .project_phase_resource import ProjectPhaseResource, ProjectPhaseListResource
from .region_selector_resource import RegionSelectorResource
from .role_resource import RoleResource, RoleListResource
from .schedule_resource import ScheduleResource, ScheduleListResource
from .service_category_resource import ServiceCategoryResource, ServiceCategoryListResource
from .service_item_resource import ServiceItemResource, ServiceItemListResource
from .startup_resource import StartupResource, StartupListResource
from .sts_info_resource import STSInfoResource
from .ticket_resource import TicketResource, TicketListResource
from .user_attachment_resource import UserAttachmentResource, UserAttachmentListResource
from .user_service_item_resource import UserServiceItemResource, UserServiceItemListResource, BillListResource
from .project_resource import ProjectResource, ProjectListResource
from flask_restful import Api
from app.exceptions import errors
from app.admin import admin

api_v1 = Api(admin, prefix='/api/v1', catch_all_404s=True, errors=errors)


api_v1.add_resource(LoginResource, '/')
api_v1.add_resource(ResetPasswordResource, '/reset_password')

api_v1.add_resource(ProjectListResource, '/projects')
api_v1.add_resource(ProjectResource, '/projects/<int:pid>')

api_v1.add_resource(RoleListResource, '/roles')
api_v1.add_resource(RoleResource, '/roles/<int:rid>')

api_v1.add_resource(AdminListResource, '/admins')
api_v1.add_resource(AdminResource, '/admins/<int:aid>')

api_v1.add_resource(StartupListResource, '/users')
api_v1.add_resource(StartupResource, '/users/<int:uid>')

api_v1.add_resource(ServiceCategoryListResource, '/service_categories')
api_v1.add_resource(ServiceCategoryResource, '/service_categories/<int:sid>')

api_v1.add_resource(ServiceItemResource, '/service_items/<int:sid>')
api_v1.add_resource(ServiceItemListResource, '/service_items')

api_v1.add_resource(CustomServiceItemResource, '/custom_service_items/<int:sid>')
api_v1.add_resource(CustomServiceItemListResource, '/custom_service_items')

api_v1.add_resource(CommentResource, '/comments/<int:cid>')
api_v1.add_resource(CommentListResource, '/comments')

api_v1.add_resource(PhaseResource, '/phases/<int:pid>')
api_v1.add_resource(PhaseListResource, '/phases')

api_v1.add_resource(AttachmentResource, '/attachments/<int:aid>')
api_v1.add_resource(AttachmentListResource, '/attachments')

api_v1.add_resource(PhaseAttachmentResource, '/phases_attachments/<int:paid>')
api_v1.add_resource(PhaseAttachmentListResource, '/phases_attachments')

api_v1.add_resource(BusinessPlanResource, '/bps/<int:bid>')
api_v1.add_resource(BusinessPlanListResource, '/bps')

api_v1.add_resource(ScheduleResource, '/schedules/<int:sid>')
api_v1.add_resource(ScheduleListResource, '/schedules')

api_v1.add_resource(TicketResource, '/tickets/<int:tid>')
api_v1.add_resource(TicketListResource, '/tickets')

api_v1.add_resource(DepartmentResource, '/departments/<int:did>')
api_v1.add_resource(DepartmentListResource, '/departments')

api_v1.add_resource(PermissionResource, '/permissions/<int:pid>')
api_v1.add_resource(PermissionListResource, '/permissions')

api_v1.add_resource(ProjectPhaseResource, '/projects_phases/<int:ppid>')
api_v1.add_resource(ProjectPhaseListResource, '/projects_phases')

api_v1.add_resource(PhaseAttachmentDetailResource, '/attachment_details/<int:padid>')
api_v1.add_resource(PhaseAttachmentDetailListResource, '/attachment_details')

api_v1.add_resource(UserServiceItemResource, '/user_service_items/<int:usiid>')
api_v1.add_resource(UserServiceItemListResource, '/user_service_items')

api_v1.add_resource(BillListResource, '/bills')

api_v1.add_resource(UserAttachmentResource, '/user_attachments/<int:uaid>')
api_v1.add_resource(UserAttachmentListResource, '/user_attachments')

api_v1.add_resource(FileResource, '/files/<name>')
api_v1.add_resource(STSInfoResource, '/sts_info')

api_v1.add_resource(RegionSelectorResource, '/region_selectors')
