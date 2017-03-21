from flask import Blueprint
from flask_restful import Api
from app.exceptions import errors

from .api import ProfileHandler, BillHandler, ProjectHandler, \
    ServiceHandler, ServiceCategoryHandler, PasswordHandler, \
    PhaseHandler, UserServiceHandler, CustomServiceHandler

startup = Blueprint('startup', __name__)

api_v1 = Api(startup, prefix='/api/v1', catch_all_404s=True, errors=errors)

# 项目接口
api_v1.add_resource(
    ProjectHandler, '/projects/', endpoint='projects_list')  # 项目列表
api_v1.add_resource(
    ProjectHandler, '/project/', endpoint='projects_create')  # 项目创建
api_v1.add_resource(
    ProjectHandler,
    '/project/<int:pid>', endpoint='project_detail_or_edit')  # 项目详情和项目修改

# # 服务接口
api_v1.add_resource(
    ServiceHandler,
    '/service/', endpoint='create_service_item')  # 创建服务
api_v1.add_resource(
    ServiceHandler,
    '/services/', endpoint='services_list')  # 服务列表

api_v1.add_resource(
    UserServiceHandler,
    '/service/user/', endpoint='user_service_create')  # 服务列表

api_v1.add_resource(
    UserServiceHandler,
    '/services/user/', endpoint='user_service_list')  # 服务列表


api_v1.add_resource(
    ServiceCategoryHandler,
    '/service/categories/', endpoint='service_categories')  # 服务分类列表
api_v1.add_resource(
    ServiceCategoryHandler,
    '/service/category/<int:scid>', endpoint='service_category')  # 服务分类
api_v1.add_resource(
    ServiceCategoryHandler,
    '/service/category/', endpoint='create_service_category')  # 服务分类

api_v1.add_resource(
    CustomServiceHandler,
    '/service/custom/', endpoint='create_custom_service_category')  # 创建自定义服务


# 账单
api_v1.add_resource(
    BillHandler,
    '/bills/', endpoint='bills')  #
api_v1.add_resource(
    BillHandler,
    '/bill/<int:sid>', endpoint='bill_item')  #

# 资料
api_v1.add_resource(
    ProfileHandler,
    '/profile/', endpoint='show_profile')  # 用户资料

api_v1.add_resource(
    PasswordHandler,
    '/password/reset/', endpoint='reset_password')  # 用户资料


# 项目阶段
api_v1.add_resource(
    PhaseHandler,
    '/phase/', endpoint='create_phase')  # 创建阶段

api_v1.add_resource(
    PhaseHandler,
    '/phase/<int:pid>', endpoint='edit_phase')  # 编辑阶段&查看阶段

api_v1.add_resource(
    PhaseHandler,
    '/phases/', endpoint='phases_list')  # 所有的阶段

#
