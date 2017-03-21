from .tools import ArgumentField, ParserModel


class ProjectSearchParser(ParserModel):
    id = ArgumentField(type=int, location='args', store_missing=False)
    name = ArgumentField(type=int, location='args', store_missing=False)
    contact_name = ArgumentField(type=str, location='args', store_missing=False)
    industry = ArgumentField(type=str, location='args', store_missing=False)
    phase_index = ArgumentField(type=int, location='args', store_missing=False)
    contact_phone = ArgumentField(type=str, location='args', store_missing=False)
    starttime = ArgumentField(type=str, location='args', store_missing=False)
    endtime = ArgumentField(type=str, location='args', store_missing=False)
    page = ArgumentField(type=int, location='args', store_missing=False)


class ProjectCreateParser(ParserModel):
    name = ArgumentField(type=str, location='json', store_missing=False)
    owner_id = ArgumentField(type=int, location='json', store_missing=False)
    icon_url = ArgumentField(type=str, location='json', store_missing=False)
    industry = ArgumentField(type=str, location='json', store_missing=False)
    description = ArgumentField(type=str, location='json', store_missing=False)
    advantage = ArgumentField(type=str, location='json', store_missing=False)
    company_phase = ArgumentField(type=str, location='json', store_missing=False)
    financing_sum = ArgumentField(type=int, location='json', store_missing=False)
    bp_url = ArgumentField(type=str, location='json', store_missing=False)
    duration = ArgumentField(type=int, location='json', store_missing=False)
    financing_status = ArgumentField(type=str, location='json', store_missing=False)
    deadline = ArgumentField(type=str, location='json', store_missing=False)
    contact_name = ArgumentField(type=str, location='json', store_missing=False)
    contact_phone = ArgumentField(type=str, location='json', store_missing=False)
    contact_email = ArgumentField(type=str, location='json', store_missing=False)
    status = ArgumentField(type=str, location='json', store_missing=False)


class ServiceCategoryParser(ParserModel):
    name = ArgumentField(type=str, location='json', store_missing=False)
    description = ArgumentField(type=str, location='json', store_missing=False)


class ServiceCategorySearchParser(ParserModel):
    page = ArgumentField(type=int, default=1, location='args', store_missing=True)


class UserServiceCreateParser(ParserModel):
    ppid = ArgumentField(type=int, location='json', store_missing=True)
    service_id = ArgumentField(type=int, location='json', store_missing=True)


class CustomServiceCreateParser(ParserModel):
    ppid = ArgumentField(type=int, location='json', store_missing=True)
    # price = ArgumentField(type=str, location='json', store_missing=True)
    category_id = ArgumentField(type=int, location='json', store_missing=True)
    title = ArgumentField(type=str, location='json', store_missing=True)
    description = ArgumentField(type=str, location='json', store_missing=True)


class CustomServiceListParser(ParserModel):
    page = ArgumentField(type=int, location='json', store_missing=True)


class UserServiceListParser(ParserModel):
    page = ArgumentField(type=int, location='json', store_missing=True)


class ServiceItemSearchParser(ParserModel):
    page = ArgumentField(type=int, default=1, location='args', store_missing=True)


class BillSearchParser(ParserModel):
    page = ArgumentField(type=int, default=1, location='args', store_missing=True)


class ProfileEditParser(ParserModel):
    name = ArgumentField(type=str, default="", location='json', store_missing=True)
    phone = ArgumentField(type=str, location='json', store_missing=True)
    wechat = ArgumentField(type=str, location='json', store_missing=True)
    company = ArgumentField(type=str, location='json', store_missing=True)
    gender = ArgumentField(type=str, location='json', store_missing=True)
    avatar = ArgumentField(type=str, location='json', store_missing=True)
    resume = ArgumentField(type=str, location='json', store_missing=True)
    company_name = ArgumentField(type=str, location='json', store_missing=True)
    company_desc = ArgumentField(type=str, location='json', store_missing=True)
    company_industry = ArgumentField(type=str, location='json', store_missing=True)


class PasswordResetParser(ParserModel):
    old_pwd = ArgumentField(type=str, required=True, help='请输入原密码', location='json', store_missing=False)
    new_pwd = ArgumentField(type=str, required=True, help='请输入新密码', location='json', store_missing=False)


class PhaseParser(ParserModel):
    name = ArgumentField(type=str, location='json', store_missing=False)
    description = ArgumentField(type=str, location='json', store_missing=False)
    attachments = ArgumentField(type=str, location='json', store_missing=False)


class PhaseSearchParser(ParserModel):
    page = ArgumentField(type=int, default=1, location='args', store_missing=True)


# 项目
project_search_parser = ProjectSearchParser()
project_create_parser = ProjectCreateParser()


# 服务
service_category_parser = ServiceCategoryParser()
service_category_search_parser = ServiceCategorySearchParser()
user_service_item_parser = UserServiceCreateParser()
custom_service_item_parser = CustomServiceCreateParser()
custom_service_list_parser = CustomServiceListParser()
user_service_list_parser = UserServiceListParser()
service_item_search_parser = ServiceItemSearchParser()
bill_search_parser = BillSearchParser()


# 资料
profile_parser = ProfileEditParser()
password_reset_parser = PasswordResetParser()


# 项目阶段
phase_parser = PhaseParser()
phase_search_parser = PhaseSearchParser()
